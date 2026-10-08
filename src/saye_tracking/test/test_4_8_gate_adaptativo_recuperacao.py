"""
Submodulo 4.8 - gate adaptativo + OCM na recuperacao (OCR).

Via o laco completo do `Rastreador3D` (nao so `recuperacao.py` isolado).

Motivacao (achado ao vivo, gravacao de 96.8s com 3 pessoas reais
andando): um unico id sobrevivia a sessao TODA (parecia perfeito), mas a
trajetoria dele continha saltos de 0.6-1.0m em 0.2-0.3s (2.7-3.4 m/s) -
10x a velocidade maxima configurada de qualquer pessoa. O id estava
pulando silenciosamente entre pessoas reais diferentes sempre que uma
delas perdia 1 frame de deteccao perto de outra - porque o OCR usava o
MESMO gate fixo (1.5m) do turno normal, sem levar em conta quanto tempo
o track estava perdido nem a direcao do movimento.

Estes testes reproduzem esse padrao com 2 "pessoas" fabricadas perto uma
da outra (menos que o gate global, mas mais do que uma pessoa real
consegue andar no tempo em que uma deteccao falha) e confirmam que o
gate adaptativo agora rejeita a troca.
"""
from saye_tracking.rastreador import Rastreador3D


def _rastreador(**kwargs):
    padrao = {
        'min_hits_confirmar': 2,
        'tolerancia_tentativo_segundos': 0.35,
        'tolerancia_perdido_segundos': 1.5,
        'gate_distancia': 1.5,  # igual ao padrao de producao (tracker_node)
        'velocidade_maxima_esperada': 0.6,
        'margem_gate_recuperacao': 0.3,
    }
    padrao.update(kwargs)
    return Rastreador3D(**padrao)


def test_nao_troca_para_pessoa_diferente_perto_quando_perde_1_deteccao():
    """
    Nao deixa o id de uma pessoa ser roubado por outra perto so por perder 1 frame.

    2 pessoas reais a 1.0m uma da outra (dentro do gate global de 1.5m,
    mas MUITO alem do que uma pessoa anda em 1 frame perdido) - A em
    x=0.0, B em x=1.0, ambas paradas (sem momentum, pro OCM nao interferir
    neste teste - so o gate adaptativo esta sendo testado aqui). A perde
    1 frame de deteccao (fica PERDIDO por 1 ciclo); nesse mesmo ciclo B
    continua sendo detectada normalmente. A deteccao de A tem que ficar
    SEM PAR (nao pode "roubar" o id de B), e o id de B tem que continuar
    casando com B - nenhum dos dois pode trocar de identidade.
    """
    r = _rastreador()
    dt = 0.1

    # confirma os 2 tracks
    r.processar([(0.0, 0.0), (1.0, 0.0)], tempo_atual=0.0)
    confirmados = r.processar([(0.0, 0.0), (1.0, 0.0)], tempo_atual=dt)
    assert len(confirmados) == 2
    por_x = {round(t.posicao[0]): t.id for t in confirmados}
    id_a, id_b = por_x[0], por_x[1]

    # ciclo seguinte: SO a deteccao de B chega (A "perdeu" 1 frame) -
    # tempo perdido de A sera bem pequeno (1 ciclo), entao o gate
    # adaptativo tem que ser bem menor que a distancia at'e B (1.0m)
    confirmados = r.processar([(1.0, 0.0)], tempo_atual=2 * dt)
    ids_presentes = {t.id for t in confirmados}

    assert id_b in ids_presentes  # B continua sendo B
    assert id_a not in [t.id for t in r.tracks if t.posicao[0] > 0.5]  # A nao "virou" B

    # A reaparece no lugar certo pouco depois - tem que RECUPERAR o
    # mesmo id original (nao criar um 3o id, nem ter sido consumido por B)
    confirmados = r.processar([(0.0, 0.0), (1.0, 0.0)], tempo_atual=3 * dt)
    ids_finais = {round(t.posicao[0]): t.id for t in confirmados}
    assert ids_finais[0] == id_a
    assert ids_finais[1] == id_b


def test_gate_global_ainda_permite_recuperacao_legitima_de_oclusao_longa():
    """
    Garante que o gate adaptativo nao regride o caso legitimo de oclusao real.

    1 pessoa
    SOZINHA (sem ninguem por perto pra confundir), perdida por varios
    ciclos (oclusao real), tem que continuar recuperando pelo MESMO id
    quando reaparece onde a trajetoria real levaria - exatamente o
    cenario que o `test_3_6_rastreador.test_sobrevive_a_oclusao_curta_com_mesmo_id`
    ja cobria, repetido aqui como guarda de regressao da 4.8.
    """
    r = _rastreador()
    dt = 0.1

    r.processar([(0.0, 0.0)], tempo_atual=0.0)
    confirmados = r.processar([(0.1, 0.0)], tempo_atual=dt)
    id_original = confirmados[0].id

    for k in range(2, 5):
        r.processar([], tempo_atual=k * dt)

    confirmados = r.processar([(0.5, 0.0)], tempo_atual=5 * dt)

    assert len(confirmados) == 1
    assert confirmados[0].id == id_original
