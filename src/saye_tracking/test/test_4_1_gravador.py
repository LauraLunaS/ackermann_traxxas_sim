"""Submodulo 4.1 - teste do gravador (hipotese/verdade -> CSV), sem ROS."""
import os
import tempfile

from saye_tracking.gravador import carregar_csv, Gravador


def test_registra_hipotese_e_verdade_em_listas_separadas():
    g = Gravador()

    g.registrar_hipotese(tempo=1.0, id_track=3, x=1.5, y=2.5)
    g.registrar_verdade(tempo=1.0, id_objeto='pessoa_detectavel', x=1.6, y=2.4)

    assert g.hipoteses == [(1.0, '3', 1.5, 2.5)]
    assert g.verdade == [(1.0, 'pessoa_detectavel', 1.6, 2.4)]


def test_salvar_e_carregar_csv_preserva_os_dados():
    g = Gravador()
    g.registrar_hipotese(tempo=0.1, id_track=1, x=0.0, y=0.0)
    g.registrar_hipotese(tempo=0.2, id_track=1, x=0.1, y=0.0)
    g.registrar_verdade(tempo=0.1, id_objeto='pessoa_detectavel', x=0.05, y=0.02)

    with tempfile.TemporaryDirectory() as tmp:
        caminho_hip = os.path.join(tmp, 'hipoteses.csv')
        caminho_gt = os.path.join(tmp, 'verdade.csv')
        g.salvar(caminho_hip, caminho_gt)

        assert os.path.exists(caminho_hip)
        assert os.path.exists(caminho_gt)

        hip_lidas = carregar_csv(caminho_hip)
        gt_lidas = carregar_csv(caminho_gt)

    assert hip_lidas == g.hipoteses
    assert gt_lidas == g.verdade


def test_gravador_vazio_salva_apenas_cabecalho():
    g = Gravador()

    with tempfile.TemporaryDirectory() as tmp:
        caminho_hip = os.path.join(tmp, 'hipoteses.csv')
        caminho_gt = os.path.join(tmp, 'verdade.csv')
        g.salvar(caminho_hip, caminho_gt)

        assert carregar_csv(caminho_hip) == []
        assert carregar_csv(caminho_gt) == []
