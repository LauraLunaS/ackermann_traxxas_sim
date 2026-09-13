"""
Submodulo 2.4 - teste da publicacao de Detection3DArray e MarkerArray.

Chama os metodos de publicacao diretamente (sem sincronizador) com uma
lista de deteccoes "ja processadas" e confere o conteudo das mensagens
que saem nos topicos ~/deteccoes_3d e ~/marcadores.
"""
from builtin_interfaces.msg import Time as TimeMsg
import numpy as np
import pytest
import rclpy
from rclpy.executors import SingleThreadedExecutor
from saye_tracking.projecao3d_node import Projecao3DNode
from vision_msgs.msg import Detection3DArray
from visualization_msgs.msg import Marker, MarkerArray

CARIMBO = TimeMsg(sec=42, nanosec=0)


@pytest.fixture
def ambiente():
    rclpy.init()
    node = Projecao3DNode()
    capturado = {}
    node.create_subscription(
        Detection3DArray, '/projecao3d_node/deteccoes_3d',
        lambda m: capturado.__setitem__('det3d', m), 10)
    node.create_subscription(
        MarkerArray, '/projecao3d_node/marcadores',
        lambda m: capturado.__setitem__('marcadores', m), 10)

    exe = SingleThreadedExecutor()
    exe.add_node(node)

    def spin(dt=1.0):
        import time
        t0 = time.time()
        while time.time() - t0 < dt:
            exe.spin_once(timeout_sec=0.02)

    spin(1.0)  # descoberta pub/sub
    yield node, capturado, spin
    node.destroy_node()
    rclpy.shutdown()


def test_detection3darray_tem_posicao_classe_e_bbox_certos(ambiente):
    node, capturado, spin = ambiente
    processadas = [('3', 'person', 0.87, np.array([1.0, 2.0, 0.3]))]

    node.publicar_deteccoes_3d(CARIMBO, processadas)
    spin(1.0)

    msg = capturado.get('det3d')
    assert msg is not None
    assert msg.header.frame_id == 'odom'
    assert len(msg.detections) == 1

    d = msg.detections[0]
    assert d.id == '3'
    assert d.results[0].hypothesis.class_id == 'person'
    assert d.results[0].hypothesis.score == pytest.approx(0.87)
    np.testing.assert_allclose(
        [d.results[0].pose.pose.position.x,
         d.results[0].pose.pose.position.y,
         d.results[0].pose.pose.position.z],
        [1.0, 2.0, 0.3])
    # tamanho de bbox conhecido para "person" (ver TAMANHOS_BBOX)
    assert d.bbox.size.z == pytest.approx(1.7)


def test_detection3darray_vazio_quando_nao_ha_deteccoes(ambiente):
    node, capturado, spin = ambiente
    node.publicar_deteccoes_3d(CARIMBO, [])
    spin(1.0)

    msg = capturado.get('det3d')
    assert msg is not None
    assert len(msg.detections) == 0


def test_classe_desconhecida_usa_tamanho_padrao(ambiente):
    node, capturado, spin = ambiente
    processadas = [('0', 'bicycle', 0.5, np.array([0.0, 0.0, 0.0]))]

    node.publicar_deteccoes_3d(CARIMBO, processadas)
    spin(1.0)

    d = capturado['det3d'].detections[0]
    assert (d.bbox.size.x, d.bbox.size.y, d.bbox.size.z) == (0.5, 0.5, 1.0)


def test_marcadores_tem_deleteall_mais_esfera_e_texto_por_deteccao(ambiente):
    node, capturado, spin = ambiente
    processadas = [
        ('0', 'person', 0.9, np.array([1.0, 0.0, 0.0])),
        ('1', 'person', 0.8, np.array([2.0, 0.0, 0.0])),
    ]

    node.publicar_marcadores(CARIMBO, processadas)
    spin(1.0)

    msg = capturado.get('marcadores')
    assert msg is not None
    # 1 DELETEALL + (1 esfera + 1 texto) por deteccao
    assert len(msg.markers) == 1 + 2 * len(processadas)
    assert msg.markers[0].action == Marker.DELETEALL

    esferas = [m for m in msg.markers if m.type == Marker.SPHERE]
    textos = [m for m in msg.markers if m.type == Marker.TEXT_VIEW_FACING]
    assert len(esferas) == 2
    assert len(textos) == 2
    assert '#0' in textos[0].text or '#1' in textos[0].text


def test_marcadores_so_deleteall_quando_sem_deteccoes(ambiente):
    node, capturado, spin = ambiente
    node.publicar_marcadores(CARIMBO, [])
    spin(1.0)

    msg = capturado.get('marcadores')
    assert msg is not None
    assert len(msg.markers) == 1
    assert msg.markers[0].action == Marker.DELETEALL
