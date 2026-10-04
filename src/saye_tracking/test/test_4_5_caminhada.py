"""Submodulo 4.5/4.6 - teste da caminhada cinematica (vai-e-vem), sem ROS/sim."""
import math

from saye_tracking.caminhada import direcao_no_instante, indice_quadro, posicao_no_instante


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


# --- direcao_no_instante (4.6) ------------------------------------------
def test_direcao_aponta_pro_destino_na_ida():
    ang = direcao_no_instante(0.0, origem=(2.0, 0.0), destino=(2.0, 2.0), velocidade=0.5)
    assert abs(ang - math.pi / 2) < 1e-9  # +y


def test_direcao_inverte_na_volta():
    # 4s de ida (chega no destino), ja esta voltando logo depois
    ang = direcao_no_instante(4.1, origem=(2.0, 0.0), destino=(2.0, 2.0), velocidade=0.5)
    assert abs(ang - (-math.pi / 2)) < 1e-9  # -y


# --- indice_quadro (4.6) -------------------------------------------------
def test_indice_quadro_comeca_em_zero():
    assert indice_quadro(0.0, velocidade=0.5, n_quadros=6, comprimento_passada=1.2) == 0


def test_indice_quadro_avanca_com_a_distancia():
    # 0.5 m/s * 0.6s = 0.3m percorridos = 1/4 de 1.2m -> quadro 6*0.25=1.5 -> 1
    idx = indice_quadro(0.6, velocidade=0.5, n_quadros=6, comprimento_passada=1.2)
    assert idx == 1


def test_indice_quadro_reinicia_apos_um_ciclo_completo():
    # 1.2m percorridos (comprimento_passada inteiro) -> volta pro quadro 0
    idx = indice_quadro(2.4, velocidade=0.5, n_quadros=6, comprimento_passada=1.2)
    assert idx == 0
