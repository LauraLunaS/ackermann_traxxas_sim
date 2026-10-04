"""
No que faz uma pessoa andar DE VERDADE, com pernas se movendo (Fase 4.6).

Diferente do `mover_pessoa_node.py` (4.5, uma unica malha parada deslizando
de um lado pro outro), este no gerencia N modelos "quadro" pre-extraidos do
ciclo real de caminhada de um esqueleto animado (ver
`saye_description/models/pessoa_andando_*_frame_*` e o script de extracao
em scripts/bake_walk_frames.py) - um "flipbook" 3D. A cada instante,
calcula qual quadro deveria estar visivel (baseado na distancia
percorrida, nao no tempo bruto) e teleporta SO esse quadro pra posicao
real; os outros ficam estacionados bem longe (fora da vista de qualquer
camera).

Por que nao usar um <actor> (animacao de esqueleto de verdade, muito mais
simples): testado e descartado - nem rgbd_camera nem depth_camera
renderizam atores nesta maquina, em nenhuma distancia (ver achado
detalhado no `simple_world.sdf` e no README). Os quadros estaticos aqui
foram extraidos OFFLINE de um ator de verdade (skinning manual a partir do
.dae original), entao o MOVIMENTO e genuino - so a renderizacao ao vivo
que precisou virar uma sequencia de malhas estaticas.
"""
import math

from gz.msgs10.boolean_pb2 import Boolean
from gz.msgs10.pose_pb2 import Pose
from gz.transport13 import Node as NodeGz
import rclpy
from rclpy.node import Node
from saye_tracking.caminhada import indice_quadro, posicao_no_caminho

Z_ESTACIONADO = -50.0  # bem longe do chao, fora de qualquer camera


class MoverPessoaAnimadaNode(Node):
    """Fase 4.6 - cicla entre N quadros de caminhada seguindo waypoints em loop."""

    def __init__(self, **kwargs):
        super().__init__('mover_pessoa_animada_node', **kwargs)

        self.declare_parameter('mundo', 'beach_world')
        self.declare_parameter('prefixo_modelo', 'pessoa_andando_1_frame_')
        self.declare_parameter('n_quadros', 6)
        self.declare_parameter('waypoints', [2.0, 0.0, 2.0, 2.0])
        self.declare_parameter('velocidade', 0.3)
        self.declare_parameter('comprimento_passada', 1.2)
        self.declare_parameter('taxa_hz', 10.0)

        self.servico = f"/world/{self.get_parameter('mundo').value}/set_pose"
        self.prefixo = self.get_parameter('prefixo_modelo').value
        self.n_quadros = int(self.get_parameter('n_quadros').value)
        flat = self.get_parameter('waypoints').value
        self.waypoints = [(flat[i], flat[i + 1]) for i in range(0, len(flat), 2)]
        self.velocidade = self.get_parameter('velocidade').value
        self.comprimento_passada = self.get_parameter('comprimento_passada').value

        self.no_gz = NodeGz()
        self.quadro_visivel_anterior = None
        self.n_ticks = 0
        self.taxa_hz = self.get_parameter('taxa_hz').value
        self.timer = self.create_timer(1.0 / self.taxa_hz, self._callback_timer)

        self.get_logger().info(
            f'mover_pessoa_animada_node iniciado (Fase 4.6). "{self.prefixo}*" '
            f'({self.n_quadros} quadros) em loop por {self.waypoints} '
            f'a {self.velocidade} m/s via "{self.servico}".')

    def _teleportar(self, nome_modelo, x, y, z, yaw):
        req = Pose()
        req.name = nome_modelo
        req.position.x = x
        req.position.y = y
        req.position.z = z
        req.orientation.z = math.sin(yaw / 2.0)
        req.orientation.w = math.cos(yaw / 2.0)
        self.no_gz.request(self.servico, req, Pose, Boolean, 200)

    def _callback_timer(self):
        tempo = self.n_ticks / self.taxa_hz
        self.n_ticks += 1

        x, y, yaw = posicao_no_caminho(self.velocidade * tempo, self.waypoints)
        quadro_ativo = indice_quadro(
            tempo, velocidade=self.velocidade, n_quadros=self.n_quadros,
            comprimento_passada=self.comprimento_passada)

        self._teleportar(f'{self.prefixo}{quadro_ativo}', x, y, 0.0, yaw)

        mudou = (self.quadro_visivel_anterior is not None
                 and self.quadro_visivel_anterior != quadro_ativo)
        if mudou:
            self._teleportar(
                f'{self.prefixo}{self.quadro_visivel_anterior}', 0.0, 0.0, Z_ESTACIONADO, 0.0)
        self.quadro_visivel_anterior = quadro_ativo


def main(args=None):
    rclpy.init(args=args)
    node = MoverPessoaAnimadaNode()
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
