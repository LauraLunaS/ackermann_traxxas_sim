"""
Adaptador do KITTI Tracking Benchmark para o `Rastreador3D` (saye_tracking).

Objetivo: testar a logica de associacao/OCM/OCR (fases 3.3-3.5, 4.7-4.9) do
rastreador contra trajetorias de pedestres REAIS, em vez dos cenarios
sinteticos de `atores.yaml` - decoupled da deteccao/Gazebo. Alimenta o
`Rastreador3D` direto com as posicoes do gabarito do KITTI, do mesmo jeito
que a validacao 3.8 ja fez com os obstaculos do Gazebo (sem passar por ROS
nem por nenhum topico - licao da fase 4.3, onde um script solto publicando
por engano num topico real contaminou uma bancada inteira).

Escopo desta 1a etapa (trechos de camera PARADA): sem nenhuma conversao de
referencial. Sem a camera se mover, o frame da camera do KITTI e tao
estavel quanto o `odom` deste projeto - exatamente o caso "robo parado" da
bancada, que e a prioridade por decisao do usuario. Trechos com o carro
andando (que exigiriam compensar o movimento via `oxts`) ficam pra uma 2a
etapa, so depois de validar a conversao com carros ESTACIONADOS (mais
amostras que pedestres parados - mesmo teste da fase 2.3, so que no KITTI).

Formato do `label_02/<seq>.txt` (devkit oficial do KITTI tracking, 1 linha
por objeto por frame, campos separados por espaco):
    frame id tipo truncado ocluido alpha bb_esq bb_topo bb_dir bb_baixo
    altura largura comprimento loc_x loc_y loc_z rotacao_y

Usados aqui: frame, id, tipo, truncado, ocluido, loc_x (lateral) e loc_z
(profundidade - "pra frente" da camera), ambos em metros no frame da
camera. `ocluido`: -1 desconhecido, 0 totalmente visivel, 1 parcialmente
oculto, 2 em grande parte oculto. `truncado`: fracao do objeto fora da
imagem (0 = nada, 1 = tudo).

Formato do `oxts/<seq>.txt` (1 linha por frame): lat lon alt roll pitch yaw
vn ve vf vl vu ax ay az af al au wx wy wz wf wl wu pos_accuracy vel_accuracy
navstat numsats posmode velmode orimode - usamos so vf (campo 8, velocidade
pra frente) e vl (campo 9, velocidade lateral), em m/s, pra decidir se o
carro esta parado.
"""

CAMPOS_MINIMOS_LABEL = 17
OCLUIDO_LARGAMENTE = 2       # >= isso: tratado como oclusao real (nao detectavel)
TRUNCADO_LIMIAR_PADRAO = 0.3  # >= isso: tratado como "saiu do campo de visao"


def ler_label_02(caminho):
    """
    Le um `label_02/<seq>.txt` e agrupa as linhas por frame.

    Retorna {frame: [linha, ...]}, cada linha um dict com `id` (int),
    `tipo` (str), `truncado` (float), `ocluido` (int), `x` e `z` (metros,
    frame da camera).
    """
    por_frame = {}
    with open(caminho) as arquivo:
        for linha in arquivo:
            campos = linha.split()
            if len(campos) < CAMPOS_MINIMOS_LABEL:
                continue  # linha incompleta - pula, nao derruba o resto
            frame = int(campos[0])
            por_frame.setdefault(frame, []).append({
                'id': int(campos[1]),
                'tipo': campos[2],
                'truncado': float(campos[3]),
                'ocluido': int(campos[4]),
                'x': float(campos[13]),
                'z': float(campos[15]),
            })
    return por_frame


def ler_velocidade_oxts(caminho):
    """
    Le um `oxts/<seq>.txt` e devolve a velocidade do carro por frame.

    Velocidade no plano do chao (m/s), um valor por frame (indice da
    lista = numero do frame).
    """
    velocidades = []
    with open(caminho) as arquivo:
        for linha in arquivo:
            campos = linha.split()
            vf, vl = float(campos[8]), float(campos[9])
            velocidades.append((vf ** 2 + vl ** 2) ** 0.5)
    return velocidades


def segmentos_carro_parado(velocidades, limiar_velocidade=0.5, duracao_minima_frames=50):
    """
    Retorna os trechos continuos com o carro essencialmente parado.

    Cada trecho e `(frame_inicio, frame_fim)` - onde nao e preciso
    compensar ego-motion.
    """
    segmentos = []
    inicio = None
    for frame, v in enumerate(velocidades):
        parado = v < limiar_velocidade
        if parado and inicio is None:
            inicio = frame
        elif not parado and inicio is not None:
            if frame - inicio >= duracao_minima_frames:
                segmentos.append((inicio, frame - 1))
            inicio = None
    if inicio is not None and len(velocidades) - inicio >= duracao_minima_frames:
        segmentos.append((inicio, len(velocidades) - 1))
    return segmentos


def filtrar_pedestres(por_frame, tipos_aceitos=('Pedestrian',)):
    """Mantem so as linhas dos tipos aceitos (descarta Car/DontCare/etc)."""
    return {
        frame: [linha for linha in linhas if linha['tipo'] in tipos_aceitos]
        for frame, linhas in por_frame.items()
    }


def gerar_deteccoes_e_motivos(
        por_frame_pedestres, ocluido_max=OCLUIDO_LARGAMENTE - 1,
        truncado_limiar=TRUNCADO_LIMIAR_PADRAO):
    """
    Decide, por frame, quem aparece como deteccao e quem some.

    Usa os campos REAIS de oclusao/truncamento do KITTI, nao sorteio
    aleatorio (dropout aleatorio testaria o modelo de ruido, nao oclusao
    real).

    Retorna (deteccoes_por_frame, motivo_ausencia):
      - deteccoes_por_frame: {frame: [(id, x, z), ...]} so quem "aparece".
      - motivo_ausencia: {(frame, id): 'oclusao' | 'fov'} pra quem existe no
        gabarito naquele frame mas nao aparece - usado pra separar os dois
        tipos de buraco no relatorio (oclusao e o que o item 5 investigou;
        saida de campo de visao e o que domina o cenario "andando" e NAO e
        o que a correcao do gate visa).
    """
    deteccoes_por_frame = {}
    motivo_ausencia = {}
    for frame, linhas in por_frame_pedestres.items():
        visiveis = []
        for linha in linhas:
            if linha['truncado'] >= truncado_limiar:
                motivo_ausencia[(frame, linha['id'])] = 'fov'
            elif linha['ocluido'] > ocluido_max:
                motivo_ausencia[(frame, linha['id'])] = 'oclusao'
            else:
                visiveis.append((linha['id'], linha['x'], linha['z']))
        deteccoes_por_frame[frame] = visiveis
    return deteccoes_por_frame, motivo_ausencia


def reescalar_deteccoes(deteccoes_por_frame, fator):
    """
    Encolhe a trajetoria de cada id por `fator`, a partir da 1a posicao.

    `fator` entre 0 e 1, preserva a forma do caminho e reduz a velocidade
    aparente na mesma proporcao (pedestres do KITTI andam ~4-5x mais
    rapido que a calibracao do rastreador - isso traz a velocidade pra
    faixa calibrada sem mudar os gates).
    """
    origem_por_id = {}
    for frame in sorted(deteccoes_por_frame):
        for id_, x, z in deteccoes_por_frame[frame]:
            origem_por_id.setdefault(id_, (x, z))

    escalado = {}
    for frame, deteccoes in deteccoes_por_frame.items():
        linha_escalada = []
        for id_, x, z in deteccoes:
            ox, oz = origem_por_id[id_]
            linha_escalada.append((id_, ox + (x - ox) * fator, oz + (z - oz) * fator))
        escalado[frame] = linha_escalada
    return escalado


def rodar_rastreador(deteccoes_por_frame, rastreador, fps=10.0):
    """
    Alimenta `rastreador` com as deteccoes sinteticas, frame a frame.

    Devolve a hipotese no mesmo formato do `gravador.py` ((tempo, id, x,
    y), 1 linha por track confirmado por frame) - pronta pra
    `comparador.py` calcular MOTA/IDF1 sem nenhum codigo novo de metrica.
    """
    hipoteses = []
    for frame in sorted(deteccoes_por_frame):
        tempo = frame / fps
        pontos = [(x, z) for _, x, z in deteccoes_por_frame[frame]]
        tracks = rastreador.processar(pontos, tempo)
        for t in tracks:
            hipoteses.append((tempo, str(t.id), float(t.posicao[0]), float(t.posicao[1])))
    return hipoteses


def verdade_para_csv(por_frame_pedestres, fps=10.0):
    """
    Traducao do gabarito completo pro formato (tempo, id, x, y).

    Sem os buracos de oclusao/fov - e o que `comparador.py` espera como
    verdade.
    """
    verdade = []
    for frame, linhas in por_frame_pedestres.items():
        tempo = frame / fps
        for linha in linhas:
            verdade.append((tempo, str(linha['id']), linha['x'], linha['z']))
    return verdade
