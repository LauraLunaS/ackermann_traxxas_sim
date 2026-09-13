"""
No de rastreamento (Fase 3 do pipeline de rastreamento).

Assina as deteccoes 3D (ja no frame `odom`) publicadas pelo `projecao3d_node`
(Fase 2) e, nos proximos submodulos, vai mante-las como tracks com ID
estavel ao longo do tempo (nucleo OC-SORT em 3D).

Submodulo 3.0: so scaffold - assina e loga. Nenhuma logica de rastreamento
ainda (isso comeca no 3.1, o filtro de Kalman de um track sozinho).

Decisao registrada (Opcao B): por enquanto NAO existe uma mensagem
customizada com campo de velocidade - o "saye_tracking" e um pacote
ament_python e nao gera mensagens (isso exigiria um pacote ament_cmake
irmao, tipo o `saye_msgs` do outro repo). A velocidade, quando existir
(submodulo 3.6+), sai por enquanto so visualmente (seta no MarkerArray);
uma mensagem de verdade (`TrackedObstacleArray`) so sera criada quando a
Fase 5 (costmap dinamico) precisar consumir o numero, nao so exibi-lo.
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from vision_msgs.msg import Detection3DArray


class TrackerNode(Node):
    """Fase 3 - mantem tracks com ID estavel a partir das deteccoes 3D."""

    def __init__(self, **kwargs):
        super().__init__('tracker_node', **kwargs)

        self.declare_parameter('topico_deteccoes_3d', '/projecao3d_node/deteccoes_3d')
        topico = self.get_parameter('topico_deteccoes_3d').value

        qos_confiavel = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.sub_deteccoes = self.create_subscription(
            Detection3DArray, topico, self.callback_deteccoes, qos_confiavel)

        self.n_mensagens = 0
        self.n_deteccoes_total = 0
        self.create_timer(3.0, self._log_diagnostico)

        self.get_logger().info(
            f'tracker_node iniciado (3.0 - so scaffold). Assinando "{topico}"')

    # ------------------------------------------------------------------
    def callback_deteccoes(self, msg: Detection3DArray):
        self.n_mensagens += 1
        self.n_deteccoes_total += len(msg.detections)

        for d in msg.detections:
            p = d.results[0].pose.pose.position if d.results else None
            classe = d.results[0].hypothesis.class_id if d.results else '?'
            if p is not None:
                self.get_logger().info(
                    f'  deteccao id={d.id} classe={classe} '
                    f'odom=({p.x:.2f}, {p.y:.2f}, {p.z:.2f})',
                    throttle_duration_sec=1.0)

    def _log_diagnostico(self):
        self.get_logger().info(
            f'[3s] mensagens recebidas={self.n_mensagens}  '
            f'deteccoes total={self.n_deteccoes_total}')
        self.n_mensagens = 0
        self.n_deteccoes_total = 0


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
