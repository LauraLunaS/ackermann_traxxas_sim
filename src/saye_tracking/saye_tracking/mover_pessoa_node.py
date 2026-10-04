"""
No que faz a pessoa detectavel andar de verdade (Fase 4 - alvo em movimento).

Liga `caminhada.py` (puro Python) ao Gazebo via `gz-transport` direto (nao
`ros_gz_bridge`) - chama o servico `/world/<mundo>/set_pose` num timer,
teleportando a pessoa pra posicao calculada a cada instante. Ver o
docstring de `caminhada.py` pro motivo de usar teleporte em vez de
fisica (force/torque): um corpo alto tomba sob o plugin TrajectoryFollower,
testado e descartado.
"""
import math

from gz.msgs10.boolean_pb2 import Boolean
from gz.msgs10.pose_pb2 import Pose
from gz.transport13 import Node as NodeGz
import rclpy
from rclpy.node import Node
from saye_tracking.caminhada import posicao_no_caminho

YAW_PADRAO = -1.5708  # mesma orientacao original da pessoa em simple_world.sdf
OFFSET_YAW = YAW_PADRAO - 1.5708  # o caminho original andava em +y (yaw pi/2)


class MoverPessoaNode(Node):
    """Fase 4 - teleporta a pessoa detectavel seguindo waypoints em loop."""

    def __init__(self, **kwargs):
        super().__init__('mover_pessoa_node', **kwargs)

        self.declare_parameter('mundo', 'beach_world')
        self.declare_parameter('nome_modelo', 'pessoa_detectavel')
        self.declare_parameter('waypoints', [3.5, 0.0, 3.5, 2.0])
        self.declare_parameter('velocidade', 0.35)
        self.declare_parameter('taxa_hz', 10.0)

        self.servico = (
            f"/world/{self.get_parameter('mundo').value}/set_pose")
        self.nome_modelo = self.get_parameter('nome_modelo').value
        flat = self.get_parameter('waypoints').value
        self.waypoints = [(flat[i], flat[i + 1]) for i in range(0, len(flat), 2)]
        self.velocidade = self.get_parameter('velocidade').value

        self.no_gz = NodeGz()
        self.n_ticks = 0
        self.taxa_hz = self.get_parameter('taxa_hz').value
        self.timer = self.create_timer(1.0 / self.taxa_hz, self._callback_timer)

        self.get_logger().info(
            f'mover_pessoa_node iniciado (Fase 4). "{self.nome_modelo}" '
            f'em loop por {self.waypoints} a {self.velocidade} m/s '
            f'via "{self.servico}".')

    def _callback_timer(self):
        tempo = self.n_ticks / self.taxa_hz
        self.n_ticks += 1

        x, y, yaw_caminho = posicao_no_caminho(self.velocidade * tempo, self.waypoints)
        yaw = yaw_caminho + OFFSET_YAW

        req = Pose()
        req.name = self.nome_modelo
        req.position.x = x
        req.position.y = y
        req.position.z = 0.0
        req.orientation.z = math.sin(yaw / 2.0)
        req.orientation.w = math.cos(yaw / 2.0)

        self.no_gz.request(self.servico, req, Pose, Boolean, 200)


def main(args=None):
    rclpy.init(args=args)
    node = MoverPessoaNode()
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
