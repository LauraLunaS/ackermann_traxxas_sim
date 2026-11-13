"""
Compensacao de ego-motion do KITTI (passo 5 - trechos com o carro andando).

Sem o carro parado (ver `kitti_adaptador.py`), a posicao de um pedestre no
frame da camera muda tanto pelo movimento dele quanto pelo movimento do
proprio carro - pra comparar com o rastreador (que opera num frame fixo,
`odom`), precisa compor a pose do carro ao longo do tempo (do `oxts`) com
a posicao relativa a camera.

Aproximacao assumida aqui (sem os arquivos de calibracao do KITTI -
`calib_imu_to_velo`/`calib_velo_to_cam` - que nao foram baixados): o eixo
da camera e tratado como alinhado com o eixo do carro (braco de alavanca
camera-IMU ignorado). Isso E uma aproximacao, nao a conversao exata do
devkit oficial - por isso o passo seguinte (nao neste modulo) e validar
com carros ESTACIONADOS reais: se a posicao deles sair constante apos a
compensacao, a aproximacao e boa o bastante; se nao, precisa dos arquivos
de calibracao de verdade.

Projecao usada pra converter lat/lon em metros locais: Mercator
equiretangular do proprio devkit oficial do KITTI (`convertOxtsToPose`),
relativa ao 1o frame da sequencia.
"""
import math

RAIO_TERRA_WGS84 = 6378137.0


def ler_pose_oxts(caminho):
    """
    Le um `oxts/<seq>.txt` e devolve lat/lon/alt/roll/pitch/yaw por frame.

    1 dict por linha (1 frame), campos 0-5 do devkit oficial.
    """
    poses = []
    with open(caminho) as arquivo:
        for linha in arquivo:
            campos = linha.split()
            poses.append({
                'lat': float(campos[0]), 'lon': float(campos[1]), 'alt': float(campos[2]),
                'roll': float(campos[3]), 'pitch': float(campos[4]), 'yaw': float(campos[5]),
            })
    return poses


def _projetar_mercator(lat, lon, escala):
    mx = escala * lon * math.pi * RAIO_TERRA_WGS84 / 180.0
    my = escala * RAIO_TERRA_WGS84 * math.log(math.tan((90.0 + lat) * math.pi / 360.0))
    return mx, my


def pose_para_enu(poses):
    """
    Pose local 2D (x, y, yaw) de cada frame, relativa ao 1o (lat/lon/yaw).

    Mesma projecao de Mercator do devkit oficial do KITTI
    (`convertOxtsToPose`) - x/y em metros, origem no 1o frame da
    sequencia.
    """
    escala = math.cos(poses[0]['lat'] * math.pi / 180.0)
    x0, y0 = _projetar_mercator(poses[0]['lat'], poses[0]['lon'], escala)

    resultado = []
    for p in poses:
        x, y = _projetar_mercator(p['lat'], p['lon'], escala)
        resultado.append((x - x0, y - y0, p['yaw']))
    return resultado


def ponto_camera_para_mundo(x_cam, z_cam, pose_ego):
    """
    Transforma um ponto no chao (frame da camera) pro frame mundo (ENU local).

    `pose_ego` e `(x, y, yaw)` do carro nesse frame (ver `pose_para_enu`).
    Convencao da camera do KITTI: `x_cam` lateral (direita), `z_cam` pra
    frente - alinhados aqui com o eixo do carro (braco de alavanca
    camera-IMU ignorado, ver docstring do modulo).
    """
    x_ego, y_ego, yaw = pose_ego
    cos_yaw, sin_yaw = math.cos(yaw), math.sin(yaw)
    dx = cos_yaw * z_cam - sin_yaw * x_cam
    dy = sin_yaw * z_cam + cos_yaw * x_cam
    return x_ego + dx, y_ego + dy
