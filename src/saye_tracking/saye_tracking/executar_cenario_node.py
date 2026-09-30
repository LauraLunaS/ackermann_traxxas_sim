"""
No executor de cenario (submodulo 4.3 da Fase 4 - bancada de avaliacao).

Liga os roteiros de `cenarios.py` (puro Python) ao robo de verdade -
publica `/cmd_vel` seguindo o roteiro do cenario escolhido (parametro
`cenario`), a uma taxa fixa, ate a duracao total acabar, depois para o
robo (zera o `Twist`) e encerra. Pensado pra rodar em paralelo com o
`gravador_node` (4.1): liga cenario + gravador, espera acabar, chama o
servico `~/salvar` do gravador, roda o `comparador` (4.2) em cima do
resultado.
"""
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from saye_tracking.cenarios import CENARIOS, comando_no_instante, duracao_total


class ExecutarCenarioNode(Node):
    """Fase 4.3 - publica /cmd_vel seguindo o roteiro de um cenario de teste."""

    def __init__(self, **kwargs):
        super().__init__('executar_cenario_node', **kwargs)

        self.declare_parameter('cenario', 'parado')
        self.declare_parameter('taxa_hz', 20.0)

        self.nome_cenario = self.get_parameter('cenario').value
        if self.nome_cenario not in CENARIOS:
            raise ValueError(
                f'Cenario "{self.nome_cenario}" desconhecido. '
                f'Opcoes: {sorted(CENARIOS.keys())}')

        self.duracao = duracao_total(self.nome_cenario)
        self.pub_cmd_vel = self.create_publisher(Twist, '/cmd_vel', 10)

        # contagem de ticks, nao subtracao de Time absoluto: com
        # use_sim_time=true, self.get_clock().now() no __init__ costuma vir
        # zerado (antes do 1o /clock chegar) e, no timer, ja vem com o
        # relogio de sim corrente (dezenas de segundos desde o boot do
        # mundo) - a diferenca estoura a duracao do cenario na 1a chamada.
        # Contar ticks (cada um = 1/taxa_hz) e imune a isso.
        self.n_ticks = 0
        self.taxa_hz = self.get_parameter('taxa_hz').value
        self.timer = self.create_timer(1.0 / self.taxa_hz, self._callback_timer)

        self.get_logger().info(
            f'executar_cenario_node iniciado (4.3). Cenario="{self.nome_cenario}" '
            f'duracao={self.duracao:.1f}s')

    def _callback_timer(self):
        tempo_decorrido = self.n_ticks / self.taxa_hz
        self.n_ticks += 1
        comando = comando_no_instante(self.nome_cenario, tempo_decorrido)

        if comando is None:
            self.pub_cmd_vel.publish(Twist())  # para o robo
            self.get_logger().info(f'Cenario "{self.nome_cenario}" concluido.')
            self.timer.cancel()
            rclpy.shutdown()
            return

        vx, wz = comando
        msg = Twist()
        msg.linear.x = vx
        msg.angular.z = wz
        self.pub_cmd_vel.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ExecutarCenarioNode()
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
