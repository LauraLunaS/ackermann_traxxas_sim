#!/usr/bin/env python3
"""
Avalia o Rastreador3D contra pedestres reais do KITTI (carro parado).

Trechos de carro PARADO - sem conversao de ego-motion, ver README.
Nao e um submodulo numerado da Fase 4 - e um teste exploratorio pedido
pelo usuario, decoupled da deteccao/Gazebo: alimenta o `Rastreador3D`
direto com as posicoes do gabarito do KITTI (como a validacao 3.8 fez com
os obstaculos do Gazebo), com buracos de deteccao tirados dos campos REAIS
de oclusao/truncamento do KITTI (nao sorteio aleatorio). Sem ROS.

Protocolo (ver README):
  1. Escolhe, por sequencia, o trecho mais longo com o carro parado E com
     mais pedestres (sem isso, teria que compensar ego-motion via oxts -
     fora do escopo desta etapa).
  2. Calibra `velocidade_maxima_esperada`/`margem_gate_recuperacao` SO na
     sequencia de AJUSTE (--sequencia-ajuste) - nunca nas de medicao.
     Esses valores ficam congelados em `config/tracker_kitti_parado.yaml`,
     SEPARADO do perfil padrao do simulador (que nao e alterado).
  3. Mede nas sequencias de MEDICAO (--sequencias-medicao), comparando o
     perfil padrao do simulador com o perfil do KITTI.

Uso:
    python3 avaliar_kitti_parado.py --kitti-dir /caminho/pra/training
"""
import argparse
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from saye_tracking.comparador import calcular_metricas  # noqa: E402
from saye_tracking.kitti_adaptador import (  # noqa: E402
    filtrar_pedestres, gerar_deteccoes_e_motivos, ler_label_02, ler_velocidade_oxts,
    rodar_rastreador, segmentos_carro_parado)
from saye_tracking.rastreador import Rastreador3D  # noqa: E402
import yaml  # noqa: E402

FPS = 10.0  # taxa nativa do KITTI tracking


def _melhor_segmento_parado(kitti_dir, seq):
    """Entre os trechos de carro parado da sequencia, devolve o mais denso de pedestres."""
    velocidades = ler_velocidade_oxts(os.path.join(kitti_dir, 'oxts', f'{seq}.txt'))
    segmentos = segmentos_carro_parado(
        velocidades, limiar_velocidade=0.5, duracao_minima_frames=30)
    if not segmentos:
        return None

    pedestres = filtrar_pedestres(ler_label_02(os.path.join(kitti_dir, 'label_02', f'{seq}.txt')))

    def _media_pedestres(inicio, fim):
        contagens = [len(pedestres.get(f, [])) for f in range(inicio, fim + 1)]
        return sum(contagens) / len(contagens)

    inicio, fim = max(segmentos, key=lambda s: _media_pedestres(*s))
    return inicio, fim, pedestres


def _velocidade_real(pedestres, inicio, fim):
    """Velocidade frame-a-frame (m/s) de cada id, so entre frames consecutivos."""
    pos_por_id = {}
    velocidades = []
    for f in range(inicio, fim + 1):
        for linha in pedestres.get(f, []):
            id_ = linha['id']
            if id_ in pos_por_id:
                f_ant, x_ant, z_ant = pos_por_id[id_]
                if f - f_ant == 1:
                    dist = ((linha['x'] - x_ant) ** 2 + (linha['z'] - z_ant) ** 2) ** 0.5
                    velocidades.append(dist * FPS)
            pos_por_id[id_] = (f, linha['x'], linha['z'])
    return velocidades


def _verdade_csv(pedestres, inicio, fim):
    linhas = []
    for f in range(inicio, fim + 1):
        tempo = f / FPS
        for linha in pedestres.get(f, []):
            linhas.append((tempo, str(linha['id']), linha['x'], linha['z']))
    return linhas


def _carregar_perfil_kitti(caminho_yaml):
    with open(caminho_yaml) as arquivo:
        params = yaml.safe_load(arquivo)['tracker_node']['ros__parameters']
    return {
        'velocidade_maxima_esperada': params['velocidade_maxima_esperada'],
        'margem_gate_recuperacao': params['margem_gate_recuperacao'],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        '--kitti-dir', default=os.path.expanduser('~/ackermann_sim/data/kitti_tracking/training'),
        help='pasta "training/" do KITTI tracking (contem label_02/ e oxts/)')
    ap.add_argument('--sequencia-ajuste', default='0017')
    ap.add_argument('--sequencias-medicao', nargs='+', default=['0016', '0019'])
    ap.add_argument(
        '--perfil-kitti',
        default=os.path.join(
            os.path.dirname(__file__), '..', 'config', 'tracker_kitti_parado.yaml'))
    args = ap.parse_args()

    # --- passo 2: confere a calibracao (so informativo - os valores usados
    # de verdade ja estao congelados no --perfil-kitti) --------------------
    inicio_aj, fim_aj, pedestres_aj = _melhor_segmento_parado(
        args.kitti_dir, args.sequencia_ajuste)
    velocidades_aj = _velocidade_real(pedestres_aj, inicio_aj, fim_aj)
    print(f'Sequencia de ajuste {args.sequencia_ajuste} [{inicio_aj}-{fim_aj}]: '
          f'mediana={statistics.median(velocidades_aj):.2f} m/s '
          f'p90={sorted(velocidades_aj)[int(0.9 * len(velocidades_aj))]:.2f} m/s '
          f'max={max(velocidades_aj):.2f} m/s (n={len(velocidades_aj)})')

    perfil_kitti = _carregar_perfil_kitti(args.perfil_kitti)
    gate_maximo_kitti = (
        perfil_kitti['velocidade_maxima_esperada'] * 1.5 + perfil_kitti['margem_gate_recuperacao'])
    print(f'Perfil KITTI ({args.perfil_kitti}): {perfil_kitti} '
          f'-> gate_maximo_recuperacao = {gate_maximo_kitti:.2f} m '
          f'(tolerancia_perdido_segundos padrao, 1.5s)\n')

    # --- passo 3: mede nas sequencias de medicao ---------------------------
    print(f'{"seq":>5} {"perfil":>12} {"mota":>7} {"idf1":>7} {"switches":>8} '
          f'{"fp":>4} {"misses":>7} {"motp(m2)":>9}')
    for seq in args.sequencias_medicao:
        resultado = _melhor_segmento_parado(args.kitti_dir, seq)
        if resultado is None:
            print(f'  {seq}: nenhum trecho de carro parado encontrado, pulando')
            continue
        inicio, fim, pedestres = resultado

        deteccoes, motivos = gerar_deteccoes_e_motivos(pedestres)
        deteccoes = {f: deteccoes[f] for f in deteccoes if inicio <= f <= fim}
        verdade_csv = _verdade_csv(pedestres, inicio, fim)
        n_oclusao = sum(
            1 for (f, _), m in motivos.items() if inicio <= f <= fim and m == 'oclusao')
        n_fov = sum(1 for (f, _), m in motivos.items() if inicio <= f <= fim and m == 'fov')

        for nome_perfil, kwargs in (
                ('padrao_sim', {}),
                ('kitti_parado', perfil_kitti)):
            rastreador = Rastreador3D(**kwargs)
            hipoteses = rodar_rastreador(deteccoes, rastreador, fps=FPS)
            m = calcular_metricas(hipoteses, verdade_csv)
            mota, idf1, motp = m['mota'].iloc[0], m['idf1'].iloc[0], m['motp'].iloc[0]
            switches = int(m['num_switches'].iloc[0])
            fp = int(m['num_false_positives'].iloc[0])
            misses = int(m['num_misses'].iloc[0])
            print(f'{seq:>5} {nome_perfil:>12} {mota:>7.3f} {idf1:>7.3f} '
                  f'{switches:>8} {fp:>4} {misses:>7} {motp:>9.4f}')
        print(f'  ({seq} [{inicio}-{fim}]: {n_oclusao} buracos por oclusao real, '
              f'{n_fov} por saida de FOV)')

    print('\nNotas: motp esta em METROS QUADRADOS (comparador.py usa '
          'norm2squared_matrix) - nao e erro linear direto, precisa de raiz '
          'quadrada pra virar metros. fp = 0 em toda rodada aqui POR '
          'CONSTRUCAO: as "deteccoes" vem direto do gabarito (sem detector '
          'real), entao todo ponto alimentado ao rastreador corresponde a '
          'uma pessoa de verdade - este teste nao avalia rejeicao de falso '
          'positivo de um detector, so a logica de associacao/recuperacao.')


if __name__ == '__main__':
    main()
