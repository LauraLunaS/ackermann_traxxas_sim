"""
Cenarios de teste (submodulo 4.3 da Fase 4 - bancada de avaliacao).

Cada cenario e uma lista de segmentos `(vx, wz, duracao_segundos)` - um
"roteiro" de comando de velocidade pro robo (`vx` linear m/s, `wz` angular
rad/s). Sem ROS - so as definicoes e a logica de "qual comando esta ativo
em tal instante", testavel sem precisar do robo de verdade.

Como so a classe "person" e detectada hoje (`deteccao.yaml`) e so existe
UMA pessoa no mundo, e ela e ESTATICA (`pessoa_detectavel`, ver 4.0), os
cenarios de movimento/oclusao/entra-sai-do-FOV sao feitos MOVENDO O ROBO
(a camera), nao a pessoa - equivalente do ponto de vista de rastreamento
relativo (o que importa pro tracker e o movimento relativo camera-alvo).

O robo nasce em `(-1.0, 1.0)`, olhando pra +x (yaw=0); a pessoa esta em
`(2.0, 1.0)`, ou seja, 3m a frente, de frente pra camera.

- `parado`: baseline, robo parado, pessoa sempre no mesmo lugar na imagem.
- `linear`: avanca reto em direcao a pessoa (aproximacao + passagem perto).
- `curva`: avanca curvando (testa estabilidade do track com o robo girando).
- `entra_sai_fov`: gira pra um lado e pro outro, tirando e trazendo a
  pessoa de dentro do campo de visao da camera repetidas vezes.
- `oclusao_obstaculo`: robo fica parado olhando pra pessoa enquanto os
  obstaculos dinamicos do mundo (que patrulham sozinhos, ver achado do 3.8)
  passam entre camera e pessoa por conta propria - MELHOR ESFORCO, nao
  deterministico (a patrulha dos obstaculos nao e limpa, ver README).

Os dois a seguir sao do `rodar_suite_pessoas.py` (4.9 - bancada
multi-pessoa, atores andando de verdade em vez da `pessoa_detectavel`
estatica): duracao bem mais longa (30s, nao 8-15s) pra dar tempo dos
atores percorrerem boa parte do proprio caminho em loop.
- `parado_pessoas`: baseline da bancada 4.9, robo parado.
- `andando_pessoas`: avanca bem devagar (0.1 m/s) - rapido o bastante pra
  testar o robo em movimento, devagar o bastante pra nao sair da zona
  onde os atores circulam nem percorrer alem do mundo (ver
  `config/atores.yaml`) nos 30s de duracao.
"""

CENARIOS = {
    'parado': [
        (0.0, 0.0, 10.0),
    ],
    'linear': [
        (0.4, 0.0, 8.0),
    ],
    'curva': [
        (0.3, 0.0, 2.0),
        (0.3, 0.4, 4.0),
        (0.3, 0.0, 2.0),
    ],
    'entra_sai_fov': [
        (0.0, 0.5, 2.0),
        (0.0, -0.5, 4.0),
        (0.0, 0.5, 2.0),
    ],
    'oclusao_obstaculo': [
        (0.0, 0.0, 15.0),
    ],
    'parado_pessoas': [
        (0.0, 0.0, 30.0),
    ],
    'andando_pessoas': [
        (0.1, 0.0, 30.0),
    ],
}


def duracao_total(nome_cenario):
    """Soma as duracoes dos segmentos do cenario `nome_cenario`."""
    return sum(duracao for _, _, duracao in CENARIOS[nome_cenario])


def comando_no_instante(nome_cenario, tempo_decorrido):
    """Retorna (vx, wz) ativo em `tempo_decorrido` segundos, ou None se ja acabou."""
    acumulado = 0.0
    for vx, wz, duracao in CENARIOS[nome_cenario]:
        acumulado += duracao
        if tempo_decorrido < acumulado:
            return (vx, wz)
    return None
