"""Submodulo 3.3 - teste da associacao (custo + gate + Hungaro), sem ROS."""
from saye_tracking.associacao import associar


def test_casamento_simples_um_track_uma_deteccao_perto():
    matches, sem_track, sem_det = associar([(0.0, 0.0)], [(0.1, 0.0)])

    assert matches == [(0, 0)]
    assert sem_track == []
    assert sem_det == []


def test_gate_rejeita_par_longe_demais():
    matches, sem_track, sem_det = associar(
        [(0.0, 0.0)], [(5.0, 0.0)], gate_max_distancia=1.5)

    assert matches == []
    assert sem_track == [0]
    assert sem_det == [0]


def test_mais_deteccoes_que_tracks_sobra_deteccao():
    matches, sem_track, sem_det = associar(
        [(0.0, 0.0)], [(0.1, 0.0), (10.0, 10.0)])

    assert matches == [(0, 0)]
    assert sem_track == []
    assert sem_det == [1]


def test_mais_tracks_que_deteccoes_sobra_track():
    matches, sem_track, sem_det = associar(
        [(0.0, 0.0), (10.0, 10.0)], [(0.1, 0.0)])

    assert matches == [(0, 0)]
    assert sem_track == [1]
    assert sem_det == []


def test_escolhe_o_casamento_de_menor_custo_total():
    # predicoes em (0,0) e (3,0); deteccoes em (1,0) e (2,0)
    # custo direto: 0-0=1, 1-1=1 (total 2) | cruzado: 0-1=2, 1-0=2 (total 4)
    # o Hungaro tem que escolher o par direto (menor custo total), mesmo
    # cada deteccao estando mais perto do OUTRO track em termos "achatados"
    matches, sem_track, sem_det = associar(
        [(0.0, 0.0), (3.0, 0.0)], [(1.0, 0.0), (2.0, 0.0)])

    assert set(matches) == {(0, 0), (1, 1)}
    assert sem_track == []
    assert sem_det == []


def test_gate_parcial_um_par_casa_outro_nao():
    matches, sem_track, sem_det = associar(
        predicoes_xy=[(0.0, 0.0), (100.0, 100.0)],
        deteccoes_xy=[(0.2, 0.0), (100.0, 50.0)],
        gate_max_distancia=1.5)

    assert matches == [(0, 0)]
    assert sem_track == [1]
    assert sem_det == [1]


def test_sem_tracks_ou_sem_deteccoes_nao_quebra():
    assert associar([], [(0.0, 0.0)]) == ([], [], [0])
    assert associar([(0.0, 0.0)], []) == ([], [0], [])
    assert associar([], []) == ([], [], [])
