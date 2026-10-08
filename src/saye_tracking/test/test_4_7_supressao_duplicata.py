"""
Submodulo 4.7 - supressao de duplicata na criacao de tracks novos.

Reproduz, com dados fabricados, o padrao de falha achado na analise ao
vivo da Fase 4.6 (3 pessoas reais andando, gravacao de 45s de
`/tracker_node/tracks`): perto do cruzamento geometrico de dois
caminhos, surgia um id "fantasma" de vida curta a poucos centimetros de
um track ja existente, bem no ciclo em que esse track era observado.

Estes testes confirmam que `Rastreador3D._filtrar_duplicatas` impede
exatamente esse caso (deteccao extra MUITO perto de um track recem
atualizado nao abre track novo), sem impedir o caso legitimo (pessoa
nova aparecendo longe de qualquer track atualizado nesta rodada).
"""
from saye_tracking.rastreador import Rastreador3D


def _rastreador(**kwargs):
    padrao = {
        'min_hits_confirmar': 2,
        'tolerancia_tentativo_segundos': 0.35,
        'tolerancia_perdido_segundos': 1.0,
        'gate_distancia': 1.0,
        'raio_supressao_duplicata': 0.5,
    }
    padrao.update(kwargs)
    return Rastreador3D(**padrao)


def test_deteccao_fantasma_perto_de_track_atualizado_nao_cria_track_novo():
    r = _rastreador()
    dt = 0.1

    # confirma um unico track andando em +x
    r.processar([(0.0, 0.0)], tempo_atual=0.0)
    r.processar([(0.1, 0.0)], tempo_atual=dt)
    assert len(r.tracks) == 1

    # nesta rodada chegam DUAS deteccoes: a boa (que casa com o track
    # existente) e uma "fantasma" a 15cm dela - exatamente o padrao visto
    # na analise (ids 102/104/105, todos a <20cm de um track recem
    # atualizado no mesmo ciclo)
    r.processar([(0.2, 0.0), (0.2, 0.15)], tempo_atual=2 * dt)

    assert len(r.tracks) == 1  # a fantasma NAO abriu track novo


def test_deteccao_longe_de_tudo_ainda_cria_track_novo():
    r = _rastreador()
    dt = 0.1

    r.processar([(0.0, 0.0)], tempo_atual=0.0)
    r.processar([(0.1, 0.0)], tempo_atual=dt)
    assert len(r.tracks) == 1

    # deteccao nova, bem longe (5m) do track existente - pessoa de verdade
    # aparecendo em outro lugar, tem que abrir track proprio normalmente
    r.processar([(0.2, 0.0), (5.0, 5.0)], tempo_atual=2 * dt)

    assert len(r.tracks) == 2


def test_raio_de_supressao_pequeno_nao_afeta_pessoas_de_verdade_proximas():
    # duas pessoas reais passando a 0.8m uma da outra (mais que o raio de
    # supressao padrao de 0.5m) - as duas tem que confirmar como tracks
    # distintos, a supressao nao pode "engolir" gente de verdade so por
    # estar relativamente proxima
    r = _rastreador()
    dt = 0.1

    r.processar([(0.0, 0.0), (0.8, 0.0)], tempo_atual=0.0)
    confirmados = r.processar([(0.0, 0.0), (0.8, 0.0)], tempo_atual=dt)

    assert len(confirmados) == 2
