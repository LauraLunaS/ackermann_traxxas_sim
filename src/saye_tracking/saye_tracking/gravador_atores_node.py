"""
No gravador para atores andando.

Submodulo 4.9 - bancada de avaliacao multi-pessoa. Igual ao
`gravador_node.py` (4.1) do lado das HIPOTESES (assina
`/tracker_node/tracks`), mas troca o lado da VERDADE: em vez de ler de
volta do bridge de pose do Gazebo (fragil pros atores com flipbook - ver
`verdade_atores.py`), RECALCULA a posicao de cada ator com a mesma formula
que o `mover_pessoa_animada_node` dele usa, numa taxa fixa.

Sincronizacao do "tempo zero": os `mover_pessoa_animada_node` contam
ticks PROPRIOS a partir de quando CADA UM comeca (`n_ticks / taxa_hz`,
nao uma subtracao de `Time` absoluto - exatamente pra evitar o problema
descrito em `executar_cenario_node.py`: com `use_sim_time=true`,
`self.get_clock().now()` no `__init__` costuma vir zerado, antes do 1o
`/clock` chegar). Este gravador faz o mesmo: conta os proprios ticks
(`_callback_verdade`) em vez de guardar um `Time` de referencia. A
bancada (`rodar_suite_pessoas.py`) sobe os movers primeiro, espera 1s
assentar (mesma convencao de `rodar_suite.py` apos resetar pose) e so
entao sobe este gravador - entao o "zero" daqui fica levemente ATRASADO
em relacao ao zero real de cada mover (por ~1s). Isso desloca a verdade
por `velocidade * ~1s` (poucos decimetros, a 0.24-0.3 m/s) - constante
durante todo o teste, nao cresce com o tempo, e fica bem abaixo do
`limiar_distancia` do comparador (0.5m).

Tambem grava a pose REAL do robo (assina `/odom`), nao mais estimada
analiticamente a partir do cmd_vel do cenario. Motivo: ao investigar por
que o MOTA de "robo andando" cai tanto (ver README, 4.9), a hipotese era
geometrica - o robo anda reto na direcao da pessoa_1 e ela acaba saindo
do FOV estreito (87 graus) da camera conforme a distancia encurta. Uma
reconstrucao analitica da pose (supondo yaw=0 fixo) ate bateu MUITO bem
com o instante exato em que o track morre num combo, mas em outro combo
piorou o MOTA ao filtrar - sinal de que a pose analitica (que nao sabe o
yaw real de spawn) nao e precisa o suficiente pra decidir visibilidade
com confianca. Gravando a pose real, o pos-processamento que decide
"a pessoa estava dentro do cone da camera nesse instante" fica exato,
em vez de aproximado.
"""
import math
import os

from nav_msgs.msg import Odometry
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from saye_tracking.gravador import Gravador
from saye_tracking.verdade_atores import posicoes_verdadeiras
from std_srvs.srv import Trigger
from vision_msgs.msg import Detection3DArray
import yaml


class GravadorAtoresNode(Node):
    """Fase 4.9 - grava hipoteses do tracker vs verdade analitica de N atores andando."""

    def __init__(self, **kwargs):
        super().__init__('gravador_atores_node', **kwargs)

        self.declare_parameter('topico_tracks', '/tracker_node/tracks')
        self.declare_parameter('topico_odom', '/odom')
        self.declare_parameter('atores_yaml', '')
        self.declare_parameter('nomes_atores', [''])  # subconjunto de atores_yaml a usar
        self.declare_parameter('taxa_verdade_hz', 20.0)
        self.declare_parameter('diretorio_saida', '/tmp/saye_tracking_gravacao_atores')

        topico_tracks = self.get_parameter('topico_tracks').value
        topico_odom = self.get_parameter('topico_odom').value
        caminho_yaml = self.get_parameter('atores_yaml').value
        nomes_desejados = set(self.get_parameter('nomes_atores').value)
        self.taxa_verdade_hz = float(self.get_parameter('taxa_verdade_hz').value)
        self.diretorio_saida = self.get_parameter('diretorio_saida').value
        self.n_ticks_verdade = 0  # contagem de ticks, nao Time absoluto - ver nota acima

        with open(caminho_yaml, encoding='utf-8') as f:
            todos_atores = yaml.safe_load(f)['atores']
        self.atores = [a for a in todos_atores if a['nome'] in nomes_desejados]
        if not self.atores:
            raise ValueError(
                f'nenhum ator de {nomes_desejados} encontrado em {caminho_yaml}')

        self.gravador = Gravador()

        qos_confiavel = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.sub_tracks = self.create_subscription(
            Detection3DArray, topico_tracks, self.callback_tracks, qos_confiavel)
        self.sub_odom = self.create_subscription(
            Odometry, topico_odom, self.callback_odom, qos_confiavel)

        self.timer_verdade = self.create_timer(1.0 / self.taxa_verdade_hz, self._callback_verdade)

        self.srv_salvar = self.create_service(Trigger, '~/salvar', self.callback_salvar)

        self.get_logger().info(
            f'gravador_atores_node iniciado (4.9). Hipoteses de "{topico_tracks}", '
            f'verdade analitica de {[a["nome"] for a in self.atores]}. '
            f'Ctrl+C ou servico "~/salvar" grava em "{self.diretorio_saida}".')

    # ------------------------------------------------------------------
    def callback_tracks(self, msg: Detection3DArray):
        tempo = self.get_clock().now().nanoseconds * 1e-9
        if tempo <= 0.0:
            return  # relogio de sim ainda nao sincronizou (ver nota abaixo)
        for d in msg.detections:
            if not d.results:
                continue
            pos = d.results[0].pose.pose.position
            self.gravador.registrar_hipotese(tempo, d.id, pos.x, pos.y)

    def callback_odom(self, msg: Odometry):
        tempo = self.get_clock().now().nanoseconds * 1e-9
        if tempo <= 0.0:
            return  # relogio de sim ainda nao sincronizou (ver nota acima)
        pos = msg.pose.pose.position
        q = msg.pose.pose.orientation
        yaw = math.atan2(2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y * q.y + q.z * q.z))
        self.gravador.registrar_robo(tempo, pos.x, pos.y, yaw)

    def _callback_verdade(self):
        tempo_desde_inicio = self.n_ticks_verdade / self.taxa_verdade_hz
        self.n_ticks_verdade += 1
        # tempo gravado na hipotese/verdade (pro comparador agrupar em frames)
        # pode usar o Time absoluto normalmente - so a REFERENCIA do caminho
        # andado (tempo_desde_inicio, acima) e que precisa ser por tick.
        #
        # Achado (4.9): com `use_sim_time=true`, as primeiras chamadas de
        # callback (tanto aqui quanto em `callback_tracks`) podem acontecer
        # ANTES do 1o `/clock` chegar - `self.get_clock().now()` volta 0.0
        # nesse caso (mesmo problema ja documentado em
        # `executar_cenario_node.py`). Sem filtrar, esses poucos registros
        # com tempo=0.0 caem todos no "frame 0" do comparador, onde a
        # verdade NUNCA existe (a janela real do teste comeca bem depois de
        # 0) - gerando falsos positivos (hipotese) ou poluindo a verdade com
        # um frame fantasma. Descartar silenciosamente esses poucos
        # registros iniciais (tempo <= 0) e mais simples e robusto que tentar
        # esperar o /clock sincronizar antes de criar os subscribers.
        tempo_sim = self.get_clock().now().nanoseconds * 1e-9
        if tempo_sim <= 0.0:
            return
        posicoes = posicoes_verdadeiras(self.atores, tempo_desde_inicio)
        for nome, (x, y) in posicoes.items():
            self.gravador.registrar_verdade(tempo_sim, nome, x, y)

    # ------------------------------------------------------------------
    def callback_salvar(self, request, response):
        caminhos = self.salvar()
        response.success = True
        response.message = f'gravado em {caminhos[0]}, {caminhos[1]} e {caminhos[2]}'
        return response

    def salvar(self):
        os.makedirs(self.diretorio_saida, exist_ok=True)
        caminho_hipoteses = os.path.join(self.diretorio_saida, 'hipoteses.csv')
        caminho_verdade = os.path.join(self.diretorio_saida, 'verdade.csv')
        caminho_robo = os.path.join(self.diretorio_saida, 'robo.csv')
        self.gravador.salvar(caminho_hipoteses, caminho_verdade, caminho_robo)
        self.get_logger().info(
            f'Gravado: {len(self.gravador.hipoteses)} linhas de hipotese, '
            f'{len(self.gravador.verdade)} linhas de verdade, '
            f'{len(self.gravador.robo)} linhas de pose do robo -> '
            f'{caminho_hipoteses}, {caminho_verdade}, {caminho_robo}')
        return caminho_hipoteses, caminho_verdade, caminho_robo


def main(args=None):
    rclpy.init(args=args)
    node = GravadorAtoresNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.salvar()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
