"""
Extrai poses estaticas do ciclo de caminhada de um .dae com esqueleto.

COLLADA skin+animation, aplicando skinning manual (linear blend skinning)
em cada keyframe escolhido, e exporta cada pose como um .obj + .mtl
separado (malha estatica, sem esqueleto) com posicoes, normais e UVs
skinadas - reaproveitando a textura original.

Uso: python3 bake_walk_frames.py entrada.dae textura_diffuse.png saida_dir/ n_frames
"""
import os
import sys

import collada
from lxml import etree
import numpy as np


def carregar_sources_samplers_channels(caminho_dae):
    tree = etree.parse(caminho_dae)
    root = tree.getroot()
    C = root.tag.split('}')[0].strip('{')

    def q(tag):
        return '{%s}%s' % (C, tag)

    sources = {}
    for src in root.iter(q('source')):
        sid = src.get('id')
        arr = src.find(q('float_array'))
        if arr is not None and arr.text:
            sources[sid] = np.array(arr.text.split(), dtype=float)

    samplers = {}
    for samp in root.iter(q('sampler')):
        sid = samp.get('id')
        entradas = {}
        for inp in samp.iter(q('input')):
            entradas[inp.get('semantic')] = inp.get('source').lstrip('#')
        samplers[sid] = entradas

    channels = {}  # node_id -> sampler_id
    for ch in root.iter(q('channel')):
        alvo = ch.get('target')
        node_id = alvo.split('/')[0]
        channels[node_id] = ch.get('source').lstrip('#')

    return root, C, sources, samplers, channels


def construir_hierarquia(root, C, node_id_raiz):
    def q(tag):
        return '{%s}%s' % (C, tag)

    raiz = None
    for node in root.iter(q('node')):
        if node.get('id') == node_id_raiz:
            raiz = node
            break
    if raiz is None:
        raise ValueError(f'no raiz {node_id_raiz} nao encontrado')

    def matriz_local_estatica(node_xml):
        m = node_xml.find(q('matrix'))
        if m is None:
            return np.eye(4)
        return np.array(m.text.split(), dtype=float).reshape(4, 4)

    def construir(node_xml):
        filhos = [construir(c) for c in node_xml.iterchildren(q('node'))]
        return {
            'id': node_xml.get('id'),
            'sid': node_xml.get('sid'),
            'local_estatica': matriz_local_estatica(node_xml),
            'filhos': filhos,
        }

    return construir(raiz)


def obter_matrizes_animadas(node_id, sources, samplers, channels):
    """Retorna (tempos, matrizes[N,4,4]) se o node tiver canal animado, senao None."""
    if node_id not in channels:
        return None
    samp = samplers[channels[node_id]]
    tempos = sources[samp['INPUT']]
    saida = sources[samp['OUTPUT']].reshape(-1, 4, 4)
    return tempos, saida


def calcular_mundiais(no, indice_keyframe, sources, samplers, channels, mundo_pai=None):
    if mundo_pai is None:
        mundo_pai = np.eye(4)

    animado = obter_matrizes_animadas(no['id'], sources, samplers, channels)
    if animado is not None:
        _, matrizes = animado
        local = matrizes[indice_keyframe % len(matrizes)]
    else:
        local = no['local_estatica']

    mundo = mundo_pai @ local
    resultado = {no['sid']: mundo} if no['sid'] else {}
    for filho in no['filhos']:
        resultado.update(calcular_mundiais(
            filho, indice_keyframe, sources, samplers, channels, mundo))
    return resultado


def aplicar_skinning(skin, mundiais_por_joint):
    geom_prim = skin.geometry.primitives[0].triangleset()
    vertices_bind = geom_prim.vertex  # (Nv, 3)
    bind_shape = np.array(skin.bind_shape_matrix).reshape(4, 4)

    nomes_joints = [n[0] for n in skin.weight_joints.data]
    inv_bind_por_joint = {
        nome: np.array(mat).reshape(4, 4)
        for nome, mat in skin.joint_matrices.items()
    }
    pesos_valores = skin.weights.data.flatten()

    n = len(vertices_bind)
    posicoes_posadas = np.zeros((n, 3))
    rotacoes_blend = np.zeros((n, 3, 3))

    for i in range(n):
        v_bind = bind_shape @ np.array([*vertices_bind[i], 1.0])
        acumulado = np.zeros(4)
        rot_acumulada = np.zeros((3, 3))
        soma_pesos = 0.0
        for jidx, widx in zip(skin.joint_index[i], skin.weight_index[i]):
            nome_joint = nomes_joints[jidx]
            peso = pesos_valores[widx]
            if nome_joint not in mundiais_por_joint:
                continue
            mundo_joint = mundiais_por_joint[nome_joint]
            inv_bind = inv_bind_por_joint[nome_joint]
            acumulado += peso * (mundo_joint @ inv_bind @ v_bind)
            rot_acumulada += peso * (mundo_joint @ inv_bind)[:3, :3]
            soma_pesos += peso
        if soma_pesos > 1e-8:
            acumulado /= soma_pesos
            rot_acumulada /= soma_pesos
        else:
            rot_acumulada = np.eye(3)
        posicoes_posadas[i] = acumulado[:3]
        rotacoes_blend[i] = rot_acumulada

    bind_rot = bind_shape[:3, :3]
    return posicoes_posadas, rotacoes_blend, bind_rot, geom_prim


def exportar_obj(caminho_obj, posicoes, rotacoes_blend, bind_rot, geom_prim, nome_textura):
    texcoords = geom_prim.texcoordset[0]
    normais_bind = geom_prim.normal
    vertex_index = geom_prim.vertex_index
    texcoord_index = geom_prim.texcoord_indexset[0]
    normal_index = geom_prim.normal_index

    chaves_normal = {}
    normais_posadas = []
    for face_i in range(len(vertex_index)):
        for k in range(3):
            chave = (vertex_index[face_i][k], normal_index[face_i][k])
            if chave not in chaves_normal:
                vi, ni = chave
                n = rotacoes_blend[vi] @ (bind_rot @ normais_bind[ni])
                n = n / (np.linalg.norm(n) + 1e-12)
                chaves_normal[chave] = len(normais_posadas) + 1
                normais_posadas.append(n)

    nome_mtl = os.path.splitext(os.path.basename(caminho_obj))[0] + '.mtl'
    with open(caminho_obj, 'w') as f:
        f.write(f'mtllib {nome_mtl}\nusemtl material0\n')
        for v in posicoes:
            f.write(f'v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n')
        for vt in texcoords:
            f.write(f'vt {vt[0]:.6f} {vt[1]:.6f}\n')
        for vn in normais_posadas:
            f.write(f'vn {vn[0]:.6f} {vn[1]:.6f} {vn[2]:.6f}\n')
        for face_i in range(len(vertex_index)):
            linha = []
            for k in range(3):
                vi = vertex_index[face_i][k] + 1
                ti = texcoord_index[face_i][k] + 1
                ni = chaves_normal[(vertex_index[face_i][k], normal_index[face_i][k])]
                linha.append(f'{vi}/{ti}/{ni}')
            f.write('f ' + ' '.join(linha) + '\n')

    caminho_mtl = os.path.join(os.path.dirname(caminho_obj), nome_mtl)
    with open(caminho_mtl, 'w') as f:
        f.write(f'newmtl material0\nKd 1 1 1\nmap_Kd {nome_textura}\n')


def main():
    caminho_dae, caminho_textura, dir_saida, n_frames = (
        sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
    os.makedirs(dir_saida, exist_ok=True)

    mesh = collada.Collada(caminho_dae)
    skin = mesh.controllers[0]

    root, C, sources, samplers, channels = carregar_sources_samplers_channels(caminho_dae)

    primeiro_alvo_armature = list(channels.keys())[0]
    hierarquia = construir_hierarquia(root, C, primeiro_alvo_armature)

    algum_animado = obter_matrizes_animadas(
        next(iter(set(channels.keys()) - {primeiro_alvo_armature})),
        sources, samplers, channels)
    total_keyframes = len(algum_animado[0])
    print(f'total de keyframes disponiveis: {total_keyframes}')

    indices = np.linspace(0, total_keyframes - 1, n_frames).astype(int)
    nome_textura = os.path.basename(caminho_textura)

    for n_frame, idx in enumerate(indices):
        mundiais = calcular_mundiais(hierarquia, int(idx), sources, samplers, channels)
        posicoes, rotacoes, bind_rot, geom_prim = aplicar_skinning(skin, mundiais)
        caminho_obj = os.path.join(dir_saida, f'walk_{n_frame:02d}.obj')
        exportar_obj(caminho_obj, posicoes, rotacoes, bind_rot, geom_prim, nome_textura)
        print(f'frame {n_frame} (keyframe {idx}) -> {caminho_obj}')


if __name__ == '__main__':
    main()
