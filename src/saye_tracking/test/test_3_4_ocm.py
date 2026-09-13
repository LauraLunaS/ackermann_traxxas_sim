"""Submodulo 3.4 - teste do OCM (consistencia de direcao), sem ROS."""
import numpy as np
import pytest
from saye_tracking.associacao import associar
from saye_tracking.ocm import custo_direcao
from saye_tracking.track import Track


# --- direcao_momentum do Track ----------------------------------------
def test_track_novo_sem_historico_suficiente_nao_tem_momentum():
    t = Track(posicao_inicial=(0.0, 0.0), tempo_criacao=0.0)

    assert t.direcao_momentum() is None


def test_track_parado_nao_tem_momentum():
    t = Track(posicao_inicial=(0.0, 0.0), tempo_criacao=0.0)
    t.observar((0.0, 0.0), tempo_atual=0.1)
    t.observar((0.0, 0.0), tempo_atual=0.2)

    assert t.direcao_momentum() is None


def test_track_em_movimento_aponta_a_direcao_certa():
    t = Track(posicao_inicial=(0.0, 0.0), tempo_criacao=0.0)
    t.observar((1.0, 0.0), tempo_atual=0.1)
    t.observar((2.0, 0.0), tempo_atual=0.2)

    np.testing.assert_allclose(t.direcao_momentum(), [1.0, 0.0], atol=1e-9)


# --- custo_direcao (a penalidade em si) -------------------------------
def test_penalidade_zero_quando_direcao_bate():
    penalidade = custo_direcao(
        predicoes_xy=[(0.0, 0.0)], deteccoes_xy=[(1.0, 0.0)],
        direcoes_momentum=[np.array([1.0, 0.0])])

    assert penalidade[0, 0] == pytest.approx(0.0, abs=1e-9)


def test_penalidade_maxima_quando_direcao_oposta():
    penalidade = custo_direcao(
        predicoes_xy=[(0.0, 0.0)], deteccoes_xy=[(-1.0, 0.0)],
        direcoes_momentum=[np.array([1.0, 0.0])], peso=1.0)

    assert penalidade[0, 0] == pytest.approx(2.0, abs=1e-9)


def test_track_sem_momentum_nao_penaliza_ninguem():
    penalidade = custo_direcao(
        predicoes_xy=[(0.0, 0.0)], deteccoes_xy=[(1.0, 0.0), (-1.0, 0.0)],
        direcoes_momentum=[None])

    np.testing.assert_allclose(penalidade, [[0.0, 0.0]])


# --- integracao: OCM desambigua cruzamento ----------------------------
def test_ocm_desambigua_duas_trajetorias_se_cruzando():
    # dois tracks EXATAMENTE na mesma posicao prevista (pior caso possivel
    # pra distancia pura: qualquer combinacao track-deteccao da o mesmo
    # custo total, entao a distancia sozinha nao consegue decidir).
    predicoes = [(5.0, 0.0), (5.0, 0.0)]
    deteccoes = [(5.5, 0.0), (4.5, 0.0)]  # uma na frente de cada um
    momentum = [np.array([1.0, 0.0]), np.array([-1.0, 0.0])]  # A vai p/ +x, B p/ -x

    penal = custo_direcao(predicoes, deteccoes, momentum, peso=1.0)
    matches, sem_track, sem_det = associar(predicoes, deteccoes, custo_extra=penal)

    # track 0 (momentum +x) tem que casar com a deteccao a frente dele (+x);
    # track 1 (momentum -x) com a deteccao a frente dele (-x)
    assert set(matches) == {(0, 0), (1, 1)}
    assert sem_track == []
    assert sem_det == []
