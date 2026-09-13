"""
Submodulo 3.0 - scaffold do tracker_node.

So confere que o no sobe, assina o topico certo e nao quebra ao receber
deteccoes 3D (fabricadas). Nenhuma logica de rastreamento ainda - isso
comeca no 3.1.
"""
import time

from geometry_msgs.msg import Point
import pytest
import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from saye_tracking.tracker_node import TrackerNode
from vision_msgs.msg import Detection3D, Detection3DArray, ObjectHypothesisWithPose

TOPICO = '/projecao3d_node/deteccoes_3d'


def _deteccoes(n=2):
    m = Detection3DArray()
    m.header.frame_id = 'odom'
    for i in range(n):
        d = Detection3D()
        d.id = str(i)
        hip = ObjectHypothesisWithPose()
        hip.hypothesis.class_id = 'person'
        hip.hypothesis.score = 0.9
        hip.pose.pose.position = Point(x=float(i), y=1.0, z=0.0)
        d.results.append(hip)
        m.detections.append(d)
    return m


class _Pub(Node):
    def __init__(self):
        super().__init__('pub_sintetico_3_0')
        qc = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.pub = self.create_publisher(Detection3DArray, TOPICO, qc)


@pytest.fixture
def ambiente():
    rclpy.init()
    node = TrackerNode()
    pub = _Pub()
    exe = SingleThreadedExecutor()
    exe.add_node(node)
    exe.add_node(pub)

    def spin(dt):
        t0 = time.time()
        while time.time() - t0 < dt:
            exe.spin_once(timeout_sec=0.02)

    spin(1.0)  # descoberta pub/sub
    yield node, pub, spin
    node.destroy_node()
    pub.destroy_node()
    rclpy.shutdown()


def test_no_sobe_e_conta_deteccoes_recebidas(ambiente):
    node, pub, spin = ambiente

    pub.pub.publish(_deteccoes(2))
    spin(0.5)
    pub.pub.publish(_deteccoes(3))
    spin(0.5)

    assert node.n_mensagens == 2
    assert node.n_deteccoes_total == 5


def test_mensagem_vazia_nao_quebra(ambiente):
    node, pub, spin = ambiente

    pub.pub.publish(Detection3DArray())
    spin(0.5)

    assert node.n_mensagens == 1
    assert node.n_deteccoes_total == 0
