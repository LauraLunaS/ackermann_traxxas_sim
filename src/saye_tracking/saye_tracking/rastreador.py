"""
O laco do rastreador OC-SORT 3D (Fase 3, submodulo 3.6).

Junta os submodulos 3.1-3.5 no ciclo completo, chamado uma vez por
mensagem de deteccoes 3D:

  1. PREDICT   - todo track (qualquer estado) avanca ate `tempo_atual`
  2. ASSOCIATE - 1o turno: tracks TENTATIVO/CONFIRMADO (que ainda confiam
                 na previsao do Kalman) casam com as deteccoes por
                 distancia + OCM (3.3+3.4)
  3. RECOVER   - 2o turno (OCR+ORU, 3.5, com gate adaptativo + OCM desde a
                 4.8): tracks PERDIDOS (de antes desta rodada OU que
                 acabaram de ficar perdidos no turno 1) tentam casar com as
                 deteccoes que sobraram, pela ULTIMA OBSERVACAO REAL, com
                 gate escalado pelo tempo perdido (nao o `gate_distancia`
                 cheio) e custo de direcao; quem casa e re-atualizado pela
                 trajetoria virtual
  4. UPDATE/MANAGE - deteccoes que sobraram de tudo viram tracks novos
                 (TENTATIVO), MENOS as que estao muito perto demais de um
                 track que acabou de ser atualizado nesta mesma rodada
                 (supressao de duplicata, 4.7 - ver docstring mais abaixo);
                 tracks que passaram da tolerancia (3.2) sao apagados
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

    def __init__(self, gate_distancia=0.4, peso_ocm=1.0, n_passos_oru=5,
                 raio_supressao_duplicata=0.5, velocidade_maxima_esperada=0.25,
                 margem_gate_recuperacao=0.1, **kwargs_track):
        self.tracks = []
        # 4.8: o `gate_distancia` original (1.5m) era maior que a MENOR
        # distancia real entre 2 pessoas distintas na cena de validacao
        # (atores.yaml): pessoa_2-pessoa_3 ficam so 0.5m uma da outra em
        # certos pontos, pessoa_1-pessoa_2 chegam a 1.0m. Isso deixava o
        # turno 1 (associacao normal, nao so o OCR) casar DIRETO a previsao
        # de um track com a deteccao de OUTRA pessoa sempre que elas
        # estivessem a menos de 1.5m - confirmado ao vivo (gravacao de
        # 97.4s). Uma 1a reducao pra 0.5m (= exatamente a menor distancia
        # real) ainda deixava passar: a troca nao acontecia mais num salto
        # unico, mas em varios passos pequenos (cada um dentro do gate),
        # ainda trocando de pessoa de forma gradual perto do ponto de
        # menor distancia. Reduzido pra 0.4m - ESTRITAMENTE abaixo dos
        # 0.5m, suficiente mesmo que o Hungaro tente encadear passos
        # pequenos - e ainda bem acima do deslocamento esperado entre 2
        # deteccoes consecutivas (velocidade real <=0.3m/s a ~10-20Hz) +
        # ruido de projecao.
        self.gate_distancia = gate_distancia
        self.peso_ocm = peso_ocm
        self.n_passos_oru = n_passos_oru
        # ver docstring de `recuperacao.recuperar_perdidos` - o gate da
        # recuperacao (OCR) escala com o tempo perdido em vez de usar sempre
        # `gate_distancia` cheio, pra nao "recuperar" um track com a
        # deteccao de OUTRA pessoa que por acaso esta por perto.
        self.velocidade_maxima_esperada = velocidade_maxima_esperada
        self.margem_gate_recuperacao = margem_gate_recuperacao
        # 4.7: raio (m) abaixo do qual uma deteccao sem par NAO abre track
        # novo, se estiver perto demais de um track ja atualizado nesta
        # mesma rodada - ver `_filtrar_duplicatas` abaixo. Tem que ser bem
        # menor que `gate_distancia` (senao sufocaria gente de verdade perto
        # uma da outra); a largura de uma pessoa (~0.3-0.5m) e a referencia.
        self.raio_supressao_duplicata = raio_supressao_duplicata
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
                perdidos_para_ocr, deteccoes_sobrando, tempo_atual,
                gate_max_distancia=self.gate_distancia,
                velocidade_maxima_esperada=self.velocidade_maxima_esperada,
                margem_gate=self.margem_gate_recuperacao,
                peso_ocm=self.peso_ocm)
        else:
            matches2, sem_det2 = [], list(range(len(deteccoes_sobrando)))

        for it, idet_local in matches2:
            reatualizar_trajetoria_virtual(
                perdidos_para_ocr[it], deteccoes_sobrando[idet_local],
                tempo_atual, n_passos=self.n_passos_oru)

        # --- deteccoes que sobraram de tudo -> tracks novos --------------
        indices_sobrando_final = [sem_det1[j] for j in sem_det2]

        tracks_atualizados_agora = (
            [elegiveis[it] for it, _ in matches1]
            + [perdidos_para_ocr[it] for it, _ in matches2]
        )
        indices_sobrando_final = self._filtrar_duplicatas(
            indices_sobrando_final, deteccoes_xy, tracks_atualizados_agora)

        for idet in indices_sobrando_final:
            self.tracks.append(
                Track(tuple(deteccoes_xy[idet]), tempo_atual, **self._kwargs_track))

        # --- apaga quem passou da tolerancia ------------------------------
        self.tracks = [t for t in self.tracks if not t.deve_ser_apagado(tempo_atual)]

        return self.tracks_confirmados()

    def tracks_confirmados(self):
        return [t for t in self.tracks if t.estado == EstadoTrack.CONFIRMADO]

    # ------------------------------------------------------------------
    def _filtrar_duplicatas(self, indices_sobrando, deteccoes_xy, tracks_atualizados_agora):
        """
        Submodulo 4.7 - supressao de duplicata.

        Motivacao (analise da Fase 4.6 com 3 pessoas reais andando): quando
        duas pessoas passam perto uma da outra (ex.: cruzamento de
        caminhos), a deteccao/projecao 3D ocasionalmente gera uma SEGUNDA
        deteccao da MESMA pessoa (silhueta particionada, sobreposicao
        momentanea das duas, ou a troca de quadro do "flipbook" de
        caminhada) a poucos centimetros de onde a deteccao "boa" dela
        acabou de casar com o track existente. Como o laco normal so cria
        track novo pra deteccao SEM par, essa segunda deteccao sobra e
        nasce como um track TENTATIVO novo, bem em cima do track que ja
        existe - o id fantasma (ex.: ids 102/104/105 observados na analise,
        todos a <20cm de um track recem-atualizado no mesmo ciclo).

        Por isso: antes de deixar uma deteccao sem par abrir track novo,
        se ela estiver a `raio_supressao_duplicata` metros ou menos de
        algum track que JA foi atualizado (observado) nesta mesma rodada,
        ela e descartada (tratada como duplicata, nao como objeto novo).
        So considera tracks atualizados NESTA rodada (nao qualquer track
        parado/perdido antigo) - uma pessoa nova que apareca perto de um
        track velho e sem atualizacao recente deve, sim, poder abrir track
        proprio.
        """
        if not indices_sobrando or not tracks_atualizados_agora:
            return indices_sobrando

        posicoes_atualizadas = np.array([t.posicao for t in tracks_atualizados_agora])
        sobrando_filtrado = []
        for idet in indices_sobrando:
            distancias = np.linalg.norm(posicoes_atualizadas - deteccoes_xy[idet], axis=1)
            if np.min(distancias) > self.raio_supressao_duplicata:
                sobrando_filtrado.append(idet)
        return sobrando_filtrado
