"""
OCR + ORU - recuperacao de tracks perdidos (Fase 3, submodulo 3.5).

OCR (Observation-Centric Recovery): quando uma deteccao nao casa com
nenhum track no primeiro turno de associacao (3.3+3.4, que usa a posicao
PREVISTA pelo Kalman), ainda tentamos casar essa deteccao com tracks
PERDIDOS usando a ULTIMA POSICAO REALMENTE OBSERVADA deles - nao a previsao,
que pode ter derivado bastante durante a oclusao. Um objeto que reaparece
tende a estar perto de onde sumiu, nao de onde o filtro (as cegas) acha
que ele foi parar.

ORU (Observation-Centric Re-Update): quando o OCR acha um par, em vez de
uma unica correcao grande (previsao ruim + 1 correcao violenta), trace uma
"trajetoria virtual" - uma reta entre a ultima observacao real e a nova -
e re-roda predict/update do Kalman ao longo dela, em passos pequenos. Isso
faz o estado final (principalmente a velocidade) refletir o deslocamento
real ao longo do tempo real, em vez de herdar a covariancia distorcida
acumulada durante o periodo cego.

Sem ROS.
"""
from saye_tracking.associacao import associar


def recuperar_perdidos(tracks_perdidos, deteccoes_xy, gate_max_distancia=1.5):
    """
    Tenta casar tracks PERDIDOS com deteccoes que sobraram do 1o turno.

    tracks_perdidos: lista de Track (estado PERDIDO, com historico >= 1)
    deteccoes_xy: (M, 2) - deteccoes que sobraram da associacao normal

    Retorna (matches, indices_tracks_ainda_sem_par, indices_deteccoes_sem_par)
    no mesmo formato de `associacao.associar` (indices relativos as LISTAS
    passadas aqui, nao aos indices originais do turno 1 - quem chama precisa
    tracear de volta).
    """
    posicoes_ultima_observacao = [t.historico[-1][1] for t in tracks_perdidos]
    return associar(posicoes_ultima_observacao, deteccoes_xy, gate_max_distancia)


def reatualizar_trajetoria_virtual(track, posicao_nova, tempo_novo, n_passos=5):
    """
    Re-atualiza um track recem-recuperado ao longo de uma reta virtual.

    Interpola `n_passos` pontos entre a ultima observacao real do track
    (antes do sumico) e `posicao_nova` (a deteccao que o OCR achou agora),
    igualmente espacados no tempo, e chama `track.prever`+`track.observar`
    em cada um - como se o track tivesse sido observado ao longo do
    caminho, nao so nas duas pontas.

    Se o tempo nao andou (dt_total <= 0), cai pra uma observacao direta.
    """
    tempo_antigo, posicao_antiga = track.historico[-1]
    dt_total = tempo_novo - tempo_antigo

    if dt_total <= 0:
        track.observar(posicao_nova, tempo_novo)
        return

    for k in range(1, n_passos + 1):
        fracao = k / n_passos
        tempo_passo = tempo_antigo + fracao * dt_total
        posicao_passo = posicao_antiga + fracao * (posicao_nova - posicao_antiga)
        track.prever(tempo_passo)
        track.observar(posicao_passo, tempo_passo)
