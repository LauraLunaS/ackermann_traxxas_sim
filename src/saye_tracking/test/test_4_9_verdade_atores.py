"""
Submodulo 4.9 - verdade analitica para atores andando, sem ROS.

Confere que `posicao_verdadeira`/`posicoes_verdadeiras` reproduzem
exatamente a mesma formula que `mover_pessoas_node` usa pra teleportar o
ator (`velocidade * tempo -> posicao_no_caminho`). Essas funcoes nao sao
mais usadas pra GRAVAR a verdade da bancada (que agora le a posicao REAL
medida do Gazebo - ver `gravador_atores_node.py`), mas continuam validas
como referencia da formula de movimento em si, e `nome_quadro_ativo`
(usada tanto pelo mover quanto pelo gravador, pra saber qual quadro do
flipbook deveria estar visivel agora) depende delas internamente.
"""
from saye_tracking.caminhada import posicao_no_caminho
from saye_tracking.verdade_atores import (
    nome_quadro_ativo, posicao_verdadeira, posicoes_verdadeiras)


def test_posicao_verdadeira_bate_com_a_formula_do_mover_node():
    ator = {'waypoints': [[2.0, 0.0], [2.0, 2.0]], 'velocidade': 0.3}
    tempo = 3.7

    esperado_x, esperado_y, _ = posicao_no_caminho(
        ator['velocidade'] * tempo, ator['waypoints'])

    assert posicao_verdadeira(ator, tempo) == (esperado_x, esperado_y)


def test_posicao_verdadeira_no_instante_zero_e_o_primeiro_waypoint():
    ator = {'waypoints': [[1.0, 1.0], [3.0, 1.0], [3.0, 3.0], [1.0, 3.0]], 'velocidade': 0.25}

    assert posicao_verdadeira(ator, 0.0) == (1.0, 1.0)


def test_posicoes_verdadeiras_retorna_um_dict_por_nome():
    atores = [
        {'nome': 'pessoa_1', 'waypoints': [[2.0, 0.0], [2.0, 2.0]], 'velocidade': 0.3},
        {'nome': 'pessoa_3', 'waypoints': [[3.5, 0.0], [3.5, 2.0]], 'velocidade': 0.24},
    ]

    posicoes = posicoes_verdadeiras(atores, tempo_desde_inicio=1.0)

    assert set(posicoes.keys()) == {'pessoa_1', 'pessoa_3'}
    assert posicoes['pessoa_1'] == posicao_verdadeira(atores[0], 1.0)
    assert posicoes['pessoa_3'] == posicao_verdadeira(atores[1], 1.0)


def test_mesmo_ator_em_instantes_diferentes_anda_fisicamente_plausivel():
    """Num intervalo curto, o deslocamento nao pode exceder velocidade * dt."""
    ator = {'waypoints': [[1.0, 1.0], [3.0, 1.0], [3.0, 3.0], [1.0, 3.0]], 'velocidade': 0.25}
    dt = 0.5

    x0, y0 = posicao_verdadeira(ator, 10.0)
    x1, y1 = posicao_verdadeira(ator, 10.0 + dt)

    deslocamento = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    assert deslocamento <= ator['velocidade'] * dt + 1e-9


def test_nome_quadro_ativo_usa_prefixo_e_indice_da_formula_de_caminhada():
    from saye_tracking.caminhada import indice_quadro

    ator = {
        'prefixo_modelo': 'pessoa_andando_1_frame_', 'n_quadros': 29,
        'comprimento_passada': 0.302, 'velocidade': 0.3,
    }
    tempo = 4.1

    quadro_esperado = indice_quadro(
        tempo, velocidade=ator['velocidade'], n_quadros=ator['n_quadros'],
        comprimento_passada=ator['comprimento_passada'])

    assert nome_quadro_ativo(ator, tempo) == f'pessoa_andando_1_frame_{quadro_esperado}'


def test_nome_quadro_ativo_no_instante_zero_e_o_quadro_0():
    ator = {
        'prefixo_modelo': 'pessoa_andando_2_frame_', 'n_quadros': 27,
        'comprimento_passada': 0.281, 'velocidade': 0.25,
    }

    assert nome_quadro_ativo(ator, 0.0) == 'pessoa_andando_2_frame_0'
