"""Submodulo 3.5 - teste do OCR (recuperacao) + ORU (re-update), sem ROS."""
import numpy as np
from saye_tracking.recuperacao import reatualizar_trajetoria_virtual, recuperar_perdidos
from saye_tracking.track import EstadoTrack, Track


def _track_perdido(posicao_inicial=(0.0, 0.0), tempo_criacao=0.0):
    t = Track(posicao_inicial=posicao_inicial, tempo_criacao=tempo_criacao,
              min_hits_confirmar=2)
    t.observar(posicao_inicial, tempo_atual=tempo_criacao + 0.1)  # confirma
    t.marcar_nao_observado()
    assert t.estado == EstadoTrack.PERDIDO
    return t


# --- OCR: recuperar_perdidos ------------------------------------------
def test_recupera_perdido_perto_da_ultima_observacao_real():
    t = _track_perdido(posicao_inicial=(5.0, 0.0))

    matches, sem_track, sem_det = recuperar_perdidos([t], [(5.2, 0.0)])

    assert matches == [(0, 0)]
    assert sem_track == []
    assert sem_det == []


def test_gate_rejeita_recuperacao_muito_longe():
    t = _track_perdido(posicao_inicial=(5.0, 0.0))

    matches, sem_track, sem_det = recuperar_perdidos(
        [t], [(50.0, 0.0)], gate_max_distancia=1.5)

    assert matches == []
    assert sem_track == [0]
    assert sem_det == [0]


def test_usa_ultima_observacao_e_nao_a_previsao_do_kalman_desviada():
    t = _track_perdido(posicao_inicial=(0.0, 0.0))
    # forca uma velocidade "errada" no Kalman e avanca bastante o tempo -
    # a PREVISAO do filtro fica longe, mas a ULTIMA OBSERVACAO REAL continua
    # em (0,0), perto da deteccao candidata
    t.kalman.x[2:] = [0.0, 10.0]
    t.prever(tempo_atual=5.0)
    assert np.linalg.norm(t.posicao) > 40  # previsao bem longe, como esperado

    matches, sem_track, sem_det = recuperar_perdidos(
        [t], [(0.3, 0.0)], gate_max_distancia=1.5)

    assert matches == [(0, 0)]  # recuperou apesar da previsao ruim


# --- ORU: reatualizar_trajetoria_virtual --------------------------------
def test_estado_final_alcanca_a_posicao_nova():
    t = _track_perdido(posicao_inicial=(0.0, 0.0))

    reatualizar_trajetoria_virtual(t, posicao_nova=np.array([2.0, 1.0]),
                                   tempo_novo=2.1, n_passos=5)

    # apos 5 passos de correcao, converge bem perto (nao exatamente igual -
    # e uma fusao de Kalman, nao uma atribuicao direta)
    np.testing.assert_allclose(t.posicao, [2.0, 1.0], atol=0.01)


def test_track_perdido_vira_confirmado_apos_reatualizar():
    t = _track_perdido(posicao_inicial=(0.0, 0.0))

    reatualizar_trajetoria_virtual(t, posicao_nova=np.array([1.0, 0.0]),
                                   tempo_novo=1.0)

    assert t.estado == EstadoTrack.CONFIRMADO


def test_dt_nao_positivo_cai_para_observacao_direta():
    t = _track_perdido(posicao_inicial=(0.0, 0.0), tempo_criacao=5.0)
    n_observacoes_antes = len(t.historico)

    # tempo_novo igual ao da ultima observacao - nao da pra tracar reta,
    # tem que cair pra uma unica observacao direta (nao n_passos)
    reatualizar_trajetoria_virtual(t, posicao_nova=np.array([0.5, 0.0]),
                                   tempo_novo=5.1, n_passos=5)

    assert t.estado == EstadoTrack.CONFIRMADO
    assert len(t.historico) == n_observacoes_antes + 1


def test_velocidade_reflete_deslocamento_real_melhor_que_atualizacao_ingenua():
    """
    O caso que justifica o ORU.

    O Kalman tinha uma velocidade ERRADA
    guardada quando ficou perdido (ex.: ruido antes de sumir). O objeto
    reaparece 2s depois num lugar que implica uma velocidade real bem
    diferente da que o filtro tinha. Uma unica atualizacao ingenua (prever
    tudo de uma vez + 1 correcao) so corrige parcialmente a velocidade,
    porque o ganho de Kalman nao "confia" 100% numa unica medicao distante.
    O ORU, corrigindo em passos ao longo da reta real, se aproxima bem mais
    da velocidade verdadeira.
    """
    tempo_ultima_obs = 0.1
    posicao_antiga = np.array([0.0, 0.0])
    posicao_nova = np.array([2.0, 0.0])
    tempo_novo = 2.1
    velocidade_real = (posicao_nova - posicao_antiga) / (tempo_novo - tempo_ultima_obs)

    def _prepara_track_com_velocidade_errada():
        t = Track(posicao_inicial=tuple(posicao_antiga), tempo_criacao=0.0,
                  min_hits_confirmar=2)
        t.observar(tuple(posicao_antiga), tempo_atual=tempo_ultima_obs)
        t.kalman.x[2:] = [0.0, 3.0]  # velocidade errada guardada antes de sumir
        t.marcar_nao_observado()
        return t

    t_ingenuo = _prepara_track_com_velocidade_errada()
    t_ingenuo.prever(tempo_novo)
    t_ingenuo.observar(posicao_nova, tempo_novo)

    t_oru = _prepara_track_com_velocidade_errada()
    reatualizar_trajetoria_virtual(t_oru, posicao_nova, tempo_novo, n_passos=5)

    erro_ingenuo = np.linalg.norm(t_ingenuo.velocidade - velocidade_real)
    erro_oru = np.linalg.norm(t_oru.velocidade - velocidade_real)

    assert erro_oru < erro_ingenuo
    assert erro_oru < 0.02
