"""Submodulo 4.2 - teste do comparador MOT (motmetrics), sem ROS/sim."""
import os
import tempfile

from saye_tracking.comparador import calcular_metricas, calcular_metricas_de_arquivos
from saye_tracking.gravador import Gravador


def test_hipotese_perfeita_da_mota_1_sem_falha():
    # 5 frames, hipotese sempre em cima da verdade -> tudo casa, MOTA=1
    hip = [(t, '1', 2.0, 1.0) for t in [0.0, 0.1, 0.2, 0.3, 0.4]]
    gt = [(t, 'pessoa', 2.0, 1.0) for t in [0.0, 0.1, 0.2, 0.3, 0.4]]

    resumo = calcular_metricas(hip, gt, limiar_distancia=0.5, tamanho_frame_segundos=0.1)

    assert resumo['num_frames'].iloc[0] == 5
    assert resumo['mota'].iloc[0] == 1.0
    assert resumo['num_switches'].iloc[0] == 0
    assert resumo['num_false_positives'].iloc[0] == 0
    assert resumo['num_misses'].iloc[0] == 0
    assert resumo['num_matches'].iloc[0] == 5


def test_hipotese_faltando_em_um_frame_conta_como_falso_negativo():
    # verdade existe nos 3 frames, hipotese so aparece em 2 -> 1 miss
    gt = [(t, 'pessoa', 2.0, 1.0) for t in [0.0, 0.1, 0.2]]
    hip = [(0.0, '1', 2.0, 1.0), (0.2, '1', 2.0, 1.0)]  # falta o frame 0.1

    resumo = calcular_metricas(hip, gt, limiar_distancia=0.5, tamanho_frame_segundos=0.1)

    assert resumo['num_misses'].iloc[0] == 1
    assert resumo['num_matches'].iloc[0] == 2
    assert resumo['mota'].iloc[0] < 1.0


def test_hipotese_extra_sem_verdade_conta_como_falso_positivo():
    # hipotese ve um objeto fantasma que nao existe na verdade
    gt = [(t, 'pessoa', 2.0, 1.0) for t in [0.0, 0.1]]
    hip = [(0.0, '1', 2.0, 1.0), (0.1, '1', 2.0, 1.0), (0.1, '2', 8.0, 8.0)]

    resumo = calcular_metricas(hip, gt, limiar_distancia=0.5, tamanho_frame_segundos=0.1)

    assert resumo['num_false_positives'].iloc[0] == 1
    assert resumo['num_matches'].iloc[0] == 2


def test_hipotese_muito_longe_nao_casa_mesmo_existindo_verdade():
    # hipotese existe mas fora do limiar de distancia -> vira miss + FP, nao match
    gt = [(0.0, 'pessoa', 2.0, 1.0)]
    hip = [(0.0, '1', 10.0, 10.0)]

    resumo = calcular_metricas(hip, gt, limiar_distancia=0.5, tamanho_frame_segundos=0.1)

    assert resumo['num_matches'].iloc[0] == 0
    assert resumo['num_misses'].iloc[0] == 1
    assert resumo['num_false_positives'].iloc[0] == 1


def test_troca_de_id_da_hipotese_conta_como_switch():
    # mesmo objeto de verdade, mas o id da hipotese muda no meio -> 1 troca
    gt = [(t, 'pessoa', 2.0, 1.0) for t in [0.0, 0.1, 0.2]]
    hip = [(0.0, '1', 2.0, 1.0), (0.1, '1', 2.0, 1.0), (0.2, '2', 2.0, 1.0)]

    resumo = calcular_metricas(hip, gt, limiar_distancia=0.5, tamanho_frame_segundos=0.1)

    # motmetrics conta o proprio instante da troca como "switch", nao
    # como "match" - por isso 1 switch + 2 matches = 3 instantes de verdade
    assert resumo['num_switches'].iloc[0] == 1
    assert resumo['num_matches'].iloc[0] == 2


def test_hipotese_perfeita_da_idf1_1_sem_falha():
    hip = [(t, '1', 2.0, 1.0) for t in [0.0, 0.1, 0.2, 0.3, 0.4]]
    gt = [(t, 'pessoa', 2.0, 1.0) for t in [0.0, 0.1, 0.2, 0.3, 0.4]]

    resumo = calcular_metricas(hip, gt, limiar_distancia=0.5, tamanho_frame_segundos=0.1)

    assert resumo['idf1'].iloc[0] == 1.0


def test_idf1_e_mais_sensivel_a_troca_de_id_do_que_o_mota():
    """
    Confere que idf1 penaliza troca de id mais do que o mota.

    Item 4 do roteiro pos-correcao: o MOTA mistura varios erros num numero
    so, e pode ficar "alto" mesmo com troca de id (posicao continua
    casando, so o id muda) - a razao de reportar `idf1` junto, nao so o
    MOTA, pro cenario "robo parado" (onde identidade e a prioridade).
    """
    # posicao sempre casa (nenhum miss/FP) - so o id da hipotese troca na metade
    gt = [(t, 'pessoa', 2.0, 1.0) for t in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]]
    hip = [
        (0.0, '1', 2.0, 1.0), (0.1, '1', 2.0, 1.0), (0.2, '1', 2.0, 1.0),
        (0.3, '2', 2.0, 1.0), (0.4, '2', 2.0, 1.0), (0.5, '2', 2.0, 1.0),
    ]

    resumo = calcular_metricas(hip, gt, limiar_distancia=0.5, tamanho_frame_segundos=0.1)

    assert resumo['mota'].iloc[0] > 0.8  # posicao sempre casou, so 1 switch
    assert resumo['idf1'].iloc[0] < resumo['mota'].iloc[0]  # idf1 penaliza mais a troca


def test_outlier_de_relogio_de_parede_e_descartado_sem_quebrar_o_calculo():
    # replica o achado do 4.1: 1a leitura da hipotese vem com timestamp de
    # relogio de parede (epoch, ~1.7 bilhao) em vez de tempo de sim - nao
    # pode virar um frame proprio nem quebrar o agrupamento
    hip = [(1790794691.7, '1', 2.0, 1.0)] + [(t, '1', 2.0, 1.0) for t in [0.0, 0.1, 0.2]]
    gt = [(t, 'pessoa', 2.0, 1.0) for t in [0.0, 0.1, 0.2]]

    resumo = calcular_metricas(hip, gt, limiar_distancia=0.5, tamanho_frame_segundos=0.1)

    assert resumo['num_frames'].iloc[0] == 3
    assert resumo['mota'].iloc[0] == 1.0


def test_maioria_das_leituras_com_relogio_de_parede_nao_derruba_as_boas():
    # achado real (4.2): uma instancia extra e indevida de deteccao/tracker
    # ficou publicando sem use_sim_time e contaminou a MAIORIA das linhas -
    # um filtro relativo a mediana erraria o lado (filtraria as boas); o
    # filtro por teto absoluto tem que manter as poucas leituras boas
    hip = [(1790794691.7 + i * 0.05, '99', 8.0, 8.0) for i in range(20)]
    hip += [(t, '1', 2.0, 1.0) for t in [0.0, 0.1, 0.2]]
    gt = [(t, 'pessoa', 2.0, 1.0) for t in [0.0, 0.1, 0.2]]

    resumo = calcular_metricas(hip, gt, limiar_distancia=0.5, tamanho_frame_segundos=0.1)

    assert resumo['num_frames'].iloc[0] == 3
    assert resumo['mota'].iloc[0] == 1.0


def test_calcular_metricas_de_arquivos_le_csv_gravado_pelo_4_1():
    g = Gravador()
    for t in [0.0, 0.1, 0.2]:
        g.registrar_hipotese(t, 1, 2.0, 1.0)
        g.registrar_verdade(t, 'pessoa_detectavel', 2.0, 1.0)

    with tempfile.TemporaryDirectory() as tmp:
        caminho_hip = os.path.join(tmp, 'hipoteses.csv')
        caminho_gt = os.path.join(tmp, 'verdade.csv')
        g.salvar(caminho_hip, caminho_gt)

        resumo = calcular_metricas_de_arquivos(caminho_hip, caminho_gt)

    assert resumo['mota'].iloc[0] == 1.0
    assert resumo['num_matches'].iloc[0] == 3
