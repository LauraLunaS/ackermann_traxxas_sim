"""
OCR + ORU - recuperacao de tracks perdidos (Fase 3, submodulo 3.5).

OCR (Observation-Centric Recovery): quando uma deteccao nao casa com
nenhum track no primeiro turno de associacao (3.3+3.4, que usa a posicao
PREVISTA pelo Kalman), ainda tentamos casar essa deteccao com tracks
PERDIDOS usando a ULTIMA POSICAO REALMENTE OBSERVADA deles - nao a previsao,
que pode ter derivado bastante durante a oclusao. Um objeto que reaparece
tende a estar perto de onde sumiu, nao de onde o filtro (as cegas) acha
que ele foi parar.

Gate adaptativo + OCM no OCR (Fase 4.8 - corrige troca de id sem oclusao
real): a 1a versao usava o MESMO `gate_distancia` fixo (1.5m) do turno
normal de associacao, por quanto tempo o track estivesse perdido. Isso e
fisicamente errado - um track perdido ha 0.1s so pode ter andado uns
centimetros, mas um perdido ha 1.4s (perto da tolerancia de 1.5s) pode
estar varios decimetros adiante; usar 1.5m pros dois casos abre a porta
pra "recuperar" um track com a deteccao de uma PESSOA DIFERENTE que por
acaso esta por ali perto, sem que as duas tenham se ocluido visualmente -
confirmado ao vivo (Fase 4.6/4.7): um id ficava a sessao TODA "vivo" mas,
tracando a trajetoria dele, media deslocamentos de 0.6-1.0m em 0.2-0.3s
(2.7-3.4 m/s) - 10x a velocidade maxima configurada de qualquer pessoa -
ou seja, o MESMO id estava silenciosamente pulando entre pessoas reais
diferentes. Agora o gate de cada track escala com o tempo que ele esta
perdido (`velocidade_maxima_esperada * tempo_perdido + margem`, nunca
acima de `gate_distancia`) e a recuperacao tambem usa o custo de direcao
do OCM (3.4) - ignorado antes, apesar do OCR ser exatamente o momento em
que duas pessoas podem estar proximas e precisar de desambiguacao por
direcao, nao so distancia.

ORU (Observation-Centric Re-Update): quando o OCR acha um par, em vez de
uma unica correcao grande (previsao ruim + 1 correcao violenta), trace uma
"trajetoria virtual" - uma reta entre a ultima observacao real e a nova -
e re-roda predict/update do Kalman ao longo dela, em passos pequenos. Isso
faz o estado final (principalmente a velocidade) refletir o deslocamento
real ao longo do tempo real, em vez de herdar a covariancia distorcida
acumulada durante o periodo cego.

Sem ROS.
"""
import numpy as np

from saye_tracking.associacao import associar
from saye_tracking.ocm import custo_direcao


def recuperar_perdidos(
        tracks_perdidos, deteccoes_xy, tempo_atual, gate_max_distancia=1.5,
        velocidade_maxima_esperada=0.6, margem_gate=0.3, peso_ocm=1.0):
    """
    Tenta casar tracks PERDIDOS com deteccoes que sobraram do 1o turno.

    tracks_perdidos: lista de Track (estado PERDIDO, com historico >= 1)
    deteccoes_xy: (M, 2) - deteccoes que sobraram da associacao normal
    tempo_atual: usado pra saber ha quanto tempo CADA track esta perdido
        (`tempo_atual - t.tempo_ultima_observacao`) e escalar o gate dele.
    gate_max_distancia: teto absoluto do gate (metros) - nunca ultrapassado,
        mesmo pra quem esta perdido ha muito tempo.
    velocidade_maxima_esperada: quao rapido (m/s) um objeto rastreado pode
        plausivelmente andar - define quanto o gate de cada track CRESCE
        por segundo perdido. Deve ter uma margem generosa sobre a
        velocidade real (ex.: 0.6 pra pessoas andando a 0.24-0.3 m/s), nao
        o valor exato - e so pra limitar recuperacao fisicamente impossivel,
        nao pra apertar o caso normal.
    margem_gate: constante (metros) somada ao gate, pra absorver ruido de
        deteccao/projecao mesmo com tempo_perdido ~0.
    peso_ocm: peso do custo de direcao (ocm.custo_direcao) somado ao custo
        de distancia - mesmo papel que em `rastreador.processar`.

    Retorna (matches, indices_tracks_ainda_sem_par, indices_deteccoes_sem_par)
    no mesmo formato de `associacao.associar` (indices relativos as LISTAS
    passadas aqui, nao aos indices originais do turno 1 - quem chama precisa
    tracear de volta).
    """
    posicoes_ultima_observacao = [t.historico[-1][1] for t in tracks_perdidos]

    tempos_perdido = np.array(
        [max(tempo_atual - t.tempo_ultima_observacao, 0.0) for t in tracks_perdidos])
    gates = np.minimum(
        gate_max_distancia, velocidade_maxima_esperada * tempos_perdido + margem_gate)

    momentum = [t.direcao_momentum() for t in tracks_perdidos]
    penal = custo_direcao(posicoes_ultima_observacao, deteccoes_xy, momentum, peso=peso_ocm)

    return associar(posicoes_ultima_observacao, deteccoes_xy, gates, custo_extra=penal)


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
