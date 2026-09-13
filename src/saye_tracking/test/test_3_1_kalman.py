"""
Submodulo 3.1 - teste do filtro de Kalman de 1 track.

Puro numpy, sem ROS (sem rclpy.init) - a mesma vantagem de nao precisar de
simulador que tivemos nos testes sinteticos das fases anteriores, mas aqui
nem precisa subir um no.
"""
import numpy as np
from saye_tracking.kalman import FiltroKalman


def test_estado_inicial_ancora_na_posicao_sem_velocidade():
    f = FiltroKalman(posicao_inicial=(5.0, 3.0))

    np.testing.assert_allclose(f.posicao, [5.0, 3.0])
    np.testing.assert_allclose(f.velocidade, [0.0, 0.0])


def test_predict_extrapola_em_linha_reta():
    f = FiltroKalman(posicao_inicial=(0.0, 0.0))
    f.x[2:] = [2.0, 1.0]  # forca uma velocidade conhecida (2, 1) m/s

    f.predict(dt=1.0)

    np.testing.assert_allclose(f.posicao, [2.0, 1.0], atol=1e-9)
    # velocidade constante: nao muda so por prever
    np.testing.assert_allclose(f.velocidade, [2.0, 1.0], atol=1e-9)


def test_incerteza_de_posicao_cresce_sem_medicao():
    f = FiltroKalman(posicao_inicial=(0.0, 0.0), ruido_processo=0.5)
    variancias = [f.P[0, 0]]
    for _ in range(5):
        f.predict(dt=0.1)
        variancias.append(f.P[0, 0])

    # cada predict sem update deixa o filtro MENOS confiante, nunca mais
    assert all(v2 >= v1 for v1, v2 in zip(variancias, variancias[1:]))
    assert variancias[-1] > variancias[0]


def test_update_corrige_em_direcao_da_medicao_sem_saltar_pra_ela():
    f = FiltroKalman(posicao_inicial=(0.0, 0.0))
    f.x[2:] = [1.0, 0.0]
    f.predict(dt=1.0)  # previsao: (1.0, 0.0)

    medicao = np.array([1.3, 0.0])  # medida real veio um pouco mais a frente
    f.update(medicao)

    # o resultado fica ENTRE a previsao e a medicao (fusao), nao igual a
    # nenhum dos dois
    assert 1.0 < f.posicao[0] < 1.3


def test_converge_para_a_velocidade_real_sem_ruido():
    velocidade_real = np.array([1.0, 0.5])
    posicao = np.array([0.0, 0.0])
    dt = 0.1

    f = FiltroKalman(posicao_inicial=tuple(posicao))
    for _ in range(30):
        posicao = posicao + velocidade_real * dt
        f.predict(dt)
        f.update(posicao)

    np.testing.assert_allclose(f.velocidade, velocidade_real, atol=0.05)
    np.testing.assert_allclose(f.posicao, posicao, atol=0.05)


def test_converge_para_a_velocidade_real_com_ruido_de_medicao():
    rng = np.random.default_rng(42)
    velocidade_real = np.array([0.8, -0.3])
    posicao_real = np.array([0.0, 0.0])
    dt = 0.1
    desvio_ruido = 0.1  # mesma ordem do ruido_medicao default do filtro

    # ruido_processo baixo: o cenario e realmente velocidade constante, entao
    # dizemos ao filtro pra confiar bastante nesse modelo (menos "agil" pra
    # curvas, mais resistente ao ruido de cada medicao individual)
    f = FiltroKalman(posicao_inicial=(0.0, 0.0), ruido_medicao=desvio_ruido,
                     ruido_processo=0.05)
    for _ in range(60):
        posicao_real = posicao_real + velocidade_real * dt
        medicao_ruidosa = posicao_real + rng.normal(0, desvio_ruido, size=2)
        f.predict(dt)
        f.update(medicao_ruidosa)

    # mesmo com cada medicao individual ruidosa, a velocidade filtrada
    # converge bem mais perto da real do que o ruido de uma unica medicao
    erro_velocidade = np.linalg.norm(f.velocidade - velocidade_real)
    assert erro_velocidade < 0.1
