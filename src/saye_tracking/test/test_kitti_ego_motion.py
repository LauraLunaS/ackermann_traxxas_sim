"""
Compensacao de ego-motion do KITTI (passo 5) - testes puros de geometria.

Nao testam se a aproximacao (sem arquivos de calibracao) bate com a
realidade - isso e validado com dados reais (carros estacionados) em
`scripts/validar_ego_motion_kitti.py`, fora do escopo deste arquivo.
"""
import math
import os
import tempfile

from saye_tracking.kitti_ego_motion import (
    ler_pose_oxts, ponto_camera_para_mundo, pose_para_enu)


def _linha_oxts(lat=0.0, lon=0.0, alt=0.0, roll=0.0, pitch=0.0, yaw=0.0):
    campos = [str(lat), str(lon), str(alt), str(roll), str(pitch), str(yaw)] + ['0.0'] * 24
    return ' '.join(campos) + '\n'


def test_ler_pose_oxts_extrai_lat_lon_alt_roll_pitch_yaw():
    with tempfile.TemporaryDirectory() as tmp:
        caminho = os.path.join(tmp, '0000.txt')
        with open(caminho, 'w') as arquivo:
            arquivo.write(_linha_oxts(lat=49.0, lon=8.4, alt=112.0, yaw=1.2))

        poses = ler_pose_oxts(caminho)

        assert poses == [
            {'lat': 49.0, 'lon': 8.4, 'alt': 112.0, 'roll': 0.0, 'pitch': 0.0, 'yaw': 1.2}]


def test_pose_para_enu_fica_na_origem_quando_carro_nao_se_move():
    poses = [{'lat': 49.0, 'lon': 8.4, 'alt': 0.0, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0}] * 5

    enu = pose_para_enu(poses)

    for x, y, yaw in enu:
        assert abs(x) < 1e-9
        assert abs(y) < 1e-9
        assert yaw == 0.0


def test_pose_para_enu_desloca_proporcional_ao_lon_quando_carro_anda_pro_leste():
    # mesma latitude, longitude crescente -> deslocamento so em x (leste)
    poses = [
        {'lat': 49.0, 'lon': 8.4, 'alt': 0.0, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0},
        {'lat': 49.0, 'lon': 8.4001, 'alt': 0.0, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0},
    ]

    enu = pose_para_enu(poses)

    x0, y0, _ = enu[0]
    x1, y1, _ = enu[1]
    assert x0 == 0.0 and y0 == 0.0
    assert x1 > 5.0  # ~0.0001 grau de longitude a 49N e da ordem de 7-8m
    assert abs(y1) < 1e-6  # nao deveria deslocar em y so mudando longitude


def test_ponto_camera_para_mundo_sem_rotacao_so_soma_posicao_do_ego():
    # yaw=0 (convencao do oxts, igual ao angulo padrao, medido do eixo x):
    # "pra frente" (z_cam) cai no eixo x do mundo
    pose_ego = (10.0, 5.0, 0.0)

    x_mundo, y_mundo = ponto_camera_para_mundo(x_cam=0.0, z_cam=3.0, pose_ego=pose_ego)

    assert x_mundo == 13.0  # 10 + 3 (pra frente)
    assert y_mundo == 5.0


def test_ponto_camera_para_mundo_roda_90_graus_troca_frente_por_lateral():
    pose_ego = (0.0, 0.0, math.pi / 2)  # carro virado 90 graus (agora "pra frente" = eixo y)

    x_mundo, y_mundo = ponto_camera_para_mundo(x_cam=0.0, z_cam=1.0, pose_ego=pose_ego)

    assert abs(x_mundo - 0.0) < 1e-9
    assert abs(y_mundo - 1.0) < 1e-9


def test_ponto_camera_para_mundo_pessoa_parada_no_frame_camera_segue_o_ego():
    # pessoa sempre na MESMA posicao relativa a camera (parada em relacao
    # ao carro) enquanto o carro anda pra frente (eixo x, yaw=0) - no
    # mundo, ela tem que "andar" junto com o carro (mesma distancia
    # percorrida pelo ego)
    pontos_mundo = [
        ponto_camera_para_mundo(0.0, 5.0, (x_ego, 0.0, 0.0))
        for x_ego in (0.0, 1.0, 2.0)
    ]

    deslocamentos_x = [b[0] - a[0] for a, b in zip(pontos_mundo, pontos_mundo[1:])]
    assert deslocamentos_x == [1.0, 1.0]
    ys = [p[1] for p in pontos_mundo]
    assert ys == [0.0, 0.0, 0.0]
