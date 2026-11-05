"""
Bancada de avaliacao multi-pessoa (submodulo 4.9).

Estende a bancada original (4.1-4.4, 1 pessoa estatica + robo se movendo)
pro cenario que o projeto realmente precisa validar: VARIAS pessoas
andando (Fase 4.6) + o robo podendo tambem estar parado OU andando. Pra
cada combinacao de (quantidade de pessoas) x (robo parado/andando):

  1. estaciona TODOS os quadros de TODOS os atores (limpa qualquer "gente
     fantasma" parada de um teste anterior - ver achado abaixo).
  2. reseta a pose do robo pro spawn E limpa o estado interno do
     `tracker_node` (servico `~/resetar`, novo nesta fase - ver achado
     sobre contaminacao entre testes, abaixo).
  3. sobe os `mover_pessoa_animada_node` SO dos N primeiros atores de
     `config/atores.yaml` (sempre os mesmos N primeiros, na mesma ordem -
     e isso que garante que a trajetoria de cada pessoa e IDENTICA entre
     testes com quantidades diferentes: a pessoa_1 no teste de 1 pessoa
     anda exatamente a mesma trajetoria que a pessoa_1 no teste de 3).
  4. espera 1s assentar, sobe o `gravador_atores_node` (verdade analitica,
     4.9) so para esses N atores.
  5. roda o roteiro de velocidade do robo (`executar_cenario_node`, 3.3),
     usando os cenarios `parado_pessoas`/`andando_pessoas` (`cenarios.py`,
     30s cada - bem mais longo que os cenarios originais de 1 pessoa
     estatica, pra dar tempo dos atores percorrerem boa parte do caminho
     deles) - mesma razao do item 3, agora pro lado do robo: cenario fixo
     e identico em toda combinacao de quantidade de pessoas.
  6. salva, derruba movers+gravador, calcula metricas (`comparador`, 4.2).

Achado (ao projetar isto): os atores com flipbook (4.6) ja vem SPAWNADOS
no `simple_world.sdf` (o quadro 0 de cada um, parado num pose default) -
se um teste usa so 1 das 3 pessoas, as outras 2 ficariam visiveis e
PARADAS na cena, contaminando a deteccao com "gente fantasma" que nunca
deveria estar ali. Por isso o passo 1 estaciona (teleporta pra
`Z_ESTACIONADO`) TODO quadro de TODO ator antes de cada combinacao, e so
religa os N que o teste atual precisa.

Achado 2 (o mais caro de achar): o `tracker_node` e um processo de vida
longa, compartilhado por TODA a bateria de testes (nunca reiniciado entre
combinacoes). Sem limpar o estado dele, um track `PERDIDO` de uma
combinacao anterior (com atores/posicoes DIFERENTES) pode sobreviver
(dentro de `tolerancia_perdido_segundos`) ate a proxima combinacao
comecar, e ser "recuperado" (OCR) por engano contra a cena NOVA -
contaminando a gravacao com hipoteses que nao correspondem a nenhum ator
do teste atual. Confirmado ao vivo, rodando a bancada inteira 2 vezes: o
MOTA de uma MESMA combinacao variou de -0.16 a 0.55 entre as rodadas, e
QUAL combinacao "dava errado" mudava de uma rodada pra outra - sintoma
classico de contaminacao entre testes (ordem-dependente), nao de uma
dificuldade real e repetivel de alguma combinacao especifica. Corrigido
chamando `/tracker_node/resetar` (servico novo, `TrackerNode.
callback_resetar`) no passo 2, antes de cada combinacao.

Achado 3 (depois do 4.7/4.8, investigando a instabilidade residual dos
testes "andando" que sobrou mesmo apos o Achado 2 acima - MOTA ainda
variando entre -0.09 e 0.60 em rodadas diferentes): a suspeita inicial
era o bug ja documentado de timestamp de camera (`gravador_node.py`,
"Achado 3" de la - `header.stamp` as vezes vem com relogio de parede, e
pioraria com o robo andando). Testado DIRETO (no sim rodando, comparando
`/clock` com `header.stamp` da imagem, parado e andando, sozinho e com 3
atores andando junto - carga real da bancada) e NAO reproduziu: maior
diferenca vista foi 24ms, sempre dentro do esperado. **Esse bug nao e a
causa aqui** (pode ter sido corrigido por uma atualizacao do ros_gz desde
que foi documentado, ou ser mais raro do que o registro original sugeria -
de qualquer forma, nao e o que afeta esta bancada).

A causa real, achada ao reproduzir sem querer: teleportar a pose do robo
(`comando_resetar_pose`) NAO para as rodas - se `/cmd_vel` ficou com um
valor diferente de zero de uma combinacao anterior (ex.: o cenario foi
interrompido antes de publicar o Twist zero final que `executar_cenario_
node` publica ao terminar normalmente), o robo continua obedecendo esse
comando velho mesmo depois de teleportado pro spawn - e pode ir parar
longe de qualquer ator. Reproduzido ao vivo: um /cmd_vel residual levou o
robo pra (-2.4, 9.1) e a deteccao ficou 100% vazia (0 de 300 mensagens)
ate ser corrigido. Corrigido publicando um Twist zero ANTES de resetar a
pose, toda combinacao (nao so no fim do cenario anterior).

Robo "andando": avanca bem devagar (0.1 m/s) por toda a duracao do teste -
rapido o bastante pra testar o robo em movimento, devagar o bastante pra
nao sair da zona onde as pessoas andam nem percorrer alem do mundo
(ao fim de 30s, ~3m, terminando perto do centro da area onde os atores
circulam - ver `config/atores.yaml`).

Achado 4 (correcao de movimentacao, pos-4.9): o antigo `mover_pessoa_
animada_node` subia 1 PROCESSO POR ATOR, cada um com seu proprio cliente
gz-transport chamando `/world/<mundo>/set_pose` concorrentemente - sob essa
concorrencia, um dos clientes podia passar a falhar 100% das chamadas pelo
resto do teste, SEM AVISO (o retorno de `request()` era descartado sem
checar). O sintoma: um ator "congelado" no pose de estacionamento durante
parte do teste, contaminando a verdade com uma posicao que nunca existiu -
indistinguivel, ao olhar so pro MOTA final, de uma troca de id real do
rastreador (foi exatamente essa confusao que motivou reabrir a
investigacao das "trocas de id com o robo parado"). Corrigido trocando por
1 SO processo (`mover_pessoas_node`) que move TODOS os atores do teste numa
unica chamada de `set_pose_vector` por tick (ver `gz_pose_vector.py` pro
achado completo) - e a verdade gravada (`gravador_atores_node`) passou a
ler a posicao REAL/medida do Gazebo em vez de recalcular pela formula, pra
qualquer falha futura aparecer como "ator parado" na propria verdade, nunca
mais mascarada.

Checagens de validade (item 2 do roteiro pos-correcao, `validacao_
bancada.py`): nenhum dos achados 1-4 acima foi pego OLHANDO O MOTA - foi
pego reproduzindo o problema ao vivo e comparando com a pose real do
Gazebo, por fora da bancada. Pra um bug assim nao passar batido de novo
(contaminando silenciosamente uma media futura), toda combinacao agora
confere, ANTES de calcular metricas: (1) cada ator andou pelo menos uma
fracao da distancia esperada (`checar_atores_andaram` - pega o proprio
achado 4 e qualquer regressao futura parecida); (2) o robo comecou a
gravacao perto do spawn e praticamente parado (`checar_robo_comecou_
no_spawn` - pega o achado 3); (3) o servico `/tracker_node/resetar`
confirmou sucesso (nao so que a chamada CLI nao deu erro - achado 2).
Uma combinacao que falhe qualquer checagem levanta excecao e e tratada
pelo `main()` como qualquer outra falha (impressa, excluida do relatorio).

Sem rclpy direto - orquestra tudo via subprocess, mesmo estilo de
`rodar_suite.py` (4.4).
"""
import argparse
import os
import signal
import subprocess
import time

from ament_index_python.packages import get_package_share_directory
from saye_tracking.cenarios import duracao_total
from saye_tracking.comparador import calcular_metricas_de_arquivos
from saye_tracking.gravador import carregar_csv, carregar_robo_csv
from saye_tracking.gz_pose_vector import TeleportadorEmLote
from saye_tracking.rodar_suite import comando_resetar_pose, MUNDO, POSE_SPAWN, ROBO
from saye_tracking.validacao_bancada import checar_atores_andaram, checar_robo_comecou_no_spawn
import yaml

Z_ESTACIONADO = -50.0

# nome do ator (robo parado/andando) -> cenario de cenarios.py a usar
ROBO_CENARIOS = {
    'parado': 'parado_pessoas',
    'andando': 'andando_pessoas',
}

QUANTIDADES_PESSOAS = [1, 2, 3]


def _caminho_atores_yaml():
    # instalado (ros2 run): config/ fica em share/saye_tracking/, NAO ao
    # lado deste arquivo .py (que vai pra site-packages/saye_tracking/) -
    # diferente de um .launch.py, que e copiado pro MESMO share/saye_tracking/
    # que o config/ (por isso so os launch files usam o truque de caminho
    # relativo). Cai pro caminho relativo so se o pacote nao estiver instalado
    # (ex.: rodando os testes direto do source, sem colcon build).
    try:
        return os.path.join(get_package_share_directory('saye_tracking'), 'config', 'atores.yaml')
    except Exception:
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'atores.yaml')


CAMINHO_ATORES_YAML = _caminho_atores_yaml()

COLUNAS_RELATORIO = [
    'n_pessoas', 'robo', 'num_frames', 'mota', 'motp',
    'num_switches', 'num_false_positives', 'num_misses', 'num_matches',
]


def _carregar_atores():
    with open(CAMINHO_ATORES_YAML, encoding='utf-8') as f:
        return yaml.safe_load(f)['atores']


def _estacionar_todos_os_atores(atores):
    """
    Teleporta TODO quadro de TODO ator pra bem longe - limpa a cena.

    1 SO chamada de `set_pose_vector` pra todos os quadros de todos os
    atores (ate 3 atores x ~30 quadros = ~90 poses de uma vez), em vez da
    versao antiga (1 chamada de `set_pose` por quadro, via subprocess `gz
    service` - ~90 processos novos por combinacao da bancada, lento e
    sujeito ao mesmo tipo de falha silenciosa documentado em
    `gz_pose_vector.py`). Falha aqui e logada (nao e so cosmetico: se a
    cena nao for limpa de verdade, o teste seguinte comeca contaminado com
    "gente fantasma" - acha do 1 original desta bancada).
    """
    poses = [
        (f"{ator['prefixo_modelo']}{i}", 0.0, 0.0, Z_ESTACIONADO, 0.0)
        for ator in atores
        for i in range(int(ator['n_quadros']))
    ]
    teleportador = TeleportadorEmLote(MUNDO, timeout_ms=3000)
    ok, sucesso = teleportador.teleportar(poses)
    if not sucesso:
        print(
            f'  aviso: falha ao estacionar {len(poses)} quadro(s) via '
            f'"{teleportador.servico}" (resposta recebida={ok}) - a cena '
            f'pode ter "gente fantasma" de um teste anterior.')


def _comando_mover_pessoas(atores_deste_teste, nome_no):
    nomes_str = '[' + ','.join(a['nome'] for a in atores_deste_teste) + ']'
    return [
        'ros2', 'run', 'saye_tracking', 'mover_pessoas_node',
        '--ros-args',
        '-r', f'__node:={nome_no}',
        '-p', 'use_sim_time:=true',
        '-p', f'atores_yaml:={CAMINHO_ATORES_YAML}',
        '-p', f'nomes_atores:={nomes_str}',
        '-p', 'taxa_hz:=30.0',
    ]


def _comando_executar_cenario(nome_cenario):
    return [
        'ros2', 'run', 'saye_tracking', 'executar_cenario_node',
        '--ros-args',
        '-p', 'use_sim_time:=true',
        '-p', f'cenario:={nome_cenario}',
    ]


def _popen_em_grupo_proprio(comando):
    """
    Sobe `comando` no PROPRIO grupo de processo (pra poder derrubar inteiro).

    O PID que `Popen` devolve e o do WRAPPER `ros2 run`, nao do no rclpy de
    verdade - mandar SIGINT so nesse PID nem sempre cascateia a tempo
    (confirmado ao vivo: `wait(timeout=5.0)` estourou, mas SIGINT direto no
    PID do no real matou na hora). `start_new_session=True` poe o wrapper
    E qualquer filho dele no MESMO grupo de processo novo, pra
    `_encerrar_processo` poder sinalizar o grupo inteiro de uma vez
    (`os.killpg`), sem precisar descobrir o PID do filho.
    """
    return subprocess.Popen(comando, start_new_session=True)


def _encerrar_processo(proc, nome, timeout=8.0):
    """
    Encerra `proc` (e todo o grupo dele) sem nunca lancar excecao.

    Tenta SIGINT no grupo inteiro primeiro (desligamento limpo do rclpy -
    ver achado ja documentado em `rodar_suite.py`/CLAUDE.md: so SIGINT
    cascateia, nao SIGTERM); se nao morrer dentro de `timeout`, cai pra
    SIGKILL no grupo. Um combinacao travada no desligamento NAO pode
    derrubar o resto da bancada - so os processos orfaos de UM teste.
    """
    if proc.poll() is not None:
        return  # ja morreu sozinho
    try:
        pgid = os.getpgid(proc.pid)
        os.killpg(pgid, signal.SIGINT)
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f'  aviso: "{nome}" nao morreu com SIGINT em {timeout}s, forcando SIGKILL')
        try:
            os.killpg(pgid, signal.SIGKILL)
            proc.wait(timeout=5.0)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            pass
    except ProcessLookupError:
        pass  # grupo ja nao existe mais


def _rodar_uma_combinacao(n_pessoas, nome_robo, atores, diretorio_saida):
    os.makedirs(diretorio_saida, exist_ok=True)
    atores_deste_teste = atores[:n_pessoas]
    nomes = [a['nome'] for a in atores_deste_teste]
    nome_cenario = ROBO_CENARIOS[nome_robo]

    _estacionar_todos_os_atores(atores)
    # zera /cmd_vel ANTES de resetar a pose - achado ao vivo (investigacao
    # pos-4.9): teleportar a pose NAO para as rodas. Se o cenario anterior
    # terminou de forma anormal (timeout, crash) sem publicar o Twist zero
    # final que `executar_cenario_node` publica ao concluir normalmente,
    # o robo continua obedecendo o ultimo /cmd_vel recebido mesmo depois
    # de teleportado - reproduzido na pratica: um /cmd_vel residual levou
    # o robo pra (-2.4, 9.1), longe de qualquer ator, e a deteccao ficou
    # 100% vazia (0 de 300 mensagens) ate ser corrigido. Provavel causa
    # real da instabilidade vista nos testes "andando" da bancada - NAO
    # era o bug de timestamp de camera (testado direto, nao reproduziu).
    subprocess.run(
        ['ros2', 'topic', 'pub', '-1', '/cmd_vel', 'geometry_msgs/msg/Twist', '{}'],
        capture_output=True)
    subprocess.run(comando_resetar_pose(MUNDO, ROBO, *POSE_SPAWN), check=True, capture_output=True)
    # limpa o estado interno do tracker_node - ver docstring de
    # `TrackerNode.callback_resetar` (achado desta bancada: sem isso, um
    # track "perdido" de uma combinacao anterior pode contaminar a proxima).
    # `check=True` so confere que a CHAMADA CLI nao deu erro - NAO que o
    # Trigger respondeu sucesso=True (checagem 3 do item 2: sem ela, um
    # reset que falhasse dentro do callback, sem crashar o processo
    # `ros2 service call`, passaria batido, igual os achados 1/4).
    resposta_reset = subprocess.run([
        'ros2', 'service', 'call', '/tracker_node/resetar', 'std_srvs/srv/Trigger', '{}',
    ], check=True, capture_output=True, text=True)
    if 'success=True' not in resposta_reset.stdout:
        raise RuntimeError(
            f'reset do tracker_node nao confirmou sucesso: {resposta_reset.stdout.strip()!r}')
    time.sleep(1.0)

    processo_mover = _popen_em_grupo_proprio(
        _comando_mover_pessoas(atores_deste_teste, 'mover_pessoas_teste_node'))
    time.sleep(1.0)  # deixa a 1a teleportacao assentar antes de gravar

    gravador = _popen_em_grupo_proprio([
        'ros2', 'run', 'saye_tracking', 'gravador_atores_node',
        '--ros-args',
        '-p', 'use_sim_time:=true',
        '-p', f'atores_yaml:={CAMINHO_ATORES_YAML}',
        '-p', 'nomes_atores:=' + '[' + ','.join(nomes) + ']',
        '-p', f'diretorio_saida:={diretorio_saida}',
    ])
    time.sleep(1.0)

    try:
        subprocess.run(
            _comando_executar_cenario(nome_cenario),
            check=True, timeout=duracao_total(nome_cenario) + 15.0)

        subprocess.run([
            'ros2', 'service', 'call', '/gravador_atores_node/salvar',
            'std_srvs/srv/Trigger', '{}',
        ], check=True, capture_output=True)
    finally:
        # SEMPRE limpa os processos deste teste, mesmo se o cenario ou o
        # salvar falharem no meio - um teste ruim nao pode vazar processo
        # pro PROXIMO teste da bancada.
        _encerrar_processo(gravador, 'gravador_atores_node')
        _encerrar_processo(processo_mover, 'mover_pessoas_node')
        time.sleep(1.0)

    caminho_hipoteses = os.path.join(diretorio_saida, 'hipoteses.csv')
    caminho_verdade = os.path.join(diretorio_saida, 'verdade.csv')
    caminho_robo = os.path.join(diretorio_saida, 'robo.csv')
    if not os.path.exists(caminho_hipoteses) or not os.path.exists(caminho_verdade):
        raise RuntimeError(
            f'gravador_atores_node nao salvou os CSVs esperados em {diretorio_saida} '
            f'(n_pessoas={n_pessoas}, robo="{nome_robo}")')

    # checagens 1 e 2 do item 2 (ver docstring do modulo) - rodam DEPOIS do
    # teste, em cima do que foi de fato gravado, pra pegar qualquer bug de
    # infraestrutura antes de confiar na metrica calculada abaixo.
    verdade = carregar_csv(caminho_verdade)
    robo = carregar_robo_csv(caminho_robo) if os.path.exists(caminho_robo) else []
    duracao_teste = duracao_total(nome_cenario)
    _, motivos_atores = checar_atores_andaram(verdade, atores_deste_teste, duracao_teste)
    _, motivos_robo = checar_robo_comecou_no_spawn(robo, POSE_SPAWN)
    motivos_invalidos = motivos_atores + motivos_robo
    if motivos_invalidos:
        raise RuntimeError(f'combinacao invalida: {"; ".join(motivos_invalidos)}')

    return calcular_metricas_de_arquivos(caminho_hipoteses, caminho_verdade)


def main():
    parser = argparse.ArgumentParser(
        description='Roda a bancada multi-pessoa (4.9): n_pessoas x robo parado/andando.')
    parser.add_argument('--diretorio-base', default='/tmp/saye_tracking_suite_pessoas')
    parser.add_argument('--n-pessoas', nargs='*', type=int, default=QUANTIDADES_PESSOAS)
    parser.add_argument('--robos', nargs='*', default=sorted(ROBO_CENARIOS.keys()))
    args = parser.parse_args()

    atores = _carregar_atores()
    if len(atores) < max(args.n_pessoas):
        raise SystemExit(
            f'config/atores.yaml so tem {len(atores)} atores, '
            f'nao da pra testar com {max(args.n_pessoas)} pessoas')

    resultados = []
    for n_pessoas in args.n_pessoas:
        for nome_robo in args.robos:
            print(f'--- rodando n_pessoas={n_pessoas} robo="{nome_robo}" ---', flush=True)
            diretorio_saida = os.path.join(
                args.diretorio_base, f'{n_pessoas}_pessoas_robo_{nome_robo}')
            try:
                resumo = _rodar_uma_combinacao(
                    n_pessoas, nome_robo, atores, diretorio_saida)
            except Exception as exc:  # noqa: BLE001 - 1 falha nao pode derrubar a bancada
                print(f'  FALHOU: {exc}')
                continue
            resultados.append((n_pessoas, nome_robo, resumo.iloc[0]))

    if not resultados:
        raise SystemExit('nenhuma combinacao terminou com sucesso - ver os avisos acima')

    print()
    print(_formatar_relatorio(resultados))
    _salvar_relatorio_csv(resultados, os.path.join(args.diretorio_base, 'relatorio.csv'))


def _formatar_relatorio(resultados):
    linhas = ['| ' + ' | '.join(COLUNAS_RELATORIO) + ' |',
              '|' + '---|' * len(COLUNAS_RELATORIO)]
    for n_pessoas, nome_robo, resumo in resultados:
        valores = [str(n_pessoas), nome_robo] + [
            _formatar_valor(resumo[c]) for c in COLUNAS_RELATORIO[2:]]
        linhas.append('| ' + ' | '.join(valores) + ' |')
    return '\n'.join(linhas)


def _formatar_valor(valor):
    if isinstance(valor, float):
        return f'{valor:.3f}'
    return str(valor)


def _salvar_relatorio_csv(resultados, caminho):
    import csv
    with open(caminho, 'w', newline='') as f:
        escritor = csv.writer(f)
        escritor.writerow(COLUNAS_RELATORIO)
        for n_pessoas, nome_robo, resumo in resultados:
            escritor.writerow(
                [n_pessoas, nome_robo] + [resumo[c] for c in COLUNAS_RELATORIO[2:]])
    print(f'relatorio CSV salvo em {caminho}')


if __name__ == '__main__':
    main()
