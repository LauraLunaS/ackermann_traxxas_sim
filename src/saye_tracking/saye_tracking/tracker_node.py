"""
No de rastreamento (Fase 3 do pipeline de rastreamento).

Assina as deteccoes 3D (ja no frame `odom`) publicadas pelo `projecao3d_node`
(Fase 2) e mantem tracks com ID estavel ao longo do tempo, via
`Rastreador3D` (nucleo OC-SORT 3D, submodulos 3.1-3.6).

Submodulo 3.7: integracao ROS - le a mensagem de entrada, chama o
rastreador, publica o resultado.

Decisao registrada (Opcao B, 3.0): sem mensagem customizada com campo de
velocidade. Publica `Detection3DArray` (posicao + id + classe) igual a
Fase 2, e mostra a velocidade so visualmente - uma seta no MarkerArray cujo
comprimento e a posicao prevista em 1s. Uma mensagem de verdade
(`TrackedObstacleArray`) so sera criada quando a Fase 5 (costmap dinamico)
precisar consumir o numero, nao so exibi-lo.

Simplificacao deliberada: como a Fase 1 hoje so detecta a classe "person"
(config `deteccao.yaml`: `classes: ["person"]`), a classe de cada track e
fixada em "person" na publicacao, em vez de propagar a classe original da
deteccao atraves do rastreador (que e deliberadamente agnostico a classe -
so trabalha com posicao). Revisitar se/quando outras classes entrarem.
"""

from geometry_msgs.msg import Point, Vector3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from saye_tracking.projecao3d_node import TAMANHOS_BBOX
from saye_tracking.rastreador import Rastreador3D
from std_msgs.msg import ColorRGBA
from vision_msgs.msg import (
    BoundingBox3D,
    Detection3D,
    Detection3DArray,
    ObjectHypothesisWithPose,
)
from visualization_msgs.msg import Marker, MarkerArray

CLASSE_PADRAO = 'person'  # ver nota de simplificacao no topo do arquivo


class TrackerNode(Node):
    """Fase 3 - mantem tracks com ID estavel a partir das deteccoes 3D."""

    def __init__(self, **kwargs):
        super().__init__('tracker_node', **kwargs)

        self.declare_parameter('topico_deteccoes_3d', '/projecao3d_node/deteccoes_3d')
        self.declare_parameter('frame_saida', 'odom')
        self.declare_parameter('gate_distancia', 1.5)
        self.declare_parameter('peso_ocm', 1.0)
        self.declare_parameter('n_passos_oru', 5)
        self.declare_parameter('min_hits_confirmar', 3)
        self.declare_parameter('tolerancia_tentativo_segundos', 0.4)
        self.declare_parameter('tolerancia_perdido_segundos', 1.5)

        topico = self.get_parameter('topico_deteccoes_3d').value
        self.frame_saida = self.get_parameter('frame_saida').value

        self.rastreador = Rastreador3D(
            gate_distancia=self.get_parameter('gate_distancia').value,
            peso_ocm=self.get_parameter('peso_ocm').value,
            n_passos_oru=int(self.get_parameter('n_passos_oru').value),
            min_hits_confirmar=int(self.get_parameter('min_hits_confirmar').value),
            tolerancia_tentativo_segundos=self.get_parameter(
                'tolerancia_tentativo_segundos').value,
            tolerancia_perdido_segundos=self.get_parameter(
                'tolerancia_perdido_segundos').value,
        )

        qos_confiavel = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.sub_deteccoes = self.create_subscription(
            Detection3DArray, topico, self.callback_deteccoes, qos_confiavel)
        self.pub_tracks = self.create_publisher(Detection3DArray, '~/tracks', 10)
        self.pub_marcadores = self.create_publisher(MarkerArray, '~/marcadores', 10)

        self.n_mensagens = 0
        self.n_deteccoes_total = 0
        self.create_timer(3.0, self._log_diagnostico)

        self.get_logger().info(
            f'tracker_node iniciado (3.7). Assinando "{topico}", '
            f'publicando tracks em "{self.frame_saida}"')

    # ------------------------------------------------------------------
    def callback_deteccoes(self, msg: Detection3DArray):
        self.n_mensagens += 1
        self.n_deteccoes_total += len(msg.detections)

        posicoes_xy = [
            (d.results[0].pose.pose.position.x, d.results[0].pose.pose.position.y)
            for d in msg.detections if d.results
        ]
        tempo_atual = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9

        confirmados = self.rastreador.processar(posicoes_xy, tempo_atual)

        for t in confirmados:
            self.get_logger().info(
                f'  track id={t.id} odom=({t.posicao[0]:.2f}, {t.posicao[1]:.2f})  '
                f'vel=({t.velocidade[0]:.2f}, {t.velocidade[1]:.2f})',
                throttle_duration_sec=1.0)

        self.publicar_tracks(msg.header.stamp, confirmados)
        self.publicar_marcadores(msg.header.stamp, confirmados)

    def _log_diagnostico(self):
        self.get_logger().info(
            f'[3s] mensagens recebidas={self.n_mensagens}  '
            f'deteccoes total={self.n_deteccoes_total}  '
            f'tracks confirmados agora={len(self.rastreador.tracks_confirmados())}')
        self.n_mensagens = 0
        self.n_deteccoes_total = 0

    # ------------------------------------------------------------------
    def publicar_tracks(self, stamp, tracks):
        msg = Detection3DArray()
        msg.header.stamp = stamp
        msg.header.frame_id = self.frame_saida

        for t in tracks:
            d = Detection3D()
            d.header = msg.header
            d.id = str(t.id)

            hip = ObjectHypothesisWithPose()
            hip.hypothesis.class_id = CLASSE_PADRAO
            hip.hypothesis.score = 1.0
            hip.pose.pose.position = Point(x=float(t.posicao[0]), y=float(t.posicao[1]), z=0.0)
            d.results.append(hip)

            tamanho = TAMANHOS_BBOX.get(CLASSE_PADRAO, TAMANHOS_BBOX['default'])
            bbox = BoundingBox3D()
            bbox.center.position = hip.pose.pose.position
            bbox.size = Vector3(x=tamanho[0], y=tamanho[1], z=tamanho[2])
            d.bbox = bbox

            msg.detections.append(d)

        self.pub_tracks.publish(msg)

    def publicar_marcadores(self, stamp, tracks):
        marcadores = MarkerArray()

        apagar_tudo = Marker()
        apagar_tudo.header.frame_id = self.frame_saida
        apagar_tudo.header.stamp = stamp
        apagar_tudo.action = Marker.DELETEALL
        marcadores.markers.append(apagar_tudo)

        altura_visual = TAMANHOS_BBOX.get(CLASSE_PADRAO, TAMANHOS_BBOX['default'])[2]

        for t in tracks:
            z = altura_visual / 2.0

            esfera = Marker()
            esfera.header.frame_id = self.frame_saida
            esfera.header.stamp = stamp
            esfera.ns = 'tracks'
            esfera.id = t.id
            esfera.type = Marker.SPHERE
            esfera.action = Marker.ADD
            esfera.pose.position = Point(x=float(t.posicao[0]), y=float(t.posicao[1]), z=z)
            esfera.pose.orientation.w = 1.0
            esfera.scale = Vector3(x=0.25, y=0.25, z=0.25)
            esfera.color = ColorRGBA(r=0.1, g=0.6, b=1.0, a=0.9)
            marcadores.markers.append(esfera)

            # seta de velocidade: comprimento = posicao prevista em 1s -
            # unica forma de "expor" velocidade por enquanto (Opcao B, 3.0)
            seta = Marker()
            seta.header.frame_id = self.frame_saida
            seta.header.stamp = stamp
            seta.ns = 'tracks_velocidade'
            seta.id = t.id
            seta.type = Marker.ARROW
            seta.action = Marker.ADD
            seta.pose.orientation.w = 1.0
            seta.points = [
                Point(x=float(t.posicao[0]), y=float(t.posicao[1]), z=z),
                Point(x=float(t.posicao[0] + t.velocidade[0]),
                      y=float(t.posicao[1] + t.velocidade[1]), z=z),
            ]
            seta.scale = Vector3(x=0.08, y=0.15, z=0.2)
            seta.color = ColorRGBA(r=1.0, g=0.2, b=0.2, a=0.9)
            marcadores.markers.append(seta)

            texto = Marker()
            texto.header.frame_id = self.frame_saida
            texto.header.stamp = stamp
            texto.ns = 'tracks_label'
            texto.id = t.id
            texto.type = Marker.TEXT_VIEW_FACING
            texto.action = Marker.ADD
            texto.pose.position = Point(
                x=float(t.posicao[0]), y=float(t.posicao[1]), z=z + altura_visual / 2 + 0.2)
            texto.pose.orientation.w = 1.0
            texto.scale.z = 0.25
            texto.color = ColorRGBA(r=1.0, g=1.0, b=1.0, a=1.0)
            velocidade_escalar = (t.velocidade[0] ** 2 + t.velocidade[1] ** 2) ** 0.5
            texto.text = f'#{t.id} {velocidade_escalar:.1f}m/s'
            marcadores.markers.append(texto)

        self.pub_marcadores.publish(marcadores)


def main(args=None):
    rclpy.init(args=args)
    node = TrackerNode()
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
