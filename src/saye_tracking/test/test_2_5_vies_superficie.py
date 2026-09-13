"""
Submodulo 2.5 - caracteriza o vies geometrico da extracao 3D.

Um sensor de profundidade so ve a face voltada pra ele: a mediana dos pontos
de uma deteccao fica perto da SUPERFICIE mais proxima da camera, nao do
CENTRO do objeto. Para um objeto de raio R (ex.: uma pessoa vista de frente,
ombro a ombro, tem uma "espessura" na direcao da camera), o vies esperado e
de aproximadamente R na direcao da camera.

Este teste fabrica uma nuvem sintetica com uma calota esferica visivel (so
os pontos da face voltada pra camera, o resto e +inf - como o sensor real)
e confere que `extrair_ponto_3d` reproduz esse vies de forma previsivel,
para que o comportamento fique documentado e qualquer mudanca futura no
metodo de agregacao (ex.: trocar mediana por outra estatistica) seja
avaliada contra esse comportamento conhecido.
"""
import numpy as np
import pytest
import rclpy
from saye_tracking.projecao3d_node import Projecao3DNode
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header

RESOLUCAO_ANGULAR = 60  # pontos por eixo na grade da calota
W = H = RESOLUCAO_ANGULAR


def _nuvem_calota_esferica(centro_xyz, raio, fov_graus=60):
    """
    Fabrica uma nuvem organizada com uma calota esferica visivel de um lado.

    Todos os pontos fora da calota (ou fora do FOV) ficam +inf, como um
    sensor real ve so a face voltada pra ele.
    """
    centro = np.array(centro_xyz, dtype=np.float64)
    dist_centro = np.linalg.norm(centro)
    dir_camera = -centro / dist_centro  # da esfera para a camera

    # base ortonormal com dir_camera como eixo principal do cone
    if abs(dir_camera[2]) < 0.9:
        referencia = np.array([0.0, 0.0, 1.0])
    else:
        referencia = np.array([1.0, 0.0, 0.0])
    e1 = np.cross(dir_camera, referencia)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(dir_camera, e1)

    pontos = np.full((H, W, 3), np.inf, dtype=np.float32)
    meia_faixa = np.radians(fov_graus / 2)
    thetas = np.linspace(-meia_faixa, meia_faixa, H)
    phis = np.linspace(-meia_faixa, meia_faixa, W)

    for i, th in enumerate(thetas):
        for j, ph in enumerate(phis):
            # direcao num cone em torno de dir_camera (a face voltada p/ a camera)
            direcao = (np.cos(th) * np.cos(ph) * dir_camera
                       + np.sin(ph) * e1 + np.sin(th) * e2)
            direcao /= np.linalg.norm(direcao)
            if np.dot(direcao, dir_camera) > 0.3:
                ponto = centro + raio * direcao
                pontos[i, j] = ponto

    m = PointCloud2()
    m.header = Header()
    m.header.frame_id = 'traxxas/base_link/realsense_d435'
    m.height, m.width = H, W
    m.fields = [
        PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
        PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
        PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
    ]
    m.is_bigendian = False
    m.point_step = 12
    m.row_step = 12 * W
    m.is_dense = False
    m.data = pontos.tobytes()
    return m, np.isfinite(pontos).all(axis=2)


@pytest.fixture
def node():
    rclpy.init()
    n = Projecao3DNode(parameter_overrides=[])
    n.min_pixels_mascara = 10
    n.min_pixels_validos = 5
    yield n
    n.destroy_node()
    rclpy.shutdown()


def test_mediana_fica_na_superficie_nao_no_centro(node):
    centro = np.array([3.0, 0.0, 0.0])
    raio = 0.4
    nuvem, mascara_visivel = _nuvem_calota_esferica(centro, raio)
    mascara = mascara_visivel.astype(np.uint8)  # 1 onde a calota e visivel

    resultado = node.extrair_ponto_3d(nuvem, mascara, indice_deteccao=0)

    assert resultado is not None
    posicao, *_ = resultado

    distancia_ao_centro = np.linalg.norm(posicao - centro)
    # a mediana da calota visivel fica proxima da superficie, nao do centro:
    # a distancia ao centro deve ser proxima do raio (nao de zero)
    assert distancia_ao_centro == pytest.approx(raio, abs=0.15)

    # e deve estar do lado da camera (mais perto da origem que o centro)
    assert np.linalg.norm(posicao) < np.linalg.norm(centro)


def test_correcao_pelo_raio_aproxima_do_centro_real(node):
    """A correcao usada na validacao de ground truth (2.5) deve reduzir o erro."""
    centro = np.array([4.0, 1.0, 0.0])
    raio = 0.3
    nuvem, mascara_visivel = _nuvem_calota_esferica(centro, raio)
    mascara = mascara_visivel.astype(np.uint8)

    resultado = node.extrair_ponto_3d(nuvem, mascara, indice_deteccao=0)
    posicao, *_ = resultado

    erro_sem_correcao = np.linalg.norm(posicao - centro)

    # correcao: soma de volta o raio na direcao de onde veio a medicao
    dist = np.linalg.norm(posicao)
    direcao_normalizada = posicao / dist
    posicao_corrigida = posicao + raio * direcao_normalizada
    erro_com_correcao = np.linalg.norm(posicao_corrigida - centro)

    assert erro_com_correcao < erro_sem_correcao
    assert erro_com_correcao < 0.05  # poucos cm apos a correcao geometrica
