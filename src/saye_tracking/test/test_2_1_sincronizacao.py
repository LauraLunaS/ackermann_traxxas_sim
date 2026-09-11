"""
Submodulo 2.1 - teste da sincronizacao de entradas do projecao3d_node.

Publica Detection2DArray + Image(mono8) + PointCloud2 sinteticos em topicos
isolados (/test/*) com stamps controlados e confere se o ApproximateTime
casa os conjuntos certos e rejeita os errados.
"""
import struct
import time

from builtin_interfaces.msg import Time as TimeMsg
import pytest
import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import qos_profile_sensor_data, QoSProfile, ReliabilityPolicy
from saye_tracking.projecao3d_node import Projecao3DNode
from sensor_msgs.msg import Image, PointCloud2, PointField
from std_msgs.msg import Header
from vision_msgs.msg import (
    BoundingBox2D,
    Detection2D,
    Detection2DArray,
    ObjectHypothesisWithPose,
)

W, H = 32, 24
TD, TM, TN = '/test/deteccoes', '/test/mascaras', '/test/points'


def _stamp(sec, nsec=0):
    t = TimeMsg()
    t.sec = int(sec)
    t.nanosec = int(nsec)
    return t


def _hdr(s):
    h = Header()
    h.stamp = s
    h.frame_id = 'traxxas/base_link/realsense_d435'
    return h


def _dets(s, n=2):
    m = Detection2DArray()
    m.header = _hdr(s)
    for i in range(n):
        d = Detection2D()
        d.header = m.header
        d.id = str(i)
        b = BoundingBox2D()
        b.center.position.x = 10.0 * (i + 1)
        b.center.position.y = 20.0
        b.size_x, b.size_y = 8.0, 16.0
        d.bbox = b
        hp = ObjectHypothesisWithPose()
        hp.hypothesis.class_id = 'person'
        hp.hypothesis.score = 0.9
        d.results.append(hp)
        m.detections.append(d)
    return m


def _mask(s):
    m = Image()
    m.header = _hdr(s)
    m.height, m.width, m.encoding, m.step = H, W, 'mono8', W
    m.data = bytes(W * H)
    return m


def _cloud(s):
    m = PointCloud2()
    m.header = _hdr(s)
    m.height, m.width = H, W
    m.fields = [
        PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
        PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
        PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
    ]
    m.is_bigendian = False
    m.point_step = 12
    m.row_step = 12 * W
    m.is_dense = True
    m.data = struct.pack('fff', 1.0, 2.0, 3.0) * (W * H)
    return m


class _Pub(Node):
    def __init__(self):
        super().__init__('pub_sintetico_2_1')
        qc = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.pd = self.create_publisher(Detection2DArray, TD, qc)
        self.pm = self.create_publisher(Image, TM, qos_profile_sensor_data)
        self.pn = self.create_publisher(PointCloud2, TN, qos_profile_sensor_data)


@pytest.fixture
def ambiente():
    rclpy.init()
    node = Projecao3DNode(parameter_overrides=[
        Parameter('topico_deteccoes', value=TD),
        Parameter('topico_mascaras', value=TM),
        Parameter('topico_nuvem', value=TN),
    ])
    pub = _Pub()
    contador = {'n': 0}
    node.sync.registerCallback(
        lambda *a: contador.__setitem__('n', contador['n'] + 1))
    exe = SingleThreadedExecutor()
    exe.add_node(node)
    exe.add_node(pub)

    def spin(dt):
        t0 = time.time()
        while time.time() - t0 < dt:
            exe.spin_once(timeout_sec=0.02)

    spin(2.0)  # descoberta pub/sub
    yield node, pub, contador, spin
    node.destroy_node()
    pub.destroy_node()
    rclpy.shutdown()


def _roda(pub, contador, spin, triplas):
    contador['n'] = 0
    for sd, sm, sn in triplas:
        if sd is not None:
            pub.pd.publish(_dets(sd))
        if sm is not None:
            pub.pm.publish(_mask(sm))
        if sn is not None:
            pub.pn.publish(_cloud(sn))
        spin(0.3)
    return contador['n']


def test_stamps_identicos_casam(ambiente):
    _, pub, contador, spin = ambiente
    n = _roda(pub, contador, spin,
              [(_stamp(100 + k), _stamp(100 + k), _stamp(100 + k)) for k in range(5)])
    assert n == 5


def test_dentro_do_slop_casa(ambiente):
    _, pub, contador, spin = ambiente
    n = _roda(pub, contador, spin,
              [(_stamp(200 + k, 0), _stamp(200 + k, 30_000_000),
                _stamp(200 + k, 15_000_000)) for k in range(5)])
    assert n == 5


def test_fora_do_slop_nao_casa(ambiente):
    _, pub, contador, spin = ambiente
    n = _roda(pub, contador, spin,
              [(_stamp(300 + k, 0), _stamp(300 + k, 0),
                _stamp(300 + k - 1, 500_000_000)) for k in range(5)])
    assert n == 0


def test_entrada_faltando_nao_casa(ambiente):
    _, pub, contador, spin = ambiente
    n = _roda(pub, contador, spin,
              [(_stamp(400 + k), _stamp(400 + k), None) for k in range(5)])
    assert n == 0
