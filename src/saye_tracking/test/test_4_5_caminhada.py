"""Submodulo 4.5 - teste da caminhada cinematica (vai-e-vem), sem ROS/sim."""
from saye_tracking.caminhada import posicao_no_instante


def test_comeca_na_origem_no_instante_zero():
    pos = posicao_no_instante(
        0.0, origem=(2.0, 0.0), destino=(2.0, 2.0), velocidade=0.5)
    assert pos == (2.0, 0.0)


def test_chega_no_destino_na_metade_do_trecho():
    # distancia 2m a 0.5 m/s -> 4s pra ir, 4s pra voltar
    x, y = posicao_no_instante(
        4.0, origem=(2.0, 0.0), destino=(2.0, 2.0), velocidade=0.5)
    assert x == 2.0
    assert abs(y - 2.0) < 1e-9


def test_metade_do_caminho_de_ida():
    x, y = posicao_no_instante(
        2.0, origem=(2.0, 0.0), destino=(2.0, 2.0), velocidade=0.5)
    assert abs(y - 1.0) < 1e-9


def test_volta_depois_de_chegar_no_destino():
    # em t=6s (4s de ida + 2s de volta) deve estar na metade voltando
    x, y = posicao_no_instante(
        6.0, origem=(2.0, 0.0), destino=(2.0, 2.0), velocidade=0.5)
    assert abs(y - 1.0) < 1e-9


def test_repete_o_ciclo_em_loop():
    # um ciclo completo (ida+volta) dura 8s - t=8 deve ser igual a t=0
    inicio = posicao_no_instante(
        0.0, origem=(2.0, 0.0), destino=(2.0, 2.0), velocidade=0.5)
    um_ciclo_depois = posicao_no_instante(
        8.0, origem=(2.0, 0.0), destino=(2.0, 2.0), velocidade=0.5)
    assert inicio == um_ciclo_depois
