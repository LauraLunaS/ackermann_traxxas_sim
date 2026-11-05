"""Item 2 do roteiro pos-correcao - checagens automaticas de validade, sem ROS."""
from saye_tracking.validacao_bancada import (
    checar_atores_andaram, checar_robo_comecou_no_spawn, distancia_percorrida)

POSE_SPAWN = (-1.0, 1.0, 0.15)


def test_distancia_percorrida_soma_segmentos_consecutivos():
    pontos = [(0.0, 0.0), (3.0, 0.0), (3.0, 4.0)]
    assert distancia_percorrida(pontos) == 7.0


def test_distancia_percorrida_com_1_ponto_e_zero():
    assert distancia_percorrida([(1.0, 2.0)]) == 0.0


def _verdade_andando(nome, velocidade, duracao, taxa_hz=20.0):
    """Fabrica linhas de verdade de um ator andando em linha reta a `velocidade`."""
    n = int(duracao * taxa_hz)
    return [(i / taxa_hz, nome, velocidade * (i / taxa_hz), 0.0) for i in range(n)]


def test_checar_atores_andaram_aceita_ator_que_andou_o_esperado():
    atores = [{'nome': 'pessoa_1', 'velocidade': 0.3}]
    verdade = _verdade_andando('pessoa_1', velocidade=0.3, duracao=10.0)

    valido, motivos = checar_atores_andaram(verdade, atores, duracao_teste=10.0)

    assert valido is True
    assert motivos == []


def test_checar_atores_andaram_rejeita_ator_parado():
    atores = [{'nome': 'pessoa_1', 'velocidade': 0.3}]
    # "congelado": sempre a mesma posicao - exatamente o achado 4 (gz_pose_vector.py)
    verdade = [(t / 20.0, 'pessoa_1', 2.0, 0.0) for t in range(200)]

    valido, motivos = checar_atores_andaram(verdade, atores, duracao_teste=10.0)

    assert valido is False
    assert 'pessoa_1' in motivos[0]


def test_checar_atores_andaram_rejeita_ator_ausente_da_verdade():
    atores = [{'nome': 'pessoa_1', 'velocidade': 0.3}, {'nome': 'pessoa_2', 'velocidade': 0.25}]
    verdade = _verdade_andando('pessoa_1', velocidade=0.3, duracao=10.0)  # so pessoa_1

    valido, motivos = checar_atores_andaram(verdade, atores, duracao_teste=10.0)

    assert valido is False
    assert any('pessoa_2' in m and 'nao aparece' in m for m in motivos)


def test_checar_robo_comecou_no_spawn_aceita_robo_parado_no_spawn():
    robo = [(t / 10.0, POSE_SPAWN[0], POSE_SPAWN[1], 0.0) for t in range(20)]

    valido, motivos = checar_robo_comecou_no_spawn(robo, POSE_SPAWN)

    assert valido is True
    assert motivos == []


def test_checar_robo_comecou_no_spawn_rejeita_posicao_inicial_errada():
    robo = [(t / 10.0, 5.0, 5.0, 0.0) for t in range(20)]  # longe do spawn

    valido, motivos = checar_robo_comecou_no_spawn(robo, POSE_SPAWN)

    assert valido is False
    assert 'spawn' in motivos[0]


def test_checar_robo_comecou_no_spawn_rejeita_cmd_vel_residual():
    # comeca no spawn certo, mas ja desliza rapido nos 1os instantes -
    # exatamente o achado 3 (/cmd_vel residual nao zerado antes do reset)
    x0, y0 = POSE_SPAWN[0], POSE_SPAWN[1]
    robo = [(t / 10.0, x0 + 0.4 * (t / 10.0), y0, 0.0) for t in range(20)]

    valido, motivos = checar_robo_comecou_no_spawn(robo, POSE_SPAWN)

    assert valido is False
    assert 'cmd_vel' in motivos[0]


def test_checar_robo_comecou_no_spawn_rejeita_sem_nenhuma_amostra():
    valido, motivos = checar_robo_comecou_no_spawn([], POSE_SPAWN)

    assert valido is False
    assert motivos == ['nenhuma pose do robo foi gravada']
