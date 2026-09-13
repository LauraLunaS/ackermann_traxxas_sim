"""
Associacao entre tracks e deteccoes novas (Fase 3, submodulo 3.3).

Dado onde cada track PREVIU que estaria (o `.prever()` do 3.2 ja rodou) e
onde as deteccoes novas realmente estao, decide "quem e quem": monta a
matriz de custo (distancia euclidiana), aplica um portao (gate - rejeita
casamentos longe demais) e resolve com o algoritmo Hungaro (otimo global,
nao um "pega o mais proximo" guloso).

Sem ROS - so numpy/scipy.
"""
import numpy as np
from scipy.optimize import linear_sum_assignment

# custo atribuido a pares fora do gate, pra que o Hungaro nunca os escolha
# a menos que seja estritamente necessario (e mesmo af, sao descartados
# depois de resolver, porque o Hungaro e obrigado a emparelhar tudo se as
# dimensoes permitirem)
_PENALIDADE_FORA_DO_GATE = 1e6


def associar(predicoes_xy, deteccoes_xy, gate_max_distancia=1.5, custo_extra=None):
    """
    Casa tracks previstos com deteccoes novas pela menor distancia total.

    predicoes_xy: (N, 2) - posicao prevista de cada track
    deteccoes_xy: (M, 2) - posicao de cada deteccao nova
    gate_max_distancia: acima disso (metros), o par nunca casa - "pessoa
        nao teleporta". O gate SEMPRE usa a distancia crua, mesmo quando
        `custo_extra` e passado - o gate e uma restricao fisica (admissivel
        ou nao), custo_extra e so uma preferencia (o que o Hungaro otimiza).
    custo_extra: (N, M) opcional, somado ao custo de distancia ANTES do
        Hungaro - ex.: a penalidade de direcao do OCM (`ocm.custo_direcao`).

    Retorna (matches, tracks_sem_par, deteccoes_sem_par):
      matches: lista de (indice_track, indice_deteccao)
      tracks_sem_par: indices de tracks que nao casaram com nada
      deteccoes_sem_par: indices de deteccoes que nao casaram com nada
    """
    predicoes_xy = np.asarray(predicoes_xy, dtype=np.float64).reshape(-1, 2)
    deteccoes_xy = np.asarray(deteccoes_xy, dtype=np.float64).reshape(-1, 2)
    n, m = len(predicoes_xy), len(deteccoes_xy)

    if n == 0 or m == 0:
        return [], list(range(n)), list(range(m))

    custo_distancia = np.linalg.norm(
        predicoes_xy[:, np.newaxis, :] - deteccoes_xy[np.newaxis, :, :], axis=2)
    custo_total = custo_distancia if custo_extra is None else custo_distancia + custo_extra

    custo_com_gate = np.where(custo_distancia > gate_max_distancia,
                              _PENALIDADE_FORA_DO_GATE, custo_total)

    indices_track, indices_deteccao = linear_sum_assignment(custo_com_gate)

    matches = []
    tracks_casados = set()
    deteccoes_casadas = set()
    for it, idet in zip(indices_track, indices_deteccao):
        if custo_distancia[it, idet] <= gate_max_distancia:
            matches.append((int(it), int(idet)))
            tracks_casados.add(it)
            deteccoes_casadas.add(idet)

    tracks_sem_par = [i for i in range(n) if i not in tracks_casados]
    deteccoes_sem_par = [j for j in range(m) if j not in deteccoes_casadas]
    return matches, tracks_sem_par, deteccoes_sem_par
