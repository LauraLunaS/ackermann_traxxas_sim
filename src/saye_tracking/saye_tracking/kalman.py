"""
Filtro de Kalman de um track, em 3D-no-plano-do-chao (Fase 3, submodulo 3.1).

Estado: [x, y, vx, vy] - posicao e velocidade no frame `odom`, em metros e
m/s. Modelo de velocidade constante (o objeto anda em linha reta entre
instantes; o ruido de processo modela o quanto ele pode acelerar/curvar).

Puro numpy - sem rclpy, sem ROS. Isso e deliberado: a matematica do filtro
nao depende de nada do ROS, e pode ser testada e usada sozinha (pelo
`Track` do submodulo 3.2, depois pelo laco do rastreador no 3.6).
"""
import numpy as np


class FiltroKalman:
    """Kalman linear, estado [x, y, vx, vy], medicao = posicao (x, y)."""

    def __init__(self, posicao_inicial, ruido_processo=1.0, ruido_medicao=0.1,
                 incerteza_inicial_posicao=0.1, incerteza_inicial_velocidade=10.0):
        """
        Inicializa o filtro a partir da primeira deteccao de um track.

        posicao_inicial: (x, y) da primeira deteccao que criou o track.
        ruido_processo: intensidade do ruido de aceleracao (q). Maior =
            filtro confia menos no modelo de velocidade constante e reage
            mais rapido a mudancas de direcao; menor = mais suave, mais lento
            pra reagir.
        ruido_medicao: desvio padrao (metros) do erro de posicao da Fase 2
            (~0.05-0.1 m, pela validacao do submodulo 2.5).
        incerteza_inicial_velocidade: alta de proposito - na primeira
            deteccao nao sabemos a velocidade, entao comecamos "sem certeza
            nenhuma" e deixamos as proximas atualizacoes corrigirem rapido.
        """
        x0, y0 = posicao_inicial
        self.x = np.array([x0, y0, 0.0, 0.0], dtype=np.float64)
        self.P = np.diag([
            incerteza_inicial_posicao ** 2, incerteza_inicial_posicao ** 2,
            incerteza_inicial_velocidade ** 2, incerteza_inicial_velocidade ** 2,
        ])
        self.q = ruido_processo
        self.R = np.eye(2) * ruido_medicao ** 2
        self.H = np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
        ])

    # ------------------------------------------------------------------
    @property
    def posicao(self) -> np.ndarray:
        return self.x[:2].copy()

    @property
    def velocidade(self) -> np.ndarray:
        return self.x[2:].copy()

    # ------------------------------------------------------------------
    def predict(self, dt: float):
        """Avanca o estado por `dt` segundos, sem nenhuma medicao nova."""
        F = np.array([
            [1.0, 0.0, dt, 0.0],
            [0.0, 1.0, 0.0, dt],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ])
        # ruido de processo: modelo de aceleracao branca discretizado,
        # eixos x e y independentes
        dt2, dt3, dt4 = dt ** 2, dt ** 3, dt ** 4
        q = self.q
        Q = q * np.array([
            [dt4 / 4, 0, dt3 / 2, 0],
            [0, dt4 / 4, 0, dt3 / 2],
            [dt3 / 2, 0, dt2, 0],
            [0, dt3 / 2, 0, dt2],
        ])

        self.x = F @ self.x
        self.P = F @ self.P @ F.T + Q

    def update(self, medicao_xy):
        """Corrige o estado com uma medicao de posicao (x, y) real."""
        z = np.asarray(medicao_xy, dtype=np.float64)
        y = z - self.H @ self.x                       # inovacao (residuo)
        S = self.H @ self.P @ self.H.T + self.R        # covariancia da inovacao
        K = self.P @ self.H.T @ np.linalg.inv(S)        # ganho de Kalman

        self.x = self.x + K @ y
        identidade = np.eye(4)
        self.P = (identidade - K @ self.H) @ self.P
