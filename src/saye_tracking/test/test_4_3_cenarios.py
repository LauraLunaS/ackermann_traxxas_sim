"""Submodulo 4.3 - teste dos roteiros de cenario, sem ROS/sim."""
from saye_tracking.cenarios import CENARIOS, comando_no_instante, duracao_total


def test_todos_os_cenarios_tem_pelo_menos_um_segmento_com_duracao_positiva():
    for nome, segmentos in CENARIOS.items():
        assert len(segmentos) > 0, nome
        for vx, wz, duracao in segmentos:
            assert duracao > 0.0, nome


def test_duracao_total_soma_os_segmentos():
    assert duracao_total('curva') == 2.0 + 4.0 + 2.0


def test_comando_no_instante_dentro_do_primeiro_segmento():
    assert comando_no_instante('linear', 0.0) == (0.4, 0.0)
    assert comando_no_instante('linear', 5.0) == (0.4, 0.0)


def test_comando_no_instante_avanca_para_o_proximo_segmento():
    # 'curva': 2s reto, depois 4s curvando, depois 2s reto
    assert comando_no_instante('curva', 1.0) == (0.3, 0.0)
    assert comando_no_instante('curva', 3.0) == (0.3, 0.4)
    assert comando_no_instante('curva', 7.0) == (0.3, 0.0)


def test_comando_no_instante_retorna_none_apos_o_fim():
    assert comando_no_instante('parado', duracao_total('parado') + 0.1) is None


def test_cenario_parado_nao_move_o_robo():
    assert comando_no_instante('parado', 0.0) == (0.0, 0.0)
