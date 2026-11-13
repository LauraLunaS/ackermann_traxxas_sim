#!/usr/bin/env python3
"""
Valida a compensacao de ego-motion (passo 5) com carros ESTACIONADOS.

A aproximacao de `kitti_ego_motion.py` ignora o braco de alavanca
camera-IMU (sem os arquivos de calibracao do KITTI). Esta validacao
confere se isso e bom o bastante: depois de compensar o movimento do
proprio carro, um carro REALMENTE estacionado deveria ficar numa posicao
~constante no mundo - exatamente o mesmo teste que a fase 2.3 fez contra
o `/odom` do robo (so que aqui, sem rotulo de "estacionado", a evidencia e
estatistica: a maioria dos carros de rua, na pratica, esta parada).

Uso:
    python3 validar_ego_motion_kitti.py --kitti-dir /caminho/pra/training --sequencia 0011
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from saye_tracking.kitti_adaptador import ler_label_02  # noqa: E402
from saye_tracking.kitti_ego_motion import (  # noqa: E402
    ler_pose_oxts, ponto_camera_para_mundo, pose_para_enu)

DURACAO_MINIMA_FRAMES = 50


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        '--kitti-dir', default=os.path.expanduser('~/ackermann_sim/data/kitti_tracking/training'))
    ap.add_argument('--sequencia', default='0011')
    args = ap.parse_args()

    poses_oxts = ler_pose_oxts(os.path.join(args.kitti_dir, 'oxts', f'{args.sequencia}.txt'))
    poses_enu = pose_para_enu(poses_oxts)
    por_frame = ler_label_02(os.path.join(args.kitti_dir, 'label_02', f'{args.sequencia}.txt'))

    v_ego = [
        ((poses_enu[i + 1][0] - poses_enu[i][0]) ** 2
         + (poses_enu[i + 1][1] - poses_enu[i][1]) ** 2) ** 0.5 * 10.0
        for i in range(len(poses_enu) - 1)
    ]
    print(f'Sequencia {args.sequencia}: velocidade do ego (apos compensacao) '
          f'media={sum(v_ego) / len(v_ego):.2f} m/s max={max(v_ego):.2f} m/s '
          f'({len(poses_enu)} frames)')

    carros_por_id = {}
    for frame, linhas in por_frame.items():
        if frame >= len(poses_enu):
            continue
        for linha in linhas:
            if linha['tipo'] != 'Car':
                continue
            x_mundo, y_mundo = ponto_camera_para_mundo(
                linha['x'], linha['z'], poses_enu[frame])
            carros_por_id.setdefault(linha['id'], []).append((frame, x_mundo, y_mundo))

    velocidades_residuais = []
    for id_, pontos in carros_por_id.items():
        if len(pontos) < DURACAO_MINIMA_FRAMES:
            continue
        pontos.sort()
        deslocamentos = [
            ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 * 10.0 / max(1, f1 - f0)
            for (f0, x0, y0), (f1, x1, y1) in zip(pontos, pontos[1:])
        ]
        velocidade_mediana = sorted(deslocamentos)[len(deslocamentos) // 2]
        velocidades_residuais.append((id_, len(pontos), velocidade_mediana))

    velocidades_residuais.sort(key=lambda t: t[2])
    n_parados = sum(1 for _, _, v in velocidades_residuais if v < 0.5)
    print(f'{len(velocidades_residuais)} carros de vida longa (>={DURACAO_MINIMA_FRAMES} '
          f'frames) apos compensacao - {n_parados} com velocidade residual mediana < 0.5 m/s '
          f'(provavelmente estacionados):\n')
    print(f'{"id":>5} {"n_frames":>9} {"v_residual_mediana(m/s)":>24}')
    for id_, n_frames, v in velocidades_residuais:
        print(f'{id_:>5} {n_frames:>9} {v:>24.3f}')


if __name__ == '__main__':
    main()
