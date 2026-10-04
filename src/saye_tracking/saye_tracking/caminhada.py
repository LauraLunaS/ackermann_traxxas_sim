"""
Caminhada cinematica da pessoa detectavel (Fase 4 - alvo em movimento).

Calcula a posicao de um alvo andando de um lado pro outro (vai-e-vem) entre
dois pontos, a uma velocidade constante, em funcao do tempo. Sem ROS/Gazebo -
so matematica, testavel com numeros simples.

Por que isso existe (em vez de mover a pessoa com fisica de verdade, como os
3 obstaculos dinamicos): testado ao vivo e um corpo alto (centro de massa
perto de 1m do chao) empurrado por forca/torque bruto (plugin
`TrajectoryFollower`) TOMBA, mesmo com varias combinacoes de parametro e
inercia rotacional artificialmente ampliada - vira um problema de
modelagem fisica (precisaria de uma junta restringindo rotacao), nao so de
ajuste fino. A alternativa adotada e mover a pessoa CINEMATICAMENTE -
teleporte direto de posicao via `/world/<mundo>/set_pose` (o mesmo servico
usado pra resetar o robo na Fase 4.4) - sem fisica nenhuma envolvida, logo
sem como tombar. Ver `mover_pessoa_node.py` pra quem liga isso ao Gazebo.
"""
import math

ORIGEM_PADRAO = (2.0, 0.0)
DESTINO_PADRAO = (2.0, 2.0)
VELOCIDADE_PADRAO = 0.3  # m/s, ritmo de caminhada lento


def posicao_no_instante(
        tempo, origem=ORIGEM_PADRAO, destino=DESTINO_PADRAO,
        velocidade=VELOCIDADE_PADRAO):
    """Posicao (x, y) de um alvo fazendo vai-e-vem entre origem e destino."""
    dx = destino[0] - origem[0]
    dy = destino[1] - origem[1]
    distancia = math.hypot(dx, dy)
    duracao_trecho = distancia / velocidade

    fase = tempo % (2 * duracao_trecho)
    if fase <= duracao_trecho:
        fracao = fase / duracao_trecho
        inicio, fim = origem, destino
    else:
        fracao = (fase - duracao_trecho) / duracao_trecho
        inicio, fim = destino, origem

    x = inicio[0] + (fim[0] - inicio[0]) * fracao
    y = inicio[1] + (fim[1] - inicio[1]) * fracao
    return (x, y)


def direcao_no_instante(
        tempo, origem=ORIGEM_PADRAO, destino=DESTINO_PADRAO,
        velocidade=VELOCIDADE_PADRAO):
    """Angulo (rad) de frente pro sentido do trecho atual (ida ou volta)."""
    dx = destino[0] - origem[0]
    dy = destino[1] - origem[1]
    distancia = math.hypot(dx, dy)
    duracao_trecho = distancia / velocidade
    fase = tempo % (2 * duracao_trecho)
    indo = fase <= duracao_trecho
    return math.atan2(dy, dx) if indo else math.atan2(-dy, -dx)


def indice_quadro(tempo, velocidade, n_quadros, comprimento_passada=1.2):
    """
    Calcula o indice do quadro de caminhada (0..n_quadros-1) pro "flipbook" de poses.

    Baseado na distancia percorrida (nao no tempo bruto) - velocidade e
    constante, entao distancia = velocidade * tempo. `comprimento_passada`
    e o quanto o corpo "anda" por ciclo completo dos N quadros extraidos
    (ver `saye_tracking/scripts` / README da Fase 4.6).
    """
    distancia = velocidade * tempo
    fase = (distancia % comprimento_passada) / comprimento_passada
    return int(fase * n_quadros) % n_quadros


def posicao_no_caminho(distancia, waypoints):
    """
    Posicao (x, y) e yaw (rad) de um alvo andando num caminho fechado de waypoints.

    `distancia` e o quanto ja foi andado; o caminho e percorrido em loop
    (o ultimo waypoint volta pro primeiro). Trechos de comprimento zero sao ignorados.
    """
    pontos = [tuple(p) for p in waypoints]
    trechos = list(zip(pontos, pontos[1:] + pontos[:1]))
    comprimentos = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in trechos]
    total = sum(comprimentos)
    restante = distancia % total

    for (a, b), comprimento in zip(trechos, comprimentos):
        if comprimento == 0.0:
            continue
        if restante <= comprimento:
            fracao = restante / comprimento
            x = a[0] + (b[0] - a[0]) * fracao
            y = a[1] + (b[1] - a[1]) * fracao
            return (x, y, math.atan2(b[1] - a[1], b[0] - a[0]))
        restante -= comprimento

    a, b = trechos[-1]
    return (b[0], b[1], math.atan2(b[1] - a[1], b[0] - a[0]))
