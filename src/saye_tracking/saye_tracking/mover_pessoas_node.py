"""
No unico que move TODOS os atores andando (flipbook, Fase 4.6) de uma vez.

Substitui o antigo `mover_pessoa_animada_node.py` (um PROCESSO POR ATOR,
cada um com seu proprio cliente gz-transport chamando `/world/<mundo>/
set_pose` concorrentemente - ver o achado completo em `gz_pose_vector.py`,
o motivo real dessa reescrita). Aqui, 1 SO timer teleporta TODOS os atores
ativos numa unica chamada de `set_pose_vector` por tick, com 1 SO cliente
gz-transport - sem concorrencia entre processos, sem a falha silenciosa
que ela causava.

Cada tick:
  1. pra cada ator, calcula a posicao (`caminhada.posicao_no_caminho`) e o
     quadro do flipbook que deveria estar visivel agora
     (`verdade_atores.nome_quadro_ativo` - MESMA formula usada pelo
     `gravador_atores_node` pra saber qual nome ler de volta do Gazebo).
  2. monta a pose do quadro ativo de cada ator e, se o quadro mudou desde o
     tick anterior, a pose de estacionamento (`Z_ESTACIONADO`) do quadro
     antigo daquele ator.
  3. manda TODAS essas poses juntas, 1 chamada de `TeleportadorEmLote`.
  4. checa o retorno - uma falha (servico fora do ar OU Gazebo recusando a
     pose) e logada em todo tick em que acontecer, nunca descartada em
     silencio.
"""
import rclpy
from rclpy.node import Node
from saye_tracking.caminhada import posicao_no_caminho
from saye_tracking.gz_pose_vector import TeleportadorEmLote
from saye_tracking.verdade_atores import nome_quadro_ativo
import yaml

Z_ESTACIONADO = -50.0  # bem longe do chao, fora de qualquer camera


class MoverPessoasNode(Node):
    """Move N atores (flipbook) numa unica chamada de set_pose_vector por tick."""

    def __init__(self, **kwargs):
        super().__init__('mover_pessoas_node', **kwargs)

        self.declare_parameter('mundo', 'beach_world')
        self.declare_parameter('atores_yaml', '')
        self.declare_parameter('nomes_atores', [''])
        self.declare_parameter('taxa_hz', 30.0)
        self.declare_parameter('timeout_ms', 300)

        caminho_yaml = self.get_parameter('atores_yaml').value
        nomes_desejados = set(self.get_parameter('nomes_atores').value)
        self.taxa_hz = float(self.get_parameter('taxa_hz').value)

        with open(caminho_yaml, encoding='utf-8') as f:
            todos_atores = yaml.safe_load(f)['atores']
        self.atores = [a for a in todos_atores if a['nome'] in nomes_desejados]
        if not self.atores:
            raise ValueError(
                f'nenhum ator de {nomes_desejados} encontrado em {caminho_yaml}')

        self.teleportador = TeleportadorEmLote(
            self.get_parameter('mundo').value,
            timeout_ms=int(self.get_parameter('timeout_ms').value))
        self.n_ticks = 0
        self.quadro_anterior_por_nome = {a['nome']: None for a in self.atores}
        self.n_falhas_consecutivas = 0

        self.timer = self.create_timer(1.0 / self.taxa_hz, self._callback_timer)

        nomes = [a['nome'] for a in self.atores]
        self.get_logger().info(
            f'mover_pessoas_node iniciado (correcao de movimentacao, pos-4.9). '
            f'Movendo {nomes} em lote (1 chamada de "{self.teleportador.servico}" '
            f'por tick) a {self.taxa_hz}Hz.')

    def _callback_timer(self):
        tempo = self.n_ticks / self.taxa_hz
        self.n_ticks += 1

        poses = []
        for ator in self.atores:
            x, y, yaw = posicao_no_caminho(ator['velocidade'] * tempo, ator['waypoints'])
            quadro_nome = nome_quadro_ativo(ator, tempo)
            poses.append((quadro_nome, x, y, 0.0, yaw))

            anterior = self.quadro_anterior_por_nome[ator['nome']]
            if anterior is not None and anterior != quadro_nome:
                poses.append((anterior, 0.0, 0.0, Z_ESTACIONADO, 0.0))
            self.quadro_anterior_por_nome[ator['nome']] = quadro_nome

        ok, sucesso = self.teleportador.teleportar(poses)
        if sucesso:
            self.n_falhas_consecutivas = 0
            return

        self.n_falhas_consecutivas += 1
        self.get_logger().error(
            f'falha ao teleportar {len(poses)} pose(s) via '
            f'"{self.teleportador.servico}" (resposta recebida={ok}) - '
            f'{self.n_falhas_consecutivas} falha(s) consecutiva(s) deste no.')


def main(args=None):
    rclpy.init(args=args)
    node = MoverPessoasNode()
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
