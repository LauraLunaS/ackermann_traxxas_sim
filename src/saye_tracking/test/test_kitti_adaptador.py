"""
Adaptador do KITTI Tracking Benchmark para o Rastreador3D.

Teste exploratorio pedido pelo usuario (nao e um submodulo numerado da
Fase 4; ver README). Sem ROS, sem depender do dataset real baixado - os
dados do KITTI aqui sao fabricados no formato oficial do devkit, so pra
testar o parsing e a logica de adaptacao.
"""
import os
import tempfile

from saye_tracking.kitti_adaptador import (
    filtrar_pedestres, gerar_deteccoes_e_motivos, ler_label_02, ler_velocidade_oxts,
    reescalar_deteccoes, rodar_rastreador, segmentos_carro_parado, verdade_para_csv)
from saye_tracking.rastreador import Rastreador3D


def _linha_label(frame, id_, tipo='Pedestrian', truncado=0.0, ocluido=0, x=0.0, z=10.0):
    # frame id tipo truncado ocluido alpha bb(4) altura largura comprimento x y z rot_y
    return (f'{frame} {id_} {tipo} {truncado} {ocluido} 0.0 '
            f'0 0 50 100 1.7 0.6 0.8 {x} 1.6 {z} 0.0\n')


def _escrever(caminho, linhas):
    with open(caminho, 'w') as arquivo:
        arquivo.writelines(linhas)


def test_ler_label_02_agrupa_por_frame_e_extrai_campos_usados():
    with tempfile.TemporaryDirectory() as tmp:
        caminho = os.path.join(tmp, '0000.txt')
        _escrever(caminho, [
            _linha_label(0, 1, x=2.5, z=9.3, truncado=0.1, ocluido=1),
            _linha_label(0, 2, tipo='Car', x=5.0, z=20.0),
            _linha_label(1, 1, x=2.6, z=9.1),
        ])

        por_frame = ler_label_02(caminho)

        assert set(por_frame.keys()) == {0, 1}
        assert len(por_frame[0]) == 2
        linha_pessoa = next(linha for linha in por_frame[0] if linha['tipo'] == 'Pedestrian')
        assert linha_pessoa == {
            'id': 1, 'tipo': 'Pedestrian', 'truncado': 0.1, 'ocluido': 1, 'x': 2.5, 'z': 9.3}


def test_ler_label_02_ignora_linha_incompleta():
    with tempfile.TemporaryDirectory() as tmp:
        caminho = os.path.join(tmp, '0000.txt')
        _escrever(caminho, ['0 1 Pedestrian 0 0\n', _linha_label(0, 2)])

        por_frame = ler_label_02(caminho)

        assert len(por_frame[0]) == 1
        assert por_frame[0][0]['id'] == 2


def test_filtrar_pedestres_descarta_outros_tipos():
    por_frame = {0: [
        {'id': 1, 'tipo': 'Pedestrian', 'truncado': 0.0, 'ocluido': 0, 'x': 0.0, 'z': 1.0},
        {'id': 2, 'tipo': 'Car', 'truncado': 0.0, 'ocluido': 0, 'x': 0.0, 'z': 1.0},
    ]}

    filtrado = filtrar_pedestres(por_frame)

    assert len(filtrado[0]) == 1
    assert filtrado[0][0]['tipo'] == 'Pedestrian'


def _linha(id_, truncado=0.0, ocluido=0, x=0.0, z=1.0):
    return {
        'id': id_, 'tipo': 'Pedestrian', 'truncado': truncado, 'ocluido': ocluido, 'x': x, 'z': z}


def test_gerar_deteccoes_separa_oclusao_de_saida_de_fov():
    por_frame = {0: [
        _linha(1, ocluido=0),               # visivel
        _linha(2, ocluido=3),               # oclusao real (largamente oculto)
        _linha(3, truncado=0.8),            # saiu do campo de visao
    ]}

    deteccoes, motivos = gerar_deteccoes_e_motivos(por_frame)

    assert [d[0] for d in deteccoes[0]] == [1]
    assert motivos[(0, 2)] == 'oclusao'
    assert motivos[(0, 3)] == 'fov'


def test_gerar_deteccoes_mantem_parcialmente_oculto_como_visivel():
    # ocluido=1 (parcialmente) fica ABAIXO do limiar padrao (OCLUIDO_LARGAMENTE=2)
    por_frame = {0: [_linha(1, ocluido=1)]}

    deteccoes, motivos = gerar_deteccoes_e_motivos(por_frame)

    assert len(deteccoes[0]) == 1
    assert motivos == {}


def test_segmentos_carro_parado_encontra_trecho_continuo_abaixo_do_limiar():
    velocidades = [5.0, 5.0] + [0.1] * 60 + [5.0, 5.0]

    segmentos = segmentos_carro_parado(
        velocidades, limiar_velocidade=0.5, duracao_minima_frames=50)

    assert segmentos == [(2, 61)]


def test_segmentos_carro_parado_descarta_trecho_curto_demais():
    velocidades = [5.0] + [0.1] * 10 + [5.0]  # so 10 frames parado, < duracao_minima

    segmentos = segmentos_carro_parado(
        velocidades, limiar_velocidade=0.5, duracao_minima_frames=50)

    assert segmentos == []


def test_ler_velocidade_oxts_combina_vf_e_vl():
    with tempfile.TemporaryDirectory() as tmp:
        caminho = os.path.join(tmp, '0000.txt')
        campos = ['0.0'] * 30
        campos[8], campos[9] = '3.0', '4.0'  # vf=3, vl=4 -> speed=5
        _escrever(caminho, [' '.join(campos) + '\n'])

        velocidades = ler_velocidade_oxts(caminho)

        assert velocidades == [5.0]


def test_reescalar_deteccoes_preserva_origem_e_encolhe_deslocamento():
    deteccoes = {0: [(1, 0.0, 0.0)], 1: [(1, 2.0, 0.0)]}  # andou 2m em x

    escalado = reescalar_deteccoes(deteccoes, fator=0.5)

    assert escalado[0] == [(1, 0.0, 0.0)]
    assert escalado[1] == [(1, 1.0, 0.0)]  # metade do deslocamento, mesma origem


def test_verdade_para_csv_usa_tempo_pelo_fps_e_formato_tempo_id_x_y():
    por_frame = {0: [_linha(1, x=2.0, z=9.0)], 10: [_linha(1, x=2.1, z=8.9)]}

    verdade = verdade_para_csv(por_frame, fps=10.0)

    assert verdade == [(0.0, '1', 2.0, 9.0), (1.0, '1', 2.1, 8.9)]


def test_rodar_rastreador_mantem_1_id_pra_1_pessoa_sem_buraco():
    # pessoa andando em linha reta, sem nenhum buraco de deteccao
    deteccoes_por_frame = {f: [(1, f * 0.03, 9.0)] for f in range(30)}
    rastreador = Rastreador3D()

    hipoteses = rodar_rastreador(deteccoes_por_frame, rastreador, fps=10.0)

    ids_vistos = {h[1] for h in hipoteses}
    assert len(ids_vistos) == 1


def test_rodar_rastreador_recupera_track_apos_buraco_curto():
    # mesma pessoa, com um buraco de 3 frames (0.3s) no meio - bem abaixo
    # da tolerancia padrao (1.5s) - deve recuperar com o MESMO id
    pontos_por_frame = {f: (1, f * 0.03, 9.0) for f in range(30)}
    deteccoes_por_frame = {
        f: ([pontos_por_frame[f]] if f not in (14, 15, 16) else [])
        for f in pontos_por_frame
    }
    rastreador = Rastreador3D()

    hipoteses = rodar_rastreador(deteccoes_por_frame, rastreador, fps=10.0)

    ids_vistos = {h[1] for h in hipoteses}
    assert len(ids_vistos) == 1
