"""Submodulo 4.7 - caminhos por waypoints (loop fechado), sem ROS/sim."""
import math

from saye_tracking.caminhada import posicao_no_caminho


def test_comeca_no_primeiro_waypoint():
    assert posicao_no_caminho(0.0, [(2.0, 0.0), (2.0, 2.0)]) == (2.0, 0.0, math.pi / 2)


def test_meio_do_primeiro_trecho():
    x, y, yaw = posicao_no_caminho(1.0, [(2.0, 0.0), (2.0, 2.0)])
    assert abs(x - 2.0) < 1e-9 and abs(y - 1.0) < 1e-9
    assert abs(yaw - math.pi / 2) < 1e-9


def test_loop_fecha_no_primeiro_waypoint():
    x, y, _ = posicao_no_caminho(4.0, [(2.0, 0.0), (2.0, 2.0)])
    assert abs(x - 2.0) < 1e-9 and abs(y - 0.0) < 1e-9


def test_volta_no_trecho_de_retorno_com_yaw_invertido():
    x, y, yaw = posicao_no_caminho(2.5, [(2.0, 0.0), (2.0, 2.0)])
    assert abs(y - 1.5) < 1e-9
    assert abs(yaw + math.pi / 2) < 1e-9


def test_segue_quadrado_com_curvas():
    quadrado = [(1.0, 1.0), (3.0, 1.0), (3.0, 3.0), (1.0, 3.0)]
    x, y, yaw = posicao_no_caminho(2.0 + 1.0, quadrado)
    assert abs(x - 3.0) < 1e-9 and abs(y - 2.0) < 1e-9
    assert abs(yaw - math.pi / 2) < 1e-9


def test_trecho_de_comprimento_zero_nao_quebra():
    x, y, _ = posicao_no_caminho(1.0, [(0.0, 0.0), (0.0, 0.0), (2.0, 0.0), (2.0, 2.0)])
    assert abs(x - 1.0) < 1e-9 and abs(y - 0.0) < 1e-9


def test_dois_caminhos_se_cruzam_no_ponto_esperado():
    # pessoa 1 em x=2 (y de 0 a 2) e pessoa 2 em y=1 (x de 1 a 3): cruzam em (2, 1)
    p1 = [(2.0, 0.0), (2.0, 2.0)]
    p2 = [(1.0, 1.0), (3.0, 1.0)]
    x1, y1, _ = posicao_no_caminho(1.0, p1)
    x2, y2, _ = posicao_no_caminho(1.0, p2)
    assert abs(x1 - 2.0) < 1e-9 and abs(y1 - 1.0) < 1e-9
    assert abs(x2 - 2.0) < 1e-9 and abs(y2 - 1.0) < 1e-9
