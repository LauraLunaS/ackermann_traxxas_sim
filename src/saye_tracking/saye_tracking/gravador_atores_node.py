"""
No gravador para atores andando.

Submodulo 4.9 - bancada de avaliacao multi-pessoa. Igual ao
`gravador_node.py` (4.1) do lado das HIPOTESES (assina
`/tracker_node/tracks`); o lado da VERDADE le a posicao REAL de cada ator
de volta do Gazebo (ver "Verdade dos ATORES" mais abaixo - secao reescrita
na correcao da bancada, que trocou calculo pela formula por leitura
medida).

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

Verdade dos ATORES: desde a correcao da bancada (ver achado completo em
`gz_pose_vector.py` - o antigo `mover_pessoa_animada_node` tinha 1 processo
por ator chamando `set_pose` concorrentemente, e uma falha silenciosa podia
deixar um ator parado sem que nada avisasse), a verdade NAO E MAIS a
posicao calculada pela formula (`verdade_atores.posicoes_verdadeiras`) -
e a posicao REAL/MEDIDA, lida de volta do Gazebo via gz-transport
(topico `/world/<mundo>/pose/info`, mensagem nativa `gz.msgs.Pose_V`, que
- diferente da ponte `ros_gz_bridge` pra `tf2_msgs/TFMessage` usada no
`gravador_node`/4.1 - preserva o campo `name` de cada pose, entao da pra
buscar por NOME em vez de indice fragil).

Achado (ao implementar isto): a 1a versao tentou calcular qual quadro
DEVERIA estar ativo agora com a mesma formula do mover
(`verdade_atores.nome_quadro_ativo`) e so entao ler a pose REAL daquele
nome especifico - testado ao vivo, resultado: verdade.csv gravado 100%
como (0, 0) do inicio ao fim. Causa: esse gravador conta ticks PROPRIOS a
partir de QUANDO ELE SOBE (ver nota de sincronizacao acima), defasado do
tick do mover por ~1-2s (tempo de assentamento da bancada) - e um ciclo
INTEIRO do flipbook (todos os N quadros) dura so ~1s (`comprimento_passada`
/ `velocidade` ≈ 0.3/0.3 ≈ 1s). Pra POSICAO continua isso daria so um erro
pequeno e aceitavel (a pessoa anda pouco em 1-2s) - mas pra escolher QUAL
QUADRO olhar, 1-2s de defasagem pode apontar pra QUALQUER quadro do ciclo,
quase sempre um que esta ESTACIONADO (`z=-50`, logo x=y=0) nesse instante,
nao o que esta ativo de verdade. Ou seja: calcular o nome e olhar DEPOIS
reintroduz a mesma fragilidade de sincronizacao que estavamos corrigindo.

Solucao: em vez de CALCULAR qual quadro deveria estar ativo, DETECTA direto
dos dados medidos - dentre os N nomes de quadro de um ator, o ativo e o
(no maximo 1) que NAO esta em `z` perto de -50. Nao depende de nenhuma
sincronizacao de tick entre mover e gravador - so do que o Gazebo
realmente reportou agora.
"""
import math
import os

from gz.msgs10.pose_v_pb2 import Pose_V
from gz.transport13 import Node as NodeGz
from nav_msgs.msg import Odometry
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from saye_tracking.gravador import Gravador
from std_srvs.srv import Trigger
from vision_msgs.msg import Detection3DArray
import yaml

# acima disto = quadro ativo (ver Z_ESTACIONADO em mover_pessoas_node.py)
Z_ESTACIONADO_LIMIAR = -40.0


class GravadorAtoresNode(Node):
    """Fase 4.9 - grava hipoteses do tracker vs verdade REAL/medida de N atores andando."""

    def __init__(self, **kwargs):
        super().__init__('gravador_atores_node', **kwargs)

        self.declare_parameter('topico_tracks', '/tracker_node/tracks')
        self.declare_parameter('topico_odom', '/odom')
        self.declare_parameter('mundo', 'beach_world')
        self.declare_parameter('atores_yaml', '')
        self.declare_parameter('nomes_atores', [''])  # subconjunto de atores_yaml a usar
        self.declare_parameter('taxa_verdade_hz', 20.0)
        self.declare_parameter('diretorio_saida', '/tmp/saye_tracking_gravacao_atores')

        topico_tracks = self.get_parameter('topico_tracks').value
        topico_odom = self.get_parameter('topico_odom').value
        mundo = self.get_parameter('mundo').value
        caminho_yaml = self.get_parameter('atores_yaml').value
        nomes_desejados = set(self.get_parameter('nomes_atores').value)
        self.taxa_verdade_hz = float(self.get_parameter('taxa_verdade_hz').value)
        self.diretorio_saida = self.get_parameter('diretorio_saida').value

        with open(caminho_yaml, encoding='utf-8') as f:
            todos_atores = yaml.safe_load(f)['atores']
        self.atores = [a for a in todos_atores if a['nome'] in nomes_desejados]
        if not self.atores:
            raise ValueError(
                f'nenhum ator de {nomes_desejados} encontrado em {caminho_yaml}')

        self.gravador = Gravador()

        # pose REAL dos atores (ver nota no topo do arquivo) - gz-transport
        # direto, NAO ros_gz_bridge (precisa do campo `name`, que a ponte
        # pra tf2_msgs descarta). {nome_do_quadro: (x, y, z)}, atualizado a
        # cada mensagem de `/world/<mundo>/pose/info`.
        self.pose_real_por_nome = {}
        self.nomes_quadros_por_ator = {
            a['nome']: [f"{a['prefixo_modelo']}{i}" for i in range(int(a['n_quadros']))]
            for a in self.atores
        }
        self.topico_pose_gz = f'/world/{mundo}/pose/info'
        self.no_gz = NodeGz()
        self.no_gz.subscribe(Pose_V, self.topico_pose_gz, self._callback_pose_gz)
        self._avisou_pose_ausente = set()  # nao repetir o mesmo aviso todo tick

        qos_confiavel = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.sub_tracks = self.create_subscription(
            Detection3DArray, topico_tracks, self.callback_tracks, qos_confiavel)
        self.sub_odom = self.create_subscription(
            Odometry, topico_odom, self.callback_odom, qos_confiavel)

        self.timer_verdade = self.create_timer(1.0 / self.taxa_verdade_hz, self._callback_verdade)

        self.srv_salvar = self.create_service(Trigger, '~/salvar', self.callback_salvar)

        self.get_logger().info(
            f'gravador_atores_node iniciado (4.9, verdade MEDIDA pos-correcao). '
            f'Hipoteses de "{topico_tracks}", verdade real de '
            f'{[a["nome"] for a in self.atores]} via "{self.topico_pose_gz}". '
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

    def _callback_pose_gz(self, msg: Pose_V):
        # roda na thread interna do gz-transport, nao na do rclpy - so
        # substitui entradas de um dict, sem lock (GIL cobre essa troca
        # simples; o pior caso e ler um valor 1 msg "atrasado", irrelevante
        # a 20Hz de verdade vs. a taxa bem mais alta deste topico).
        for p in msg.pose:
            self.pose_real_por_nome[p.name] = (p.position.x, p.position.y, p.position.z)

    def callback_odom(self, msg: Odometry):
        tempo = self.get_clock().now().nanoseconds * 1e-9
        if tempo <= 0.0:
            return  # relogio de sim ainda nao sincronizou (ver nota acima)
        pos = msg.pose.pose.position
        q = msg.pose.pose.orientation
        yaw = math.atan2(2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y * q.y + q.z * q.z))
        self.gravador.registrar_robo(tempo, pos.x, pos.y, yaw)

    def _callback_verdade(self):
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
        for ator in self.atores:
            pose = self._pose_ativa_medida(ator['nome'])
            if pose is None:
                # ou nenhuma msg de pose/info chegou ainda (normal nos 1os
                # instantes - subscricao gz-transport e assincrona), ou
                # nenhum quadro deste ator esta "ativo" agora (ex.: estado
                # transitorio de 1 unico tick entre o teleporte do quadro
                # novo e o estacionamento do antigo). Pula a amostra em vez
                # de inventar uma posicao - se persistir por muitos ticks,
                # e sinal real de problema, por isso avisa (1x por ator).
                if ator['nome'] not in self._avisou_pose_ausente:
                    self._avisou_pose_ausente.add(ator['nome'])
                    self.get_logger().warn(
                        f'nenhum quadro ATIVO de "{ator["nome"]}" encontrado em '
                        f'"{self.topico_pose_gz}" ainda - pulando amostra(s) de '
                        f'verdade dele ate aparecer um.')
                continue
            x, y = pose
            self.gravador.registrar_verdade(tempo_sim, ator['nome'], x, y)

    def _pose_ativa_medida(self, nome_ator):
        """Dentre os quadros de `nome_ator`, devolve (x, y) do que NAO esta estacionado."""
        for nome_quadro in self.nomes_quadros_por_ator[nome_ator]:
            pose = self.pose_real_por_nome.get(nome_quadro)
            if pose is not None and pose[2] > Z_ESTACIONADO_LIMIAR:
                return pose[0], pose[1]
        return None

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
