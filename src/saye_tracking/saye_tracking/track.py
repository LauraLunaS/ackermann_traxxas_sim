"""
Ciclo de vida de um track (Fase 3, submodulo 3.2).

Um Track envolve um FiltroKalman (3.1) com uma maquina de estados baseada em
TEMPO (segundos), nao em contagem de frames - importante porque o FPS da
Fase 1/2 varia (YOLO em CPU, ~10Hz e irregular nesta maquina).

Estados:
  TENTATIVO  - acabou de nascer de uma deteccao sem par. Vira CONFIRMADO se
               for observado de novo `min_hits_confirmar` vezes; se demorar
               demais pra ser reobservado, e apagado (filtra deteccao de
               1 frame so, tipo ruido).
  CONFIRMADO - ja tem historico suficiente pra ser considerado real; tem
               um ID publico estavel.
  PERDIDO    - era CONFIRMADO mas o ciclo de associacao (3.3) nao casou ele
               com nenhuma deteccao nesta rodada. Continua "vivo" (elegivel
               pra recuperacao via OCR no 3.5); volta a CONFIRMADO na
               proxima observacao real, ou e apagado se ficar tempo demais
               sem ser visto.

Sem ROS - so a maquina de estados e o Kalman por baixo.
"""
from collections import deque
from enum import Enum
import itertools

import numpy as np

from saye_tracking.kalman import FiltroKalman

TAMANHO_HISTORICO_MOMENTUM = 5  # quantas observacoes reais guardar p/ o OCM (3.4)


class EstadoTrack(Enum):
    TENTATIVO = 'tentativo'
    CONFIRMADO = 'confirmado'
    PERDIDO = 'perdido'


class Track:
    """Um objeto rastreado: Kalman + maquina de estados por tempo."""

    _proximo_id = itertools.count(1)

    def __init__(self, posicao_inicial, tempo_criacao,
                 min_hits_confirmar=3,
                 tolerancia_tentativo_segundos=0.4,
                 tolerancia_perdido_segundos=1.5,
                 **kwargs_kalman):
        self.id = next(Track._proximo_id)
        self.kalman = FiltroKalman(posicao_inicial, **kwargs_kalman)
        self.estado = EstadoTrack.TENTATIVO
        self.hits = 1

        self.tempo_criacao = tempo_criacao
        self.tempo_ultima_observacao = tempo_criacao
        self._tempo_ultimo_predict = tempo_criacao

        self._min_hits_confirmar = min_hits_confirmar
        self._tolerancia_tentativo = tolerancia_tentativo_segundos
        self._tolerancia_perdido = tolerancia_perdido_segundos

        # 3.4 (OCM): historico de observacoes REAIS (nao do Kalman) - o
        # OC-SORT usa observacoes, nao o estado do filtro, pra estimar a
        # direcao do movimento (mais estavel que a velocidade do Kalman
        # logo apos uma oclusao)
        self.historico = deque(
            [(tempo_criacao, np.array(posicao_inicial, dtype=np.float64))],
            maxlen=TAMANHO_HISTORICO_MOMENTUM)

    # ------------------------------------------------------------------
    @property
    def posicao(self):
        return self.kalman.posicao

    @property
    def velocidade(self):
        return self.kalman.velocidade

    # ------------------------------------------------------------------
    def prever(self, tempo_atual):
        """Avanca o Kalman ate `tempo_atual` (chamado toda rodada, sempre)."""
        dt = tempo_atual - self._tempo_ultimo_predict
        if dt > 0:
            self.kalman.predict(dt)
        self._tempo_ultimo_predict = tempo_atual

    def observar(self, posicao_xy, tempo_atual):
        """Corrige com uma deteccao real que casou com este track."""
        self.kalman.update(posicao_xy)
        self.hits += 1
        self.tempo_ultima_observacao = tempo_atual
        self.historico.append((tempo_atual, np.array(posicao_xy, dtype=np.float64)))

        if self.estado == EstadoTrack.TENTATIVO:
            if self.hits >= self._min_hits_confirmar:
                self.estado = EstadoTrack.CONFIRMADO
        elif self.estado == EstadoTrack.PERDIDO:
            self.estado = EstadoTrack.CONFIRMADO

    def marcar_nao_observado(self):
        """Chamado quando a associacao (3.3) NAO casou este track na rodada."""
        if self.estado == EstadoTrack.CONFIRMADO:
            self.estado = EstadoTrack.PERDIDO

    def deve_ser_apagado(self, tempo_atual) -> bool:
        """
        Diz se o track ja passou tempo demais sem ser observado.

        Track tentativo tem pouca paciencia (filtra deteccao ruido); track
        confirmado/perdido tem mais (sobrevive a oclusao curta).
        """
        tempo_sem_ver = tempo_atual - self.tempo_ultima_observacao
        limite = (self._tolerancia_tentativo if self.estado == EstadoTrack.TENTATIVO
                  else self._tolerancia_perdido)
        return tempo_sem_ver > limite

    # ------------------------------------------------------------------
    def direcao_momentum(self):
        """
        Estima a direcao do movimento a partir de observacoes reais.

        Usa OBSERVACOES reais (nao o Kalman) - da mais antiga a mais
        recente do historico.

        None se ainda nao ha pelo menos 2 observacoes reais, ou se o track
        nao se moveu o suficiente pra ter uma direcao definida (parado).
        """
        if len(self.historico) < 2:
            return None
        _, posicao_antiga = self.historico[0]
        _, posicao_recente = self.historico[-1]
        vetor = posicao_recente - posicao_antiga
        norma = np.linalg.norm(vetor)
        if norma < 1e-6:
            return None
        return vetor / norma
