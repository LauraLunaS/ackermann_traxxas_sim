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
