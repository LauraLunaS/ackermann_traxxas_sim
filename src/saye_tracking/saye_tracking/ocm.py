"""
OCM - Observation-Centric Momentum (Fase 3, submodulo 3.4).

Soma, na associacao, um termo de CONSISTENCIA DE DIRECAO: um track que vem
se movendo numa direcao deve preferir uma deteccao que continue nessa
direcao, mesmo que outra deteccao esteja geometricamente mais perto. Isso
desambigua duas trajetorias se cruzando, onde a distancia sozinha empata
ou favorece o casamento errado.

A direcao usada e a de OBSERVACOES REAIS do track (`Track.direcao_momentum`,
3.2/3.4), nao a velocidade do filtro de Kalman - que fica ruidosa logo
depois de uma oclusao, exatamente quando a desambiguacao mais importa.

Sem ROS - so numpy.
"""
import numpy as np


def custo_direcao(predicoes_xy, deteccoes_xy, direcoes_momentum, peso=1.0):
    """
    Penalidade de inconsistencia de direcao, para somar ao custo de distancia.

    predicoes_xy: (N, 2) - posicao prevista de cada track
    deteccoes_xy: (M, 2) - posicao de cada deteccao nova
    direcoes_momentum: lista de tamanho N; cada item e um vetor unitario
        (2,) com a direcao historica do track, ou None se ainda nao ha
        direcao definida (track novo, ou parado)
    peso: escala da penalidade. 0 quando a direcao track->deteccao concorda
        com o momentum, ate `2*peso` quando e oposta. Tracks sem momentum
        (None) nao penalizam nenhuma deteccao (falta de informacao nao
        deve desqualificar ninguem).

    Retorna uma matriz (N, M) pra somar ao custo de distancia antes do
    Hungaro - ver `associacao.associar(..., custo_extra=...)`.
    """
    predicoes_xy = np.asarray(predicoes_xy, dtype=np.float64).reshape(-1, 2)
    deteccoes_xy = np.asarray(deteccoes_xy, dtype=np.float64).reshape(-1, 2)
    n, m = len(predicoes_xy), len(deteccoes_xy)
    penalidade = np.zeros((n, m))

    for i in range(n):
        direcao = direcoes_momentum[i]
        if direcao is None:
            continue
        for j in range(m):
            vetor = deteccoes_xy[j] - predicoes_xy[i]
            norma = np.linalg.norm(vetor)
            if norma < 1e-6:
                continue  # deteccao praticamente em cima da previsao
            similaridade = float(np.dot(direcao, vetor / norma))  # -1..1
            penalidade[i, j] = peso * (1.0 - similaridade)

    return penalidade
