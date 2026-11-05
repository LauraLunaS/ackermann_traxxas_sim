"""
Teleporte em LOTE de varios modelos do Gazebo numa unica chamada de servico.

Correcao da bancada 4.9 (investigacao "movimentacao das pessoas"). Achado:
cada ator (`mover_pessoa_animada_node`, Fase 4.6) rodava como um PROCESSO
PROPRIO chamando `/world/<mundo>/set_pose` (1 pose por chamada) a 30Hz - com
3 atores, 3 clientes `gz-transport` concorrentes martelando o MESMO servico
nomeado. Reproduzido ao vivo (5+ rodadas): em ~33-50% das rodadas, UM dos
clientes passava a falhar 100% das chamadas pelo resto do teste (nao
intermitente - sistematico), sem que ningum notasse porque o `_teleportar`
original descartava o retorno `(bool, resposta)` do `request()` sem checar.
Recriar o `Node()` gz-transport depois de falhas consecutivas NAO recuperava
(testado: ainda 0% de sucesso apos 6 recriacoes). O sintoma observado era
"verdade.csv" de uma pessoa congelada no pose de estacionamento (z=-50)
durante parte do teste, inflando trocas de id/falsos negativos que pareciam
bug do RASTREADOR mas eram, na verdade, corrupcao da propria simulacao.

Correcao: 1 SO cliente gz-transport (1 processo, `mover_pessoas_node.py`),
1 SO chamada por tick, usando `/world/<mundo>/set_pose_vector` (aceita uma
lista de poses) em vez de 1 chamada de `set_pose` por pessoa. Sem concorrencia
entre clientes = sem o bug acima (nunca mais reproduzido testando assim).
E TODA chamada aqui tem o retorno checado por quem usa `TeleportadorEmLote`
- nenhuma falha deve voltar a passar despercebida.
"""
import math

from gz.msgs10.boolean_pb2 import Boolean
from gz.msgs10.pose_pb2 import Pose
from gz.msgs10.pose_v_pb2 import Pose_V
from gz.transport13 import Node as NodeGz


def montar_pose(nome, x, y, z, yaw=0.0):
    """Monta um `gz.msgs.Pose` (nome + posicao + orientacao so em yaw)."""
    p = Pose()
    p.name = nome
    p.position.x = x
    p.position.y = y
    p.position.z = z
    p.orientation.z = math.sin(yaw / 2.0)
    p.orientation.w = math.cos(yaw / 2.0)
    return p


class TeleportadorEmLote:
    """Cliente gz-transport unico: teleporta N modelos numa so chamada."""

    def __init__(self, mundo, timeout_ms=300, cliente_gz=None):
        self.servico = f'/world/{mundo}/set_pose_vector'
        self.timeout_ms = timeout_ms
        # injeção pra teste (fake), sem Gazebo de verdade
        self.no_gz = cliente_gz if cliente_gz is not None else NodeGz()

    def teleportar(self, poses):
        """
        Teleporta todas as `poses` numa so chamada de `set_pose_vector`.

        `poses`: lista de (nome, x, y, z, yaw).

        Retorna (ok, sucesso): `ok` e se a chamada gz-transport completou
        dentro do timeout (False = sem resposta nenhuma, ex.: servico fora
        do ar); `sucesso` e se o Gazebo CONFIRMOU ter aplicado as poses
        (`resposta.data`). Nunca levanta excecao - quem chama decide o que
        fazer com a falha, mas e OBRIGADO a checar (ver achado no topo do
        arquivo: a falha silenciosa e exatamente o que corrompeu a bancada).
        """
        req = Pose_V()
        for nome, x, y, z, yaw in poses:
            req.pose.append(montar_pose(nome, x, y, z, yaw))
        ok, resposta = self.no_gz.request(
            self.servico, req, Pose_V, Boolean, self.timeout_ms)
        sucesso = bool(ok and resposta is not None and resposta.data)
        return ok, sucesso
