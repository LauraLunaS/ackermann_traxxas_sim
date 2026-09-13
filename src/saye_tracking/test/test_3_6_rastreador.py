"""
Submodulo 3.6 - teste do laco completo do rastreador (3.1-3.5 juntos).

Cenarios fabricados, sem ROS: aparicao, deteccao ruido de 1 frame,
oclusao curta (recupera com o MESMO id via OCR/ORU), oclusao longa
(apaga - nao recupera), e duas trajetorias se cruzando (nao troca id,
via OCM).

Parametros de tolerancia mais curtos que o padrao pra manter os testes
rapidos (poucos ciclos), mas a logica e a mesma que rodaria em producao.
"""
from saye_tracking.rastreador import Rastreador3D


def _rastreador(**kwargs):
    padrao = {
        'min_hits_confirmar': 2,
        'tolerancia_tentativo_segundos': 0.35,
        'tolerancia_perdido_segundos': 1.0,
        'gate_distancia': 1.0,
    }
    padrao.update(kwargs)
    return Rastreador3D(**padrao)


def test_deteccao_isolada_e_apagada_sem_confirmar():
    r = _rastreador()
    r.processar([(0.0, 0.0)], tempo_atual=0.0)

    # nunca mais aparece nada perto - depois da tolerancia de tentativo,
    # tem que sumir (nao ficou confirmado, so 1 deteccao)
    confirmados = r.processar([], tempo_atual=1.0)

    assert confirmados == []
    assert r.tracks == []


def test_deteccao_persistente_confirma_e_mantem_id():
    r = _rastreador()
    dt = 0.1
    posicao = 0.0
    ids = set()

    for k in range(5):
        confirmados = r.processar([(posicao, 0.0)], tempo_atual=k * dt)
        if confirmados:
            ids.add(confirmados[0].id)
        posicao += 0.1 * dt  # anda devagar

    assert len(ids) == 1  # o mesmo id o tempo todo, uma vez confirmado


def test_sobrevive_a_oclusao_curta_com_mesmo_id():
    r = _rastreador()
    dt = 0.1

    # confirma o track andando em +x
    r.processar([(0.0, 0.0)], tempo_atual=0.0)
    confirmados = r.processar([(0.1, 0.0)], tempo_atual=dt)
    assert len(confirmados) == 1
    id_original = confirmados[0].id

    # "oclusao": 3 ciclos sem nenhuma deteccao (dentro da tolerancia de 1.0s)
    for k in range(2, 5):
        r.processar([], tempo_atual=k * dt)

    # reaparece perto de onde a trajetoria projetava
    confirmados = r.processar([(0.5, 0.0)], tempo_atual=5 * dt)

    assert len(confirmados) == 1
    assert confirmados[0].id == id_original  # RECUPEROU o mesmo id, nao criou outro


def test_oclusao_longa_apaga_e_nao_recupera():
    r = _rastreador()
    dt = 0.1

    r.processar([(0.0, 0.0)], tempo_atual=0.0)
    confirmados = r.processar([(0.1, 0.0)], tempo_atual=dt)
    id_original = confirmados[0].id

    # oclusao BEM mais longa que a tolerancia de perdido (1.0s) - o track
    # original tem que ser apagado nesta chamada (sem deteccao nenhuma)
    r.processar([], tempo_atual=3.0)
    assert r.tracks == []

    # reaparece uma deteccao perto de onde ele estava - como o track velho
    # nao existe mais, isso tem que criar um track NOVO (tentativo), nao
    # recuperar o antigo
    confirmados = r.processar([(0.5, 0.0)], tempo_atual=3.1)

    assert confirmados == []  # o novo track ainda e so tentativo (1 hit)
    assert len(r.tracks) == 1
    assert r.tracks[0].id != id_original


def test_duas_trajetorias_cruzando_nao_trocam_id():
    r = _rastreador(peso_ocm=1.0)
    dt = 0.1

    # A anda em +x a partir de x=0; B anda em -x a partir de x=1 - se
    # cruzam por volta do 3o ciclo (rapido o bastante pra realmente passar
    # um pelo outro dentro do teste, nao so se aproximar)
    pos_a, pos_b = 0.0, 1.0
    vel_a, vel_b = 2.0, -2.0

    id_a = id_b = None
    for k in range(10):
        tempo = k * dt
        confirmados = r.processar([(pos_a, 0.0), (pos_b, 0.0)], tempo_atual=tempo)
        if k == 1:  # 2a rodada: ja confirmado (min_hits_confirmar=2)
            assert len(confirmados) == 2
            # o mais a esquerda e o "A" (comecou em x=0 andando p/ +x)
            confirmados_ordenados = sorted(confirmados, key=lambda t: t.posicao[0])
            id_a, id_b = confirmados_ordenados[0].id, confirmados_ordenados[1].id
        pos_a += vel_a * dt
        pos_b += vel_b * dt

    # depois de cruzarem (A e B ja trocaram de lado fisicamente), confere
    # que CADA id continua na trajetoria que comecou - A (indo p/ +x)
    # tem que estar na FRENTE de B (indo p/ -x), sem troca de identidade
    finais = {t.id: t.posicao[0] for t in r.tracks_confirmados()}
    assert id_a in finais and id_b in finais
    assert finais[id_a] > finais[id_b]


def test_deteccao_sem_par_cria_track_novo():
    r = _rastreador()

    confirmados = r.processar([(0.0, 0.0)], tempo_atual=0.0)

    assert confirmados == []  # ainda tentativo, so 1 hit
    assert len(r.tracks) == 1
