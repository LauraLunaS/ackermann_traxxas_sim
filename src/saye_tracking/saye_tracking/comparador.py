"""
Comparador MOT (submodulo 4.2 da Fase 4 - bancada de avaliacao).

Le hipoteses (o que o `tracker_node` disse que existia) e verdade (onde os
objetos realmente estavam no Gazebo), gravadas pelo `gravador_node` (4.1),
e calcula metricas padrao de MOT (MOTA, trocas de ID, falsos
positivos/negativos) com a biblioteca `motmetrics`. Sem ROS - roda offline
em cima dos CSVs gravados.

Metricas (item 4 do roteiro pos-correcao de movimentacao): o MOTA mistura
3 tipos de erro diferentes (perda, fantasma, troca de id) num unico
numero - por isso `METRICAS_PADRAO` sempre reporta `num_switches`
(trocas de id), `num_false_positives` (fantasmas) e `num_misses`
(perdas) separados, alem do MOTA agregado. Tambem inclui `idf1`
(identity F1 - fracao do tempo que cada objeto manteve o id certo,
olhando a trajetoria inteira, nao frame a frame) - metrica mais sensivel
a troca de id do que o MOTA, relevante principalmente pro cenario "robo
parado" (onde, por decisao do usuario, manter o MESMO id por pessoa e a
prioridade); pro cenario "robo andando" o MOTA (ja filtrado pelo FOV da
camera, ver `gravador_atores_node.py`) continua sendo a referencia
principal - rastreamento geral importa mais que permanencia de id ali.

Duas adaptacoes necessarias pros dados do 4.1:
  1. `motmetrics` exige ids NUMERICOS - nao aceita string como
     "pessoa_detectavel" (testado: a biblioteca quebra tentando converter
     pra float). O id da hipotese (ja numerico, vem do rastreador) e usado
     direto; o nome da verdade e mapeado pra um numero estavel na primeira
     vez que aparece (`mapa_ids_verdade`, cresce durante o calculo).
  2. os dois CSVs tem timestamps em taxas diferentes (hipotese ~60Hz do
     rastreador, verdade na taxa da ponte do Gazebo) - agrupamos cada lado
     em "frames" de largura fixa (`tamanho_frame_segundos`) antes de
     comparar; dentro de um frame, fica so a ULTIMA leitura de cada id.
     Linhas com timestamp de relogio de parede (em vez de tempo de sim) sao
     descartadas antes de agrupar, usando um teto absoluto - ver
     `_filtrar_outliers_tempo`.
"""
import argparse
import os

import motmetrics as mm
from saye_tracking.gravador import carregar_csv

METRICAS_PADRAO = [
    'num_frames', 'mota', 'motp', 'idf1', 'num_switches',
    'num_false_positives', 'num_misses', 'num_matches',
]


def _filtrar_outliers_tempo(linhas, tempo_sim_maximo_segundos=1e6):
    """
    Descarta leituras com timestamp de relogio de parede em vez de tempo de sim.

    Usa um teto ABSOLUTO (nao relativo a mediana): tempo de sim desta
    simulacao sempre fica bem abaixo de 1e6 s (~11 dias de sim continua),
    enquanto timestamp de relogio de parede (epoch Unix) hoje esta na casa
    de 1.7-2e9 s. Um filtro relativo a mediana (testado e descartado) quebra
    quando a MAIORIA das leituras vem com o bug (mediana vira relogio de
    parede e filtra as leituras boas, nao as ruins) - ja aconteceu numa
    gravacao real (ver README, achado do 4.1/4.2: uma instancia extra e
    indevida de deteccao_node/tracker_node ficou publicando sem
    `use_sim_time`, contaminando a maior parte de um `hipoteses.csv`).
    """
    return [linha for linha in linhas if linha[0] < tempo_sim_maximo_segundos]


def _agrupar_por_frame(linhas, tamanho_frame_segundos):
    """Agrupa (tempo, id, x, y) em frames discretos, 1 leitura (a ultima) por id."""
    por_frame = {}
    for tempo, id_, x, y in linhas:
        # round(), nao int(): int() trunca e, por erro de ponto flutuante
        # (ex.: 0.3 / 0.1 == 2.9999999999999996), pode jogar um instante
        # pro frame anterior por engano.
        frame = round(tempo / tamanho_frame_segundos)
        por_frame.setdefault(frame, {})[id_] = (x, y)
    return por_frame


def _ids_numericos(nomes, mapa):
    numericos = []
    for nome in nomes:
        if nome not in mapa:
            mapa[nome] = len(mapa)
        numericos.append(mapa[nome])
    return numericos


def calcular_metricas(
        linhas_hipoteses, linhas_verdade, limiar_distancia=0.5,
        tamanho_frame_segundos=0.1, metricas=None):
    """Calcula metricas MOT comparando hipoteses (rastreador) com verdade (Gazebo)."""
    hipoteses = _filtrar_outliers_tempo(linhas_hipoteses)
    verdade = _filtrar_outliers_tempo(linhas_verdade)

    frames_hip = _agrupar_por_frame(hipoteses, tamanho_frame_segundos)
    frames_gt = _agrupar_por_frame(verdade, tamanho_frame_segundos)
    todos_frames = sorted(set(frames_hip) | set(frames_gt))

    mapa_ids_verdade = {}
    acumulador = mm.MOTAccumulator(auto_id=True)

    for frame in todos_frames:
        gt = frames_gt.get(frame, {})
        hip = frames_hip.get(frame, {})

        gt_ids = _ids_numericos(list(gt.keys()), mapa_ids_verdade)
        hip_ids = [int(id_) for id_ in hip.keys()]

        distancias = mm.distances.norm2squared_matrix(
            list(gt.values()), list(hip.values()), max_d2=limiar_distancia ** 2)
        acumulador.update(gt_ids, hip_ids, distancias)

    metricas_host = mm.metrics.create()
    return metricas_host.compute(
        acumulador, metrics=metricas or METRICAS_PADRAO, name='saye_tracking')


def calcular_metricas_de_arquivos(caminho_hipoteses, caminho_verdade, **kwargs):
    """Mesma coisa que `calcular_metricas`, lendo os CSVs gravados pelo gravador_node (4.1)."""
    return calcular_metricas(
        carregar_csv(caminho_hipoteses), carregar_csv(caminho_verdade), **kwargs)


def main():
    parser = argparse.ArgumentParser(
        description='Calcula metricas MOT a partir dos CSVs do gravador_node (4.1).')
    parser.add_argument('diretorio', help='Diretorio com hipoteses.csv e verdade.csv')
    parser.add_argument(
        '--limiar-distancia', type=float, default=0.5,
        help='Distancia maxima (m) pra considerar hipotese e verdade a mesma coisa.')
    parser.add_argument(
        '--tamanho-frame', type=float, default=0.1,
        help='Largura (s) de cada frame usado pra sincronizar as duas series.')
    args = parser.parse_args()

    resumo = calcular_metricas_de_arquivos(
        os.path.join(args.diretorio, 'hipoteses.csv'),
        os.path.join(args.diretorio, 'verdade.csv'),
        limiar_distancia=args.limiar_distancia,
        tamanho_frame_segundos=args.tamanho_frame)
    print(resumo.to_string())


if __name__ == '__main__':
    main()
