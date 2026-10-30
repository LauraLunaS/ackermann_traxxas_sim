"""
Gravador (submodulo 4.1 da Fase 4 - bancada de avaliacao).

Grava, ao longo do tempo, duas series paralelas:
  - hipoteses: o que o `tracker_node` disse que existia (id do track, x, y,
    tempo) - e o que o rastreador ACHA que esta vendo.
  - verdade: onde os objetos de verdade estavam no Gazebo (nome do objeto,
    x, y, tempo) - o "gabarito".

Puro Python + csv, sem ROS - so acumula linhas em memoria e escreve em disco.
Sincronizar as duas series por instante (agrupar em "frames" pro motmetrics)
e calcular metricas (MOTA, trocas de ID, etc.) fica pro submodulo 4.2; aqui
e so a gravacao bruta, pra poder testar sem precisar da simulacao rodando.
"""
import csv

CABECALHO = ['tempo', 'id', 'x', 'y']


CABECALHO_ROBO = ['tempo', 'x', 'y', 'yaw']


class Gravador:
    """Acumula linhas de hipotese/verdade e salva como CSV."""

    def __init__(self):
        self.hipoteses = []  # lista de (tempo, id, x, y)
        self.verdade = []    # lista de (tempo, id, x, y)
        self.robo = []       # lista de (tempo, x, y, yaw) - pose real do robo (4.9)

    def registrar_hipotese(self, tempo, id_track, x, y):
        self.hipoteses.append((float(tempo), str(id_track), float(x), float(y)))

    def registrar_verdade(self, tempo, id_objeto, x, y):
        self.verdade.append((float(tempo), str(id_objeto), float(x), float(y)))

    def registrar_robo(self, tempo, x, y, yaw):
        self.robo.append((float(tempo), float(x), float(y), float(yaw)))

    def salvar(self, caminho_hipoteses, caminho_verdade, caminho_robo=None):
        _salvar_csv(caminho_hipoteses, self.hipoteses)
        _salvar_csv(caminho_verdade, self.verdade)
        if caminho_robo is not None:
            _salvar_csv(caminho_robo, self.robo, cabecalho=CABECALHO_ROBO)


def _salvar_csv(caminho, linhas, cabecalho=CABECALHO):
    with open(caminho, 'w', newline='') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(cabecalho)
        escritor.writerows(linhas)


def carregar_csv(caminho):
    """Le um CSV gravado por `Gravador.salvar` de volta como lista de tuplas."""
    linhas = []
    with open(caminho, newline='') as arquivo:
        leitor = csv.reader(arquivo)
        next(leitor)  # cabecalho
        for tempo, id_, x, y in leitor:
            linhas.append((float(tempo), id_, float(x), float(y)))
    return linhas
