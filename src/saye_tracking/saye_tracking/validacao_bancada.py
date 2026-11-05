"""
Checagens automaticas de validade de uma combinacao da bancada.

Item 2 do roteiro pos-correcao de movimentacao.

Motivacao: o achado 4 (`gz_pose_vector.py` - teleporte de ator falhando em
silencio sob concorrencia) passou por VARIAS rodadas da bancada sem ser
percebido, porque nada nela verificava se o que deveria ter acontecido
realmente aconteceu - so o MOTA final era olhado, e um numero "razoavel"
nao distingue um teste limpo de um teste contaminado por um bug de
infraestrutura. Cada checagem aqui ataca um dos achados ja documentados
(README, 4.9):

  - `checar_atores_andaram`: achado 1/4 (ator fantasma parado OU teleporte
    falhando) - cada ator devia ter percorrido perto da distancia
    esperada (`velocidade * duracao`), nao ficar parado.
  - `checar_robo_comecou_no_spawn`: achado 3 (`/cmd_vel` residual) - o robo
    tem que comecar a gravacao perto do spawn e praticamente parado, nao
    "aparecer" ja deslizando por um comando antigo.

A 3a checagem do roteiro ("o reset do tracker realmente zerou as
tracks?") fica em `rodar_suite_pessoas.py` (depende do texto da resposta
do servico ROS, nao e logica pura) - ver `_chamar_resetar_tracker`.

Sem ROS - recebe os dados JA CARREGADOS (listas de tuplas), testavel com
cenarios fabricados.
"""


def distancia_percorrida(pontos):
    """Soma das distancias entre pontos (x, y) CONSECUTIVOS, na ordem dada."""
    total = 0.0
    for (x0, y0), (x1, y1) in zip(pontos, pontos[1:]):
        total += ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    return total


def checar_atores_andaram(linhas_verdade, atores, duracao_teste, fracao_minima=0.3):
    """
    Confere que cada ator andou pelo menos uma fracao da distancia esperada.

    Distancia esperada = `velocidade * duracao_teste`. `linhas_verdade`:
    lista de (tempo, nome, x, y), como `gravador.carregar_csv` devolve pro
    `verdade.csv`. Devolve (valido, motivos) - `motivos` e uma lista de
    strings, vazia se `valido`.
    """
    motivos = []
    for ator in atores:
        nome = ator['nome']
        pontos = [(x, y) for _tempo, nome_linha, x, y in linhas_verdade if nome_linha == nome]
        if not pontos:
            motivos.append(f'"{nome}" nao aparece nenhuma vez na verdade gravada')
            continue
        esperado = ator['velocidade'] * duracao_teste
        andado = distancia_percorrida(pontos)
        if andado < esperado * fracao_minima:
            motivos.append(
                f'"{nome}" andou {andado:.2f}m, esperado pelo menos '
                f'{esperado * fracao_minima:.2f}m ({fracao_minima:.0%} de {esperado:.2f}m)')
    return (not motivos, motivos)


def checar_robo_comecou_no_spawn(
        linhas_robo, pose_spawn, tolerancia_m=0.3, janela_segundos=1.0, velocidade_maxima=0.05):
    """
    Confere que o robo comecou a gravacao perto do spawn e praticamente parado.

    `linhas_robo`: lista de (tempo, x, y, yaw), como `gravador.
    carregar_robo_csv` devolve. `pose_spawn`: (x, y, z) - so x/y importam
    aqui. Devolve (valido, motivos).
    """
    if not linhas_robo:
        return (False, ['nenhuma pose do robo foi gravada'])

    x_spawn, y_spawn = pose_spawn[0], pose_spawn[1]
    tempo_inicio = linhas_robo[0][0]
    janela = [
        (tempo, x, y) for tempo, x, y, _yaw in linhas_robo
        if tempo - tempo_inicio <= janela_segundos
    ]

    motivos = []
    primeiro_x, primeiro_y = janela[0][1], janela[0][2]
    distancia_do_spawn = ((primeiro_x - x_spawn) ** 2 + (primeiro_y - y_spawn) ** 2) ** 0.5
    if distancia_do_spawn > tolerancia_m:
        motivos.append(
            f'robo comecou a {distancia_do_spawn:.2f}m do spawn '
            f'({x_spawn}, {y_spawn}), tolerancia {tolerancia_m}m')

    if len(janela) >= 2:
        andado = distancia_percorrida([(x, y) for _tempo, x, y in janela])
        duracao_janela = janela[-1][0] - janela[0][0]
        if duracao_janela > 0:
            velocidade_media = andado / duracao_janela
            if velocidade_media > velocidade_maxima:
                motivos.append(
                    f'robo ja andava a {velocidade_media:.3f}m/s no 1o '
                    f'{janela_segundos}s (esperado parado, <={velocidade_maxima}m/s) '
                    f'- possivel /cmd_vel residual')

    return (not motivos, motivos)
