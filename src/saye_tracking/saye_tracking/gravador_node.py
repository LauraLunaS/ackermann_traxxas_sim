"""
No gravador (submodulo 4.1 da Fase 4 - bancada de avaliacao).

Liga o `Gravador` (submodulo 4.1, puro Python) aos topicos ROS de verdade:
  - hipoteses: assina `/tracker_node/tracks` (saida da Fase 3, frame `odom`).
  - verdade: assina um topico `tf2_msgs/msg/TFMessage` com a pose real dos
    objetos no Gazebo (ground truth), filtrando por indice (ver abaixo).

Achado 1 (verificado ao vivo antes de implementar): nesta simulacao o frame
`odom` do robo e IDENTICO ao frame `world` do Gazebo - `/odom` publica a
mesma posicao que a pose real do robo no mundo, sem deslocamento nem
rotacao (spawn em yaw=0). Por isso a verdade pode ser lida direto do
Gazebo (`/world/<mundo>/pose/info`, que inclui ate objetos estaticos) e
comparada com a saida do tracker sem nenhuma transformacao de frame.

Achado 2 (limitacao do `ros_gz_bridge` nesta versao, ja conhecida desde o
2.5/3.8 - ver README): a conversao `gz.msgs.Pose_V` -> `tf2_msgs/TFMessage`
NAO preenche `child_frame_id` (fica sempre `''`) nem o timestamp de cada
transform (fica sempre zero) - so a ORDEM e a posicao vem corretas.
Por isso a verdade e identificada por INDICE dentro da lista (nao por
nome). O indice de cada objeto e a posicao dele na ordem de declaracao dos
`<model>`/`<include>` de nivel 1 no `simple_world.sdf`: 0=sandy_terrain,
1=pessoa_detectavel, 2=dynamic_obstacle_sphere, 3=...box, 4=...cylinder,
5=traxxas (confirmado lendo `gz topic -e -t /world/beach_world/pose/info`
lado a lado com o topico bridgeado).

Achado 3 (achado no 4.3, impacto maior do que o registrado no 4.1/4.2):
o `header.stamp` que sai do `deteccao_node` (propagado da camera, ver
[[env-gpu-sim]] no README) fica com timestamp de relogio de parede boa
parte do tempo - em cenarios com o robo se movendo, chegou a **98% das
mensagens** perdidas por esse motivo, o suficiente pra esvaziar quase toda
a gravacao. Por isso NENHUM dos dois lados usa o timestamp vindo da
mensagem: tanto hipotese quanto verdade usam `self.get_clock().now()` (o
relogio do proprio `gravador_node`, sincronizado com `/clock` via
`use_sim_time:=true`) no instante em que a mensagem CHEGA - o atraso de
processamento do pipeline inteiro (deteccao->projecao3d->tracker) e
pequeno (dezenas de ms) comparado ao `tamanho_frame_segundos` usado no
comparador (4.2, padrao 0.1s), entao nao atrapalha a sincronizacao.

Para gerar o topico de verdade, faca a ponte Gazebo->ROS (nome do mundo e
"beach_world" no `simple_world.sdf`):

    ros2 run ros_gz_bridge parameter_bridge \
        /world/beach_world/pose/info@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V \
        --ros-args -r /world/beach_world/pose/info:=/gt/pose_info

Ao final (Ctrl+C ou `ros2 service call ~/salvar std_srvs/srv/Trigger`),
salva `hipoteses.csv` e `verdade.csv` no diretorio de saida.
"""
import os

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from saye_tracking.gravador import Gravador
from std_srvs.srv import Trigger
from tf2_msgs.msg import TFMessage
from vision_msgs.msg import Detection3DArray


class GravadorNode(Node):
    """Fase 4.1 - grava hipoteses do tracker e verdade do Gazebo em CSV."""

    def __init__(self, **kwargs):
        super().__init__('gravador_node', **kwargs)

        self.declare_parameter('topico_tracks', '/tracker_node/tracks')
        self.declare_parameter('topico_verdade', '/gt/pose_info')
        self.declare_parameter('indices_verdade', [1])
        self.declare_parameter('nomes_verdade', ['pessoa_detectavel'])
        self.declare_parameter('diretorio_saida', '/tmp/saye_tracking_gravacao')

        topico_tracks = self.get_parameter('topico_tracks').value
        topico_verdade = self.get_parameter('topico_verdade').value
        indices = [int(i) for i in self.get_parameter('indices_verdade').value]
        nomes = self.get_parameter('nomes_verdade').value
        self.nome_por_indice = dict(zip(indices, nomes))
        self.diretorio_saida = self.get_parameter('diretorio_saida').value

        self.gravador = Gravador()

        qos_confiavel = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.sub_tracks = self.create_subscription(
            Detection3DArray, topico_tracks, self.callback_tracks, qos_confiavel)
        self.sub_verdade = self.create_subscription(
            TFMessage, topico_verdade, self.callback_verdade, 10)

        self.srv_salvar = self.create_service(Trigger, '~/salvar', self.callback_salvar)

        self.get_logger().info(
            f'gravador_node iniciado (4.1). Hipoteses de "{topico_tracks}", '
            f'verdade de "{topico_verdade}" (indices={self.nome_por_indice}). '
            f'Ctrl+C ou servico "~/salvar" grava em "{self.diretorio_saida}".')

    # ------------------------------------------------------------------
    def callback_tracks(self, msg: Detection3DArray):
        # ver "Achado 3" no topo do arquivo: nao usa msg.header.stamp
        # (propagado da camera, contaminado com relogio de parede boa
        # parte do tempo) - usa o instante de chegada no proprio no.
        tempo = self.get_clock().now().nanoseconds * 1e-9
        for d in msg.detections:
            if not d.results:
                continue
            pos = d.results[0].pose.pose.position
            self.gravador.registrar_hipotese(tempo, d.id, pos.x, pos.y)

    def callback_verdade(self, msg: TFMessage):
        # ver "Achado 2" no topo do arquivo: a ponte nao preenche nome nem
        # timestamp por transform, so a ordem e a posicao sao confiaveis.
        tempo = self.get_clock().now().nanoseconds * 1e-9
        for indice, nome in self.nome_por_indice.items():
            if indice >= len(msg.transforms):
                continue
            t = msg.transforms[indice].transform.translation
            self.gravador.registrar_verdade(tempo, nome, t.x, t.y)

    # ------------------------------------------------------------------
    def callback_salvar(self, request, response):
        caminhos = self.salvar()
        response.success = True
        response.message = f'gravado em {caminhos[0]} e {caminhos[1]}'
        return response

    def salvar(self):
        os.makedirs(self.diretorio_saida, exist_ok=True)
        caminho_hipoteses = os.path.join(self.diretorio_saida, 'hipoteses.csv')
        caminho_verdade = os.path.join(self.diretorio_saida, 'verdade.csv')
        self.gravador.salvar(caminho_hipoteses, caminho_verdade)
        self.get_logger().info(
            f'Gravado: {len(self.gravador.hipoteses)} linhas de hipotese, '
            f'{len(self.gravador.verdade)} linhas de verdade -> '
            f'{caminho_hipoteses}, {caminho_verdade}')
        return caminho_hipoteses, caminho_verdade


def main(args=None):
    rclpy.init(args=args)
    node = GravadorNode()
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
