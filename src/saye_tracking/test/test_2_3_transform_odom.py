"""
Submodulo 2.3 - teste da transformacao camera -> odom.

Insere transforms conhecidos direto no buffer tf2 (sem publicar/assinar) e
confere se `transformar_para_odom` aplica translacao e rotacao corretamente,
e se retorna None quando o TF nao existe.
"""
from builtin_interfaces.msg import Time as TimeMsg
from geometry_msgs.msg import TransformStamped
import numpy as np
import pytest
import rclpy
from saye_tracking.projecao3d_node import Projecao3DNode

CARIMBO = TimeMsg(sec=100, nanosec=0)


def _transform(frame_pai, frame_filho, t=(0.0, 0.0, 0.0), q=(0.0, 0.0, 0.0, 1.0)):
    ts = TransformStamped()
    ts.header.frame_id = frame_pai
    ts.header.stamp = CARIMBO
    ts.child_frame_id = frame_filho
    ts.transform.translation.x, ts.transform.translation.y, ts.transform.translation.z = t
    (ts.transform.rotation.x, ts.transform.rotation.y,
     ts.transform.rotation.z, ts.transform.rotation.w) = q
    return ts


@pytest.fixture
def node():
    rclpy.init()
    n = Projecao3DNode()
    yield n
    n.destroy_node()
    rclpy.shutdown()


def test_translacao_pura(node):
    node.tf_buffer.set_transform_static(
        _transform('odom', 'cam', t=(1.0, 2.0, 0.5)), 'teste')

    resultado = node.transformar_para_odom(
        np.array([0.3, 0.0, 0.0]), 'cam', CARIMBO)

    np.testing.assert_allclose(resultado, [1.3, 2.0, 0.5], atol=1e-6)


def test_rotacao_90_graus_em_z(node):
    # quaternion de 90 graus em torno de Z: (0, 0, sin45, cos45)
    q = (0.0, 0.0, 0.70710678, 0.70710678)
    node.tf_buffer.set_transform_static(
        _transform('odom', 'cam', t=(0.0, 0.0, 0.0), q=q), 'teste')

    # ponto "1 metro a frente da camera" -> apos girar 90 graus, deve virar
    # "1 metro para o eixo Y do odom"
    resultado = node.transformar_para_odom(
        np.array([1.0, 0.0, 0.0]), 'cam', CARIMBO)

    np.testing.assert_allclose(resultado, [0.0, 1.0, 0.0], atol=1e-6)


def test_translacao_e_rotacao_combinadas(node):
    q = (0.0, 0.0, 0.70710678, 0.70710678)  # 90 graus em Z
    node.tf_buffer.set_transform_static(
        _transform('odom', 'cam', t=(5.0, -1.0, 0.2), q=q), 'teste')

    resultado = node.transformar_para_odom(
        np.array([1.0, 0.0, 0.0]), 'cam', CARIMBO)

    # gira (1,0,0) -> (0,1,0), depois soma a translacao
    np.testing.assert_allclose(resultado, [5.0, 0.0, 0.2], atol=1e-6)


def test_tf_inexistente_retorna_none(node):
    resultado = node.transformar_para_odom(
        np.array([1.0, 0.0, 0.0]), 'frame_que_nao_existe', CARIMBO)

    assert resultado is None
