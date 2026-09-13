"""Submodulo 3.2 - teste da maquina de estados do Track (por tempo, sem ROS)."""
from saye_tracking.track import EstadoTrack, Track


def test_track_novo_comeca_tentativo_com_id_unico():
    t1 = Track(posicao_inicial=(0.0, 0.0), tempo_criacao=0.0)
    t2 = Track(posicao_inicial=(1.0, 1.0), tempo_criacao=0.0)

    assert t1.estado == EstadoTrack.TENTATIVO
    assert t2.estado == EstadoTrack.TENTATIVO
    assert t1.id != t2.id


def test_confirma_apos_min_hits():
    t = Track(posicao_inicial=(0.0, 0.0), tempo_criacao=0.0, min_hits_confirmar=3)

    t.observar((0.1, 0.0), tempo_atual=0.1)  # hit 2
    assert t.estado == EstadoTrack.TENTATIVO

    t.observar((0.2, 0.0), tempo_atual=0.2)  # hit 3
    assert t.estado == EstadoTrack.CONFIRMADO


def test_tentativo_nao_reobservado_a_tempo_e_apagado():
    t = Track(posicao_inicial=(0.0, 0.0), tempo_criacao=0.0,
              tolerancia_tentativo_segundos=0.4)

    assert t.deve_ser_apagado(tempo_atual=0.3) is False
    assert t.deve_ser_apagado(tempo_atual=0.5) is True


def test_confirmado_vira_perdido_quando_nao_observado_no_ciclo():
    t = Track(posicao_inicial=(0.0, 0.0), tempo_criacao=0.0, min_hits_confirmar=2)
    t.observar((0.0, 0.0), tempo_atual=0.1)  # hit 2 -> confirmado
    assert t.estado == EstadoTrack.CONFIRMADO

    t.marcar_nao_observado()

    assert t.estado == EstadoTrack.PERDIDO


def test_perdido_recupera_ao_ser_observado_de_novo():
    t = Track(posicao_inicial=(0.0, 0.0), tempo_criacao=0.0, min_hits_confirmar=2)
    t.observar((0.0, 0.0), tempo_atual=0.1)
    t.marcar_nao_observado()
    assert t.estado == EstadoTrack.PERDIDO

    t.observar((0.05, 0.0), tempo_atual=0.3)

    assert t.estado == EstadoTrack.CONFIRMADO


def test_confirmado_e_perdido_tem_mais_paciencia_que_tentativo():
    t = Track(posicao_inicial=(0.0, 0.0), tempo_criacao=0.0, min_hits_confirmar=2,
              tolerancia_tentativo_segundos=0.4, tolerancia_perdido_segundos=1.5)
    t.observar((0.0, 0.0), tempo_atual=0.1)  # confirmado
    t.marcar_nao_observado()  # perdido, ultima observacao em t=0.1

    # passou mais que a tolerancia de TENTATIVO, mas nao a de PERDIDO
    assert t.deve_ser_apagado(tempo_atual=0.6) is False
    # agora passou da tolerancia de PERDIDO
    assert t.deve_ser_apagado(tempo_atual=1.7) is True


def test_marcar_nao_observado_nao_afeta_tentativo():
    t = Track(posicao_inicial=(0.0, 0.0), tempo_criacao=0.0)

    t.marcar_nao_observado()

    assert t.estado == EstadoTrack.TENTATIVO


def test_prever_avanca_o_kalman_com_dt_correto():
    t = Track(posicao_inicial=(0.0, 0.0), tempo_criacao=0.0)
    t.kalman.x[2:] = [2.0, 0.0]  # forca velocidade conhecida (2 m/s em x)

    t.prever(tempo_atual=1.5)

    assert t.posicao[0] == 3.0
