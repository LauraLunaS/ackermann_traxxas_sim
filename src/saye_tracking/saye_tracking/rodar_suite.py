"""
Roda a suite inteira de cenarios (submodulo 4.4 da Fase 4 - bancada de avaliacao).

Pressupoe que a simulacao e o pipeline (deteccao+projecao3d+tracker+ponte
de ground truth) ja estao rodando (ver README: "Rodando um cenario
manualmente"). Para cada cenario em `saye_tracking.cenarios.CENARIOS`:
  1. reseta a pose do robo pro spawn (`/world/<mundo>/set_pose`) - sem
     isso, cenarios rodados em sequencia (ex.: "linear" depois de "linear")
     iam comecar de onde o anterior parou, nao do inicio.
  2. sobe um `gravador_node` novo (diretorio de saida proprio do cenario).
  3. roda o `executar_cenario_node` (bloqueia ate o cenario acabar sozinho).
  4. chama o servico `~/salvar` do gravador, derruba o gravador.
  5. calcula as metricas com o `comparador` (4.2) em cima do CSV salvo.
Ao final, formata tudo com `relatorio.formatar_relatorio` (4.4) e imprime.

Sem rclpy direto - orquestra tudo via subprocess (`gz service`, `ros2
launch`, `ros2 service call`) do mesmo jeito que foi validado manualmente
nos submodulos 4.1-4.3, so automatizado. Ver achado do 4.3 no README: antes
de confiar em qualquer resultado, confirme com `ros2 topic info <topico>
-v` que so existe 1 publisher real em cada topico do pipeline.
"""
import argparse
import os
import signal
import subprocess
import time

from saye_tracking.cenarios import CENARIOS, duracao_total
from saye_tracking.comparador import calcular_metricas_de_arquivos
from saye_tracking.relatorio import formatar_relatorio

MUNDO = 'beach_world'
ROBO = 'traxxas'
POSE_SPAWN = (-1.0, 1.0, 0.15)  # ver traxxas_spawn.launch.py


def comando_resetar_pose(mundo, robo, x, y, z):
    """Monta o comando `gz service` que teleporta `robo` de volta pra (x, y, z)."""
    req = (f'name: "{robo}", position: {{x: {x}, y: {y}, z: {z}}}, '
           'orientation: {x: 0, y: 0, z: 0, w: 1}')
    return [
        'gz', 'service', '-s', f'/world/{mundo}/set_pose',
        '--reqtype', 'gz.msgs.Pose', '--reptype', 'gz.msgs.Boolean',
        '--timeout', '2000', '--req', req,
    ]


def _resetar_robo():
    subprocess.run(
        comando_resetar_pose(MUNDO, ROBO, *POSE_SPAWN),
        check=True, capture_output=True)
    time.sleep(1.0)  # deixa a fisica assentar antes de comecar a gravar


def _rodar_um_cenario(nome_cenario, diretorio_base):
    diretorio_saida = os.path.join(diretorio_base, nome_cenario)
    os.makedirs(diretorio_saida, exist_ok=True)

    gravador = subprocess.Popen([
        'ros2', 'launch', 'saye_tracking', 'gravador.launch.py',
        f'diretorio_saida:={diretorio_saida}',
    ])
    time.sleep(2.0)

    subprocess.run([
        'ros2', 'launch', 'saye_tracking', 'cenario.launch.py',
        f'cenario:={nome_cenario}',
    ], check=True, timeout=duracao_total(nome_cenario) + 15.0)

    subprocess.run([
        'ros2', 'service', 'call', '/gravador_node/salvar',
        'std_srvs/srv/Trigger', '{}',
    ], check=True, capture_output=True)

    # SIGTERM no processo do "ros2 launch" nao derruba o gravador_node
    # filho (achado ao vivo: 4 instancias ficaram orfas numa primeira
    # tentativa) - SIGINT e o que "ros2 launch" trata pra cascatear o
    # desligamento, igual Ctrl+C no terminal.
    gravador.send_signal(signal.SIGINT)
    gravador.wait(timeout=5.0)
    time.sleep(1.0)  # evita corrida com o nome "gravador_node" do proximo cenario

    caminho_hipoteses = os.path.join(diretorio_saida, 'hipoteses.csv')
    caminho_verdade = os.path.join(diretorio_saida, 'verdade.csv')
    if not os.path.exists(caminho_hipoteses) or not os.path.exists(caminho_verdade):
        raise RuntimeError(
            f'gravador_node nao salvou os CSVs esperados em {diretorio_saida} '
            f'(cenario "{nome_cenario}") - confira se so havia 1 gravador_node vivo.')

    return calcular_metricas_de_arquivos(caminho_hipoteses, caminho_verdade)


def main():
    parser = argparse.ArgumentParser(
        description='Roda a suite inteira de cenarios (4.4) e imprime o relatorio.')
    parser.add_argument(
        '--diretorio-base', default='/tmp/saye_tracking_suite',
        help='Onde salvar os CSVs de cada cenario (um subdiretorio por cenario).')
    parser.add_argument(
        '--cenarios', nargs='*', default=sorted(CENARIOS.keys()),
        help='Quais cenarios rodar (padrao: todos).')
    args = parser.parse_args()

    resultados = []
    for nome_cenario in args.cenarios:
        print(f'--- rodando cenario "{nome_cenario}" ---')
        _resetar_robo()
        resumo = _rodar_um_cenario(nome_cenario, args.diretorio_base)
        resultados.append((nome_cenario, resumo.iloc[0]))

    print()
    print(formatar_relatorio(resultados))


if __name__ == '__main__':
    main()
