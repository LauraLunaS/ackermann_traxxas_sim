"""Submodulo 4.4 - teste do formatador de relatorio e do comando de reset, sem ROS/sim."""
from saye_tracking.relatorio import formatar_relatorio
from saye_tracking.rodar_suite import comando_resetar_pose


def _resumo(num_frames=10, mota=0.8, motp=0.03, num_switches=0,
            num_false_positives=0, num_misses=1, num_matches=9):
    return {
        'num_frames': num_frames, 'mota': mota, 'motp': motp,
        'num_switches': num_switches, 'num_false_positives': num_false_positives,
        'num_misses': num_misses, 'num_matches': num_matches,
    }


def test_relatorio_tem_uma_linha_por_cenario():
    resultados = [('parado', _resumo()), ('linear', _resumo(mota=0.1))]

    texto = formatar_relatorio(resultados)

    assert texto.count('\n') == 3  # cabecalho + separador + 2 cenarios
    assert 'parado' in texto
    assert 'linear' in texto


def test_relatorio_formata_floats_com_3_casas():
    resultados = [('parado', _resumo(mota=0.816327))]

    texto = formatar_relatorio(resultados)

    assert '0.816' in texto


def test_relatorio_cabecalho_lista_todas_as_colunas():
    texto = formatar_relatorio([('parado', _resumo())])

    for coluna in ['mota', 'motp', 'num_switches', 'num_matches']:
        assert coluna in texto.split('\n')[0]


def test_comando_resetar_pose_usa_nome_e_posicao_corretos():
    comando = comando_resetar_pose('beach_world', 'traxxas', -1.0, 1.0, 0.15)

    assert comando[:4] == ['gz', 'service', '-s', '/world/beach_world/set_pose']
    req = comando[comando.index('--req') + 1]
    assert 'name: "traxxas"' in req
    assert 'x: -1.0' in req
    assert 'y: 1.0' in req
