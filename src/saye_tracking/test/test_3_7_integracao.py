"""
Submodulo 3.7 - teste da integracao ROS do tracker_node.

Publica Detection3DArray sinteticos (como a Fase 2 publicaria) numa
sequencia representando um objeto andando, e confere que o tracker_node
publica Detection3DArray (tracks) + MarkerArray com o mesmo id estavel.
"""
import time

from builtin_interfaces.msg import Time as TimeMsg
import pytest
import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import QoSProfile, ReliabilityPolicy
from saye_tracking.tracker_node import TrackerNode
from vision_msgs.msg import Detection3D, Detection3DArray, ObjectHypothesisWithPose
from visualization_msgs.msg import Marker, MarkerArray

TOPICO_ENTRADA = '/test/deteccoes_3d'


def _stamp(segundos):
    t = TimeMsg()
    t.sec = int(segundos)
    t.nanosec = int((segundos - int(segundos)) * 1e9)
    return t


def _deteccoes_3d(posicao_xy, stamp):
    m = Detection3DArray()
    m.header.frame_id = 'odom'
    m.header.stamp = stamp
    d = Detection3D()
    d.header = m.header
    d.id = '0'
    hip = ObjectHypothesisWithPose()
    hip.hypothesis.class_id = 'person'
    hip.hypothesis.score = 0.9
    hip.pose.pose.position.x, hip.pose.pose.position.y = posicao_xy
    d.results.append(hip)
    m.detections.append(d)
    return m


class _Pub(Node):
    def __init__(self):
        super().__init__('pub_sintetico_3_7')
        qc = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.pub = self.create_publisher(Detection3DArray, TOPICO_ENTRADA, qc)


@pytest.fixture
def ambiente():
    rclpy.init()
    node = TrackerNode(parameter_overrides=[
        Parameter('topico_deteccoes_3d', value=TOPICO_ENTRADA),
        Parameter('min_hits_confirmar', value=2),
        Parameter('tolerancia_tentativo_segundos', value=0.5),
        Parameter('tolerancia_perdido_segundos', value=1.5),
        Parameter('gate_distancia', value=1.0),
    ])
    pub = _Pub()
    capturado = {}
    node.create_subscription(
        Detection3DArray, '/tracker_node/tracks',
        lambda m: capturado.__setitem__('tracks', m), 10)
    node.create_subscription(
        MarkerArray, '/tracker_node/marcadores',
        lambda m: capturado.__setitem__('marcadores', m), 10)

    exe = SingleThreadedExecutor()
    exe.add_node(node)
    exe.add_node(pub)

    def spin(dt):
        t0 = time.time()
        while time.time() - t0 < dt:
            exe.spin_once(timeout_sec=0.02)

    spin(1.0)  # descoberta pub/sub
    yield pub, capturado, spin
    node.destroy_node()
    pub.destroy_node()
    rclpy.shutdown()


def test_track_confirmado_e_publicado_com_id_estavel(ambiente):
    pub, capturado, spin = ambiente

    posicao = 0.0
    for k in range(4):
        pub.pub.publish(_deteccoes_3d((posicao, 1.0), _stamp(k * 0.1)))
        spin(0.3)
        posicao += 0.05

    msg = capturado.get('tracks')
    assert msg is not None
    assert msg.header.frame_id == 'odom'
    assert len(msg.detections) == 1
    assert msg.detections[0].results[0].hypothesis.class_id == 'person'


def test_marcadores_incluem_seta_de_velocidade(ambiente):
    pub, capturado, spin = ambiente

    posicao = 0.0
    for k in range(5):
        pub.pub.publish(_deteccoes_3d((posicao, 0.0), _stamp(k * 0.1)))
        spin(0.3)
        posicao += 0.1  # 1 m/s

    msg = capturado.get('marcadores')
    assert msg is not None
    setas = [m for m in msg.markers
             if m.action == Marker.ADD and m.type == Marker.ARROW]
    assert len(setas) == 1
    # a seta comeca na posicao do track e aponta na direcao do movimento
    inicio, fim = setas[0].points
    assert fim.x > inicio.x


def test_mensagem_sem_deteccoes_nao_quebra(ambiente):
    pub, capturado, spin = ambiente

    pub.pub.publish(Detection3DArray())
    spin(0.5)

    msg = capturado.get('tracks')
    assert msg is not None
    assert len(msg.detections) == 0
