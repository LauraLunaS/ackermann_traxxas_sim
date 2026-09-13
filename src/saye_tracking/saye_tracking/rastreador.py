"""
O laco do rastreador OC-SORT 3D (Fase 3, submodulo 3.6).

Junta os submodulos 3.1-3.5 no ciclo completo, chamado uma vez por
mensagem de deteccoes 3D:

  1. PREDICT   - todo track (qualquer estado) avanca ate `tempo_atual`
  2. ASSOCIATE - 1o turno: tracks TENTATIVO/CONFIRMADO (que ainda confiam
                 na previsao do Kalman) casam com as deteccoes por
                 distancia + OCM (3.3+3.4)
  3. RECOVER   - 2o turno (OCR+ORU, 3.5): tracks PERDIDOS (de antes desta
                 rodada OU que acabaram de ficar perdidos no turno 1) tentam
                 casar com as deteccoes que sobraram, pela ULTIMA OBSERVACAO
                 REAL; quem casa e re-atualizado pela trajetoria virtual
  4. UPDATE/MANAGE - deteccoes que sobraram de tudo viram tracks novos
                 (TENTATIVO); tracks que passaram da tolerancia (3.2) sao
                 apagados
  5. PUBLISH   - devolve os tracks CONFIRMADOS (os outros nao sao "reais"
                 o bastante pra reportar pra fora ainda)

Sem ROS.
"""
import numpy as np

from saye_tracking.associacao import associar
from saye_tracking.ocm import custo_direcao
from saye_tracking.recuperacao import reatualizar_trajetoria_virtual, recuperar_perdidos
from saye_tracking.track import EstadoTrack, Track


class Rastreador3D:
    """Mantem uma populacao de Tracks e os atualiza a cada rodada de deteccoes."""

    def __init__(self, gate_distancia=1.5, peso_ocm=1.0, n_passos_oru=5,
                 **kwargs_track):
        self.tracks = []
        self.gate_distancia = gate_distancia
        self.peso_ocm = peso_ocm
        self.n_passos_oru = n_passos_oru
        self._kwargs_track = kwargs_track  # min_hits_confirmar, tolerancias, etc

    # ------------------------------------------------------------------
    def processar(self, deteccoes_xy, tempo_atual):
        """Roda 1 ciclo completo; retorna a lista de tracks CONFIRMADOS."""
        deteccoes_xy = np.asarray(deteccoes_xy, dtype=np.float64).reshape(-1, 2)

        for t in self.tracks:
            t.prever(tempo_atual)

        elegiveis = [t for t in self.tracks if t.estado != EstadoTrack.PERDIDO]
        ja_perdidos = [t for t in self.tracks if t.estado == EstadoTrack.PERDIDO]

        # --- turno 1: associacao normal (previsao + OCM) -----------------
        if elegiveis:
            predicoes = np.array([t.posicao for t in elegiveis])
            momentum = [t.direcao_momentum() for t in elegiveis]
            penal = custo_direcao(predicoes, deteccoes_xy, momentum, peso=self.peso_ocm)
            matches1, sem_track1, sem_det1 = associar(
                predicoes, deteccoes_xy, self.gate_distancia, custo_extra=penal)
        else:
            matches1, sem_track1, sem_det1 = [], [], list(range(len(deteccoes_xy)))

        for it, idet in matches1:
            elegiveis[it].observar(deteccoes_xy[idet], tempo_atual)
        for it in sem_track1:
            elegiveis[it].marcar_nao_observado()

        # --- turno 2: OCR + ORU (tracks perdidos, de antes ou de agora) --
        perdidos_para_ocr = ja_perdidos + [
            elegiveis[i] for i in sem_track1
            if elegiveis[i].estado == EstadoTrack.PERDIDO
        ]
        deteccoes_sobrando = deteccoes_xy[sem_det1]

        if perdidos_para_ocr and len(deteccoes_sobrando):
            matches2, _, sem_det2 = recuperar_perdidos(
                perdidos_para_ocr, deteccoes_sobrando, self.gate_distancia)
        else:
            matches2, sem_det2 = [], list(range(len(deteccoes_sobrando)))

        for it, idet_local in matches2:
            reatualizar_trajetoria_virtual(
                perdidos_para_ocr[it], deteccoes_sobrando[idet_local],
                tempo_atual, n_passos=self.n_passos_oru)

        # --- deteccoes que sobraram de tudo -> tracks novos --------------
        indices_sobrando_final = [sem_det1[j] for j in sem_det2]
        for idet in indices_sobrando_final:
            self.tracks.append(
                Track(tuple(deteccoes_xy[idet]), tempo_atual, **self._kwargs_track))

        # --- apaga quem passou da tolerancia ------------------------------
        self.tracks = [t for t in self.tracks if not t.deve_ser_apagado(tempo_atual)]

        return self.tracks_confirmados()

    def tracks_confirmados(self):
        return [t for t in self.tracks if t.estado == EstadoTrack.CONFIRMADO]
