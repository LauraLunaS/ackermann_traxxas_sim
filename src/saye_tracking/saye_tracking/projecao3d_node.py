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

from message_filters import ApproximateTimeSynchronizer, Subscriber
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data, QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import Image, PointCloud2
from vision_msgs.msg import Detection2DArray


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

        topico_det = self.get_parameter('topico_deteccoes').value
        topico_masc = self.get_parameter('topico_mascaras').value
        topico_nuvem = self.get_parameter('topico_nuvem').value
        self.frame_alvo = self.get_parameter('frame_alvo').value
        slop = float(self.get_parameter('sync_slop').value)
        queue = int(self.get_parameter('sync_queue').value)

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
