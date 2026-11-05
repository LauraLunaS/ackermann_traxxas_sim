"""
Correcao de movimentacao (pos-4.9) - `TeleportadorEmLote`, sem Gazebo de verdade.

Usa um cliente gz-transport FAKE (so grava o que foi chamado) pra testar
que `TeleportadorEmLote` monta o `Pose_V` certo e, principalmente, que
NUNCA finge sucesso quando a chamada falhou - era exatamente esse retorno
ignorado, no no antigo (`mover_pessoa_animada_node`), que causava a falha
silenciosa documentada em `gz_pose_vector.py`.
"""
from gz.msgs10.boolean_pb2 import Boolean
from saye_tracking.gz_pose_vector import TeleportadorEmLote


class _ClienteGzFake:
    def __init__(self, ok=True, sucesso=True):
        self.ok = ok
        self.sucesso = sucesso
        self.chamadas = []

    def request(self, servico, req, tipo_req, tipo_resp, timeout):
        self.chamadas.append((servico, req, timeout))
        return self.ok, Boolean(data=self.sucesso)


def test_teleportar_monta_uma_pose_por_entrada_com_nome_e_posicao_certos():
    cliente = _ClienteGzFake()
    teleportador = TeleportadorEmLote('beach_world', cliente_gz=cliente)

    teleportador.teleportar([
        ('pessoa_1_frame_0', 1.0, 2.0, 0.0, 0.0),
        ('pessoa_2_frame_3', 3.0, 4.0, -50.0, 1.57),
    ])

    assert len(cliente.chamadas) == 1
    servico, req, _timeout = cliente.chamadas[0]
    assert servico == '/world/beach_world/set_pose_vector'
    assert [p.name for p in req.pose] == ['pessoa_1_frame_0', 'pessoa_2_frame_3']
    p0, p1 = req.pose
    assert (p0.position.x, p0.position.y, p0.position.z) == (1.0, 2.0, 0.0)
    assert (p1.position.x, p1.position.y, p1.position.z) == (3.0, 4.0, -50.0)


def test_teleportar_so_1_chamada_pra_qualquer_quantidade_de_poses():
    cliente = _ClienteGzFake()
    teleportador = TeleportadorEmLote('beach_world', cliente_gz=cliente)

    poses = [(f'pessoa_{i}_frame_0', float(i), 0.0, 0.0, 0.0) for i in range(5)]
    teleportador.teleportar(poses)

    assert len(cliente.chamadas) == 1  # NUNCA 1 chamada por pose


def test_teleportar_reporta_falha_quando_gazebo_recusa_a_pose():
    cliente = _ClienteGzFake(ok=True, sucesso=False)
    teleportador = TeleportadorEmLote('beach_world', cliente_gz=cliente)

    ok, sucesso = teleportador.teleportar([('pessoa_1_frame_0', 0.0, 0.0, 0.0, 0.0)])

    assert ok is True
    assert sucesso is False  # NUNCA mascarar recusa do Gazebo como sucesso


def test_teleportar_reporta_falha_quando_servico_nao_responde():
    cliente = _ClienteGzFake(ok=False, sucesso=True)
    teleportador = TeleportadorEmLote('beach_world', cliente_gz=cliente)

    ok, sucesso = teleportador.teleportar([('pessoa_1_frame_0', 0.0, 0.0, 0.0, 0.0)])

    assert ok is False
    assert sucesso is False  # sem resposta nunca pode contar como sucesso
