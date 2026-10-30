"""
Verdade (ground truth) analitica para atores andando.

Submodulo 4.9 - bancada de avaliacao multi-pessoa. A bancada original
(4.1, `gravador_node.py`) le a verdade direto do Gazebo
(`/world/<mundo>/pose/info`, por INDICE - ver achado 2 la) porque a
unica pessoa existente na epoca (`pessoa_detectavel`) era um unico modelo
estatico com indice fixo. Isso nao serve mais pros atores andando (Fase
4.6): cada um e um "flipbook" de ~27-30 sub-modelos (`pessoa_andando_N_
frame_K`), e a QUALQUER instante so um deles esta visivel (os outros
parados em z=-50) - o indice do sub-modelo "ativo" muda a cada troca de
quadro, entao nao da pra usar indice fixo como verdade.

Solucao: a posicao de um ator andando e INTEIRAMENTE determinista a partir
da config dele (`waypoints`, `velocidade`) e de quanto tempo se passou
desde que o `mover_pessoa_animada_node` dele comecou a tiquetaquear -
e exatamente a mesma formula que o proprio no usa pra decidir onde
teleportar (`mover_pessoa_animada_node._callback_timer`:
`posicao_no_caminho(velocidade * tempo, waypoints)`, `tempo = n_ticks /
taxa_hz` desde a criacao do timer). Em vez de ler a posicao de volta do
Gazebo (fragil, sujeito a indice errado), RECALCULAMOS ela aqui com a
mesma formula - verdade exata por construcao, sem nenhuma dependencia do
bridge de pose do Gazebo.

Sem ROS - so a logica, testavel com configs fabricadas.
"""
from saye_tracking.caminhada import posicao_no_caminho


def posicao_verdadeira(ator, tempo_desde_inicio):
    """
    Posicao (x, y) de um ator no instante `tempo_desde_inicio`.

    `tempo_desde_inicio`: segundos desde que o `mover_pessoa_animada_node`
    dele comecou.

    `ator`: dict com pelo menos `waypoints` (lista de [x,y]) e `velocidade`
    (m/s) - o mesmo formato de uma entrada de `config/atores.yaml`.
    """
    distancia = ator['velocidade'] * tempo_desde_inicio
    x, y, _yaw = posicao_no_caminho(distancia, ator['waypoints'])
    return (x, y)


def posicoes_verdadeiras(atores, tempo_desde_inicio):
    """
    Posicao de VARIOS atores no mesmo instante.

    `atores`: lista de dicts (formato `config/atores.yaml`, cada um com
    `nome`, `waypoints`, `velocidade`).

    Retorna um dict {nome: (x, y)}.
    """
    return {
        ator['nome']: posicao_verdadeira(ator, tempo_desde_inicio)
        for ator in atores
    }
