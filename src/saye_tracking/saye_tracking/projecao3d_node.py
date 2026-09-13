"""
No de projecao 3D (Fase 2 do pipeline de rastreamento).

Recebe, sincronizadas por timestamp:
  - deteccoes 2D          (vision_msgs/Detection2DArray)  <- Fase 1
  - mascara de instancias (sensor_msgs/Image, mono8)      <- Fase 1
  - nuvem de pontos       (sensor_msgs/PointCloud2)        <- simulador / RealSense

Estrategia "Caminho B": em vez de deprojetar a imagem de profundidade, le
diretamente o ponto 3D ja calculado na nuvem organizada (indice = v*width + u).

Submodulo 2.1: apenas a assinatura + sincronizacao. A extracao 3D, o
transform para `odom` e a publicacao entram nos submodulos 2.2-2.4.
"""

from geometry_msgs.msg import Point, PointStamped, Vector3
from message_filters import ApproximateTimeSynchronizer, Subscriber
import numpy as np
import rclpy
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data, QoSProfile, ReliabilityPolicy
from rclpy.time import Time
from sensor_msgs.msg import Image, PointCloud2
from sensor_msgs_py import point_cloud2 as pc2
from std_msgs.msg import ColorRGBA
from tf2_geometry_msgs import do_transform_point
import tf2_ros
from vision_msgs.msg import (
    BoundingBox3D,
    Detection2DArray,
    Detection3D,
    Detection3DArray,
    ObjectHypothesisWithPose,
)
from visualization_msgs.msg import Marker, MarkerArray

# 2.4: tamanho de bbox 3D por classe (x, y, z em metros); usa "default" p/
# classes nao listadas. Estimativa grosseira - refina quando tiver Fase 4/5.
TAMANHOS_BBOX = {
    'person': (0.5, 0.5, 1.7),
    'default': (0.5, 0.5, 1.0),
}


def _stamp_ns(stamp) -> int:
    return int(stamp.sec) * 1_000_000_000 + int(stamp.nanosec)


class Projecao3DNode(Node):
    """Fase 2 - projecao das deteccoes 2D para posicao 3D no frame odom."""

    def __init__(self, **kwargs):
        super().__init__('projecao3d_node', **kwargs)

        # --- Parametros ---------------------------------------------------
        self.declare_parameter('topico_deteccoes', '/deteccao_node/deteccoes')
        self.declare_parameter('topico_mascaras', '/deteccao_node/mascaras')
        self.declare_parameter('topico_nuvem', '/camera/realsense/points')
        self.declare_parameter('frame_alvo', 'odom')
        self.declare_parameter('sync_slop', 0.08)      # s: folga do sincronizador
        self.declare_parameter('sync_queue', 10)
        self.declare_parameter('min_pixels_mascara', 20)   # 2.2: min. pixels na mascara
        self.declare_parameter('min_pixels_validos', 10)   # 2.2: min. pontos 3D finitos
        self.declare_parameter('tf_timeout', 0.2)          # 2.3: espera pelo TF, em s

        topico_det = self.get_parameter('topico_deteccoes').value
        topico_masc = self.get_parameter('topico_mascaras').value
        topico_nuvem = self.get_parameter('topico_nuvem').value
        self.frame_alvo = self.get_parameter('frame_alvo').value
        slop = float(self.get_parameter('sync_slop').value)
        queue = int(self.get_parameter('sync_queue').value)
        self.min_pixels_mascara = int(self.get_parameter('min_pixels_mascara').value)
        self.min_pixels_validos = int(self.get_parameter('min_pixels_validos').value)
        self.tf_timeout = float(self.get_parameter('tf_timeout').value)

        # --- 2.3: TF camera -> frame_alvo (odom) -------------------------
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # --- QoS por entrada (tem que casar com quem publica) -----------
        qos_confiavel = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)

        # --- Assinantes sincronizados ---------------------------------
        self.sub_det = Subscriber(
            self, Detection2DArray, topico_det, qos_profile=qos_confiavel)
        self.sub_masc = Subscriber(
            self, Image, topico_masc, qos_profile=qos_profile_sensor_data)
        self.sub_nuvem = Subscriber(
            self, PointCloud2, topico_nuvem, qos_profile=qos_profile_sensor_data)

        self.sync = ApproximateTimeSynchronizer(
            [self.sub_det, self.sub_masc, self.sub_nuvem],
            queue_size=queue, slop=slop)
        self.sync.registerCallback(self.callback_sincronizado)

        # --- 2.4: publicacao do resultado --------------------------------
        self.pub_deteccoes_3d = self.create_publisher(
            Detection3DArray, '~/deteccoes_3d', 10)
        self.pub_marcadores = self.create_publisher(
            MarkerArray, '~/marcadores', 10)

        # --- Diagnostico: contadores individuais + timer ---------------
        self.n_det = self.n_masc = self.n_nuvem = self.n_sync = 0
        self.sub_det.registerCallback(lambda _: self._conta('det'))
        self.sub_masc.registerCallback(lambda _: self._conta('masc'))
        self.sub_nuvem.registerCallback(lambda _: self._conta('nuvem'))
        self.create_timer(3.0, self._log_diagnostico)

        self.get_logger().info(
            f'projecao3d_node iniciado (2.1). '
            f'Sincronizando:\n'
            f'  deteccoes: {topico_det}\n'
            f'  mascaras : {topico_masc}\n'
            f'  nuvem    : {topico_nuvem}\n'
            f'  slop={slop}s  queue={queue}  frame_alvo={self.frame_alvo}')

    # ------------------------------------------------------------------
    def _conta(self, qual: str):
        setattr(self, f'n_{qual}', getattr(self, f'n_{qual}') + 1)

    def _log_diagnostico(self):
        self.get_logger().info(
            f'[3s] recebidos  det={self.n_det}  masc={self.n_masc}  '
            f'nuvem={self.n_nuvem}  |  sincronizados={self.n_sync}')
        self.n_det = self.n_masc = self.n_nuvem = self.n_sync = 0

    # ------------------------------------------------------------------
    def callback_sincronizado(self, det: Detection2DArray, masc: Image,
                              nuvem: PointCloud2):
        self.n_sync += 1

        stamps = {
            'det': _stamp_ns(det.header.stamp),
            'masc': _stamp_ns(masc.header.stamp),
            'nuvem': _stamp_ns(nuvem.header.stamp),
        }
        spread_ms = (max(stamps.values()) - min(stamps.values())) / 1e6

        nuvem_organizada = nuvem.height > 1
        self.get_logger().info(
            f'SYNC  deteccoes={len(det.detections)}  '
            f'mascara={masc.width}x{masc.height} ({masc.encoding})  '
            f'nuvem={nuvem.width}x{nuvem.height} '
            f'{"organizada" if nuvem_organizada else "NAO-organizada!"}  '
            f'spread_stamps={spread_ms:.1f}ms  '
            f'frame_nuvem="{nuvem.header.frame_id}"',
            throttle_duration_sec=2.0)

        # checagens de sanidade que os proximos submodulos assumem
        if not nuvem_organizada:
            self.get_logger().warn(
                'Nuvem NAO organizada (height=1): o Caminho B precisa de nuvem '
                'organizada para indexar por pixel. Verificar o sensor.',
                throttle_duration_sec=10.0)
        if (masc.width, masc.height) != (nuvem.width, nuvem.height):
            self.get_logger().warn(
                f'Mascara {masc.width}x{masc.height} != nuvem '
                f'{nuvem.width}x{nuvem.height}: precisam da mesma resolucao.',
                throttle_duration_sec=10.0)
            return

        # --- 2.2/2.3: extrair a posicao 3D de cada deteccao e levar p/ odom
        mascara_arr = np.frombuffer(bytes(masc.data), dtype=np.uint8).reshape(
            masc.height, masc.width)

        processadas = []  # lista de (id_str, classe, score, posicao_odom)
        for i, deteccao in enumerate(det.detections):
            resultado = self.extrair_ponto_3d(nuvem, mascara_arr, i)
            if resultado is None:
                self.get_logger().debug(f'deteccao {i}: sem posicao 3D valida')
                continue
            posicao_cam, n_mascara, n_validos = resultado

            posicao_odom = self.transformar_para_odom(
                posicao_cam, nuvem.header.frame_id, det.header.stamp)
            if posicao_odom is None:
                continue  # TF ainda nao disponivel para este instante

            if deteccao.results:
                classe = deteccao.results[0].hypothesis.class_id
                score = deteccao.results[0].hypothesis.score
            else:
                classe, score = '?', 0.0

            self.get_logger().info(
                f'  deteccao {i} ({classe}): odom='
                f'({posicao_odom[0]:.2f}, {posicao_odom[1]:.2f}, {posicao_odom[2]:.2f})  '
                f'[camera=({posicao_cam[0]:.2f}, {posicao_cam[1]:.2f}, {posicao_cam[2]:.2f})]  '
                f'pixels_mascara={n_mascara}  pixels_validos={n_validos}',
                throttle_duration_sec=1.0)

            processadas.append((deteccao.id, classe, score, posicao_odom))

        # --- 2.4: publicar Detection3DArray + MarkerArray ----------------
        self.publicar_deteccoes_3d(det.header.stamp, processadas)
        self.publicar_marcadores(det.header.stamp, processadas)

    # ------------------------------------------------------------------
    def publicar_deteccoes_3d(self, stamp, processadas):
        msg = Detection3DArray()
        msg.header.stamp = stamp
        msg.header.frame_id = self.frame_alvo

        for id_str, classe, score, posicao in processadas:
            d = Detection3D()
            d.header = msg.header
            d.id = id_str

            hip = ObjectHypothesisWithPose()
            hip.hypothesis.class_id = classe
            hip.hypothesis.score = float(score)
            hip.pose.pose.position = Point(
                x=float(posicao[0]), y=float(posicao[1]), z=float(posicao[2]))
            d.results.append(hip)

            tamanho = TAMANHOS_BBOX.get(classe, TAMANHOS_BBOX['default'])
            bbox = BoundingBox3D()
            bbox.center.position = hip.pose.pose.position
            bbox.size = Vector3(x=tamanho[0], y=tamanho[1], z=tamanho[2])
            d.bbox = bbox

            msg.detections.append(d)

        self.pub_deteccoes_3d.publish(msg)

    # ------------------------------------------------------------------
    def publicar_marcadores(self, stamp, processadas):
        marcadores = MarkerArray()

        # limpa os marcadores do frame anterior antes de desenhar os novos -
        # senao, quando uma deteccao some, a bolinha dela fica presa no RViz.
        apagar_tudo = Marker()
        apagar_tudo.header.frame_id = self.frame_alvo
        apagar_tudo.header.stamp = stamp
        apagar_tudo.action = Marker.DELETEALL
        marcadores.markers.append(apagar_tudo)

        for i, (id_str, classe, score, posicao) in enumerate(processadas):
            tamanho = TAMANHOS_BBOX.get(classe, TAMANHOS_BBOX['default'])

            esfera = Marker()
            esfera.header.frame_id = self.frame_alvo
            esfera.header.stamp = stamp
            esfera.ns = 'deteccoes_3d'
            esfera.id = i
            esfera.type = Marker.SPHERE
            esfera.action = Marker.ADD
            esfera.pose.position = Point(
                x=float(posicao[0]), y=float(posicao[1]), z=float(posicao[2]))
            esfera.pose.orientation.w = 1.0
            esfera.scale = Vector3(x=0.2, y=0.2, z=0.2)  # marca a posicao, nao o bbox
            esfera.color = ColorRGBA(r=1.0, g=0.8, b=0.0, a=0.85)
            marcadores.markers.append(esfera)

            texto = Marker()
            texto.header.frame_id = self.frame_alvo
            texto.header.stamp = stamp
            texto.ns = 'deteccoes_3d_label'
            texto.id = i
            texto.type = Marker.TEXT_VIEW_FACING
            texto.action = Marker.ADD
            texto.pose.position = Point(
                x=float(posicao[0]), y=float(posicao[1]),
                z=float(posicao[2]) + tamanho[2] / 2 + 0.2)
            texto.pose.orientation.w = 1.0
            texto.scale.z = 0.25
            texto.color = ColorRGBA(r=1.0, g=1.0, b=1.0, a=1.0)
            texto.text = f'{classe} {score:.2f} #{id_str}'
            marcadores.markers.append(texto)

        self.pub_marcadores.publish(marcadores)

    # ------------------------------------------------------------------
    def transformar_para_odom(self, posicao_camera: np.ndarray,
                              frame_origem: str, stamp):
        """
        Transforma um ponto 3D do frame da camera para `self.frame_alvo`.

        Retorna None (e loga um aviso, com throttle) se o TF para o instante
        pedido ainda nao estiver disponivel - comum nos primeiros segundos
        apos o boot, enquanto a cadeia de TF (que inclui um /tf_static
        latched) ainda esta se montando.
        """
        ponto = PointStamped()
        ponto.header.frame_id = frame_origem
        ponto.header.stamp = stamp
        ponto.point.x = float(posicao_camera[0])
        ponto.point.y = float(posicao_camera[1])
        ponto.point.z = float(posicao_camera[2])

        try:
            transform = self.tf_buffer.lookup_transform(
                self.frame_alvo, frame_origem, Time.from_msg(stamp),
                timeout=Duration(seconds=self.tf_timeout))
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException,
                tf2_ros.ExtrapolationException) as e:
            self.get_logger().warn(
                f'TF {frame_origem} -> {self.frame_alvo} indisponivel: '
                f'{type(e).__name__}: {e}', throttle_duration_sec=5.0)
            return None

        ponto_alvo = do_transform_point(ponto, transform)
        return np.array(
            [ponto_alvo.point.x, ponto_alvo.point.y, ponto_alvo.point.z])

    # ------------------------------------------------------------------
    def extrair_ponto_3d(self, nuvem: PointCloud2, mascara_arr: np.ndarray,
                         indice_deteccao: int):
        """
        Extrai a posicao 3D de uma deteccao a partir dos pixels da mascara.

        Le os pontos da nuvem organizada (no frame da nuvem, ex.: corpo da
        camera) nos pixels da mascara. Retorna
        (posicao_xyz, n_pixels_mascara, n_pixels_validos) ou None se nao
        houver pixels/pontos suficientes.
        """
        ys, xs = np.where(mascara_arr == indice_deteccao + 1)
        n_mascara = len(xs)
        if n_mascara < self.min_pixels_mascara:
            return None

        indices_planos = ys.astype(np.int64) * nuvem.width + xs.astype(np.int64)
        pontos = pc2.read_points_numpy(
            nuvem, field_names=('x', 'y', 'z'), uvs=indices_planos)

        finitos = np.isfinite(pontos).all(axis=1)
        pontos_validos = pontos[finitos]
        n_validos = len(pontos_validos)
        if n_validos < self.min_pixels_validos:
            return None

        posicao = np.median(pontos_validos, axis=0)
        return posicao, n_mascara, n_validos


def main(args=None):
    rclpy.init(args=args)
    node = Projecao3DNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
