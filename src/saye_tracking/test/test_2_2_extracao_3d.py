"""
Submodulo 2.2 - teste da extracao do ponto 3D de uma deteccao.

Constroi uma PointCloud2 sintetica (organizada, com pontos validos e
"sem-retorno" == inf, como o sensor real produz) e uma mascara de instancias,
e confere se `extrair_ponto_3d` acha a posicao certa e rejeita os casos ruins.
"""
import struct

import numpy as np
import pytest
import rclpy
from rclpy.parameter import Parameter
from saye_tracking.projecao3d_node import Projecao3DNode
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header

W, H = 10, 10


def _cloud_de(pontos_xyz: np.ndarray) -> PointCloud2:
    """pontos_xyz: array (H*W, 3) float32, ja em ordem row-major (v*W+u)."""
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
    m.data = b''.join(struct.pack('fff', *p) for p in pontos_xyz)
    return m


def _mascara_retangulo(y0, y1, x0, x1, valor=1):
    a = np.zeros((H, W), dtype=np.uint8)
    a[y0:y1, x0:x1] = valor
    return a


@pytest.fixture
def node():
    rclpy.init()
    n = Projecao3DNode(parameter_overrides=[
        Parameter('min_pixels_mascara', value=5),
        Parameter('min_pixels_validos', value=3),
    ])
    yield n
    n.destroy_node()
    rclpy.shutdown()


def test_posicao_correta_com_todos_pontos_validos(node):
    pontos = np.tile([2.0, 0.5, -0.1], (H * W, 1)).astype(np.float32)
    nuvem = _cloud_de(pontos)
    mascara = _mascara_retangulo(2, 6, 2, 6)  # 4x4 = 16 pixels

    resultado = node.extrair_ponto_3d(nuvem, mascara, indice_deteccao=0)

    assert resultado is not None
    posicao, n_mascara, n_validos = resultado
    assert n_mascara == 16
    assert n_validos == 16
    np.testing.assert_allclose(posicao, [2.0, 0.5, -0.1], atol=1e-5)


def test_mediana_ignora_pontos_invalidos(node):
    pontos = np.tile([3.0, 0.0, 0.0], (H * W, 1)).astype(np.float32)
    mascara = _mascara_retangulo(2, 6, 2, 6)  # 16 pixels na mascara
    # marca 5 desses pixels como "sem retorno" (inf), como a camera real faz
    idx_invalidos = [(2, 2), (2, 3), (3, 2), (4, 4), (5, 5)]
    pontos_2d = pontos.reshape(H, W, 3)
    for (y, x) in idx_invalidos:
        pontos_2d[y, x] = [np.inf, np.inf, np.inf]
    nuvem = _cloud_de(pontos_2d.reshape(-1, 3))

    resultado = node.extrair_ponto_3d(nuvem, mascara, indice_deteccao=0)

    assert resultado is not None
    posicao, n_mascara, n_validos = resultado
    assert n_mascara == 16
    assert n_validos == 16 - len(idx_invalidos)
    np.testing.assert_allclose(posicao, [3.0, 0.0, 0.0], atol=1e-5)


def test_mediana_resiste_a_outlier(node):
    """Um pixel de fundo vazando pra dentro da mascara nao deve puxar a posicao."""
    pontos = np.tile([2.0, 0.0, 0.0], (H * W, 1)).astype(np.float32)
    mascara = _mascara_retangulo(2, 7, 2, 7)  # 25 pixels
    pontos_2d = pontos.reshape(H, W, 3)
    pontos_2d[3, 3] = [20.0, 20.0, 20.0]  # 1 outlier (ex.: borda pegando o fundo)
    nuvem = _cloud_de(pontos_2d.reshape(-1, 3))

    resultado = node.extrair_ponto_3d(nuvem, mascara, indice_deteccao=0)

    assert resultado is not None
    posicao, *_ = resultado
    np.testing.assert_allclose(posicao, [2.0, 0.0, 0.0], atol=1e-5)


def test_poucos_pixels_na_mascara_rejeita(node):
    pontos = np.tile([2.0, 0.0, 0.0], (H * W, 1)).astype(np.float32)
    nuvem = _cloud_de(pontos)
    mascara = _mascara_retangulo(0, 2, 0, 2)  # 4 pixels < min_pixels_mascara=5

    resultado = node.extrair_ponto_3d(nuvem, mascara, indice_deteccao=0)

    assert resultado is None


def test_poucos_pontos_validos_rejeita(node):
    pontos = np.full((H * W, 3), np.inf, dtype=np.float32)
    pontos_2d = pontos.reshape(H, W, 3)
    pontos_2d[2, 2] = [1.0, 1.0, 1.0]  # so 1 ponto valido < min_pixels_validos=3
    nuvem = _cloud_de(pontos_2d.reshape(-1, 3))
    mascara = _mascara_retangulo(2, 6, 2, 6)  # 16 pixels na mascara (passa o 1o filtro)

    resultado = node.extrair_ponto_3d(nuvem, mascara, indice_deteccao=0)

    assert resultado is None


def test_indices_de_pixel_batem_com_a_posicao_certa(node):
    """Confere que o indexamento v*width+u pega o pixel certo, nao outro."""
    pontos_2d = np.zeros((H, W, 3), dtype=np.float32)
    pontos_2d[:, :] = [99.0, 99.0, 99.0]  # "fundo" (nao deve ser lido)
    pontos_2d[7, 1] = [5.0, -2.0, 0.3]     # o alvo, fora da mascara em (2..6, 2..6)
    mascara = _mascara_retangulo(7, 8, 1, 2)  # so 1 pixel: (y=7, x=1)
    nuvem = _cloud_de(pontos_2d.reshape(-1, 3))

    # min_pixels_* do fixture (5 e 3) exigem mais que os 1 pixel deste teste
    node.min_pixels_mascara = 1
    node.min_pixels_validos = 1
    resultado = node.extrair_ponto_3d(nuvem, mascara, indice_deteccao=0)

    assert resultado is not None
    posicao, n_mascara, n_validos = resultado
    assert n_mascara == 1
    np.testing.assert_allclose(posicao, [5.0, -2.0, 0.3], atol=1e-5)
