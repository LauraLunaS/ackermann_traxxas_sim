#!/usr/bin/env python3
"""
Converte o KITTI Tracking Benchmark (so pedestres) pro formato YOLOv8-seg.

Pra fine-tuning do `deteccao_node` com um dataset maior/mais real que o
COCO sozinho.

Por que SEGMENTACAO e nao so deteccao: `deteccao_node` roda `yolov8n-seg` e
`projecao3d_node` usa a MASCARA (nao a bbox) pra amostrar profundidade -
trocar pro modelo de deteccao pura quebraria a Fase 2 inteira. O KITTI so
tem rotulo de caixa (bbox), sem mascara de instancia. Solucao pragmatica:
cada bbox vira um poligono retangular (os 4 cantos da caixa) no formato de
rotulo de segmentacao do YOLO - nao e uma silhueta de verdade, mas e um
rotulo valido pro treino continuar. Por isso o `treinar_yolo_kitti.py`
recomenda poucas epocas + taxa de aprendizado baixa + congelar o backbone:
a ideia e melhorar a deteccao/classificacao de pedestre em cenas reais,
sem destruir a qualidade de mascara que o modelo ja aprendeu no COCO.

Uso:
    python3 preparar_dataset_kitti.py \
        --kitti_dir /caminho/pra/kitti_tracking/training \
        --saida /caminho/pra/dataset_kitti_pessoas \
        [--val_sequencias 0,1,2,3] [--incluir_person_sitting]

`--kitti_dir` precisa conter `image_02/<seq>/*.png` e `label_02/<seq>.txt`
(estrutura padrao do devkit de tracking do KITTI, so as imagens da camera
esquerda + rotulos - NAO precisa baixar velodyne/calibracao/camera direita
pra isso).

Nao baixa o dataset (exige cadastro gratuito em cvlibs.net) - so converte
o que ja esta no disco.
"""
import argparse
import os
import sys

NOME_CLASSE = 'person'  # so 1 classe - combina com classes: ["person"] do deteccao.yaml

# tipos do KITTI que viram "person"; Person_sitting e opcional (pose atipica,
# pode ajudar ou atrapalhar dependendo do quanto o robo real encontra gente
# sentada - fica como flag)
TIPO_PEDESTRE = {'Pedestrian'}
TIPO_PEDESTRE_SENTADO = {'Person_sitting'}

OCLUSAO_TOTALMENTE_OCULTO = 3  # codigo KITTI p/ "occluded" - sem pixel visivel


def _ler_rotulos_sequencia(caminho_label_txt):
    """Agrupa as linhas de um label_02/<seq>.txt por numero de frame."""
    por_frame = {}
    with open(caminho_label_txt) as f:
        for linha in f:
            campos = linha.split()
            if len(campos) < 17:
                continue  # linha incompleta/corrompida - pula, nao derruba o resto
            frame = int(campos[0])
            tipo = campos[2]
            ocluido = int(campos[4])
            esquerda, topo, direita, baixo = map(float, campos[6:10])
            por_frame.setdefault(frame, []).append(
                (tipo, ocluido, esquerda, topo, direita, baixo))
    return por_frame


def _bbox_para_linha_yolo_seg(esquerda, topo, direita, baixo, largura_img, altura_img):
    """
    Bbox em pixels -> 1 linha de rotulo YOLOv8-seg.

    Poligono = os 4 cantos da caixa, normalizados 0-1. Classe sempre 0
    (so existe "person" aqui).
    """
    pontos = [
        (esquerda, topo), (direita, topo), (direita, baixo), (esquerda, baixo),
    ]
    coords = []
    for x, y in pontos:
        coords.append(f'{max(0.0, min(1.0, x / largura_img)):.6f}')
        coords.append(f'{max(0.0, min(1.0, y / altura_img)):.6f}')
    return '0 ' + ' '.join(coords)


def converter(kitti_dir, saida_dir, val_sequencias, incluir_sentado):
    import cv2  # so pra ler altura/largura da imagem (tamanho do rotulo normalizado)

    dir_imagens = os.path.join(kitti_dir, 'image_02')
    dir_rotulos = os.path.join(kitti_dir, 'label_02')
    if not os.path.isdir(dir_imagens) or not os.path.isdir(dir_rotulos):
        sys.exit(
            f'Esperava encontrar "{dir_imagens}" e "{dir_rotulos}" - '
            'confira se --kitti_dir aponta pra pasta "training/" do KITTI tracking.')

    tipos_aceitos = set(TIPO_PEDESTRE)
    if incluir_sentado:
        tipos_aceitos |= TIPO_PEDESTRE_SENTADO

    sequencias = sorted(
        d for d in os.listdir(dir_imagens) if os.path.isdir(os.path.join(dir_imagens, d)))
    if not sequencias:
        sys.exit(f'Nenhuma sequencia encontrada em {dir_imagens}')

    n_imagens = {'train': 0, 'val': 0}
    n_pessoas = {'train': 0, 'val': 0}

    for split in ('train', 'val'):
        os.makedirs(os.path.join(saida_dir, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(saida_dir, 'labels', split), exist_ok=True)

    for seq in sequencias:
        split = 'val' if int(seq) in val_sequencias else 'train'
        caminho_label = os.path.join(dir_rotulos, f'{seq}.txt')
        if not os.path.exists(caminho_label):
            print(f'  aviso: sem label_02 pra sequencia {seq}, pulando')
            continue

        rotulos_por_frame = _ler_rotulos_sequencia(caminho_label)
        arquivos_frame = sorted(os.listdir(os.path.join(dir_imagens, seq)))

        for nome_arquivo in arquivos_frame:
            if not nome_arquivo.endswith('.png'):
                continue
            frame = int(os.path.splitext(nome_arquivo)[0])
            caminho_img = os.path.join(dir_imagens, seq, nome_arquivo)

            altura_img, largura_img = cv2.imread(caminho_img).shape[:2]

            linhas = []
            for tipo, ocluido, esq, topo, dir_, baixo in rotulos_por_frame.get(frame, []):
                if tipo not in tipos_aceitos:
                    continue
                if ocluido == OCLUSAO_TOTALMENTE_OCULTO:
                    continue  # sem pixel visivel - nao da pra aprender nada util
                linhas.append(
                    _bbox_para_linha_yolo_seg(esq, topo, dir_, baixo, largura_img, altura_img))

            nome_base = f'seq{seq}_{frame:06d}'
            caminho_link_img = os.path.join(saida_dir, 'images', split, nome_base + '.png')
            if not os.path.exists(caminho_link_img):
                os.symlink(os.path.abspath(caminho_img), caminho_link_img)

            caminho_rotulo = os.path.join(saida_dir, 'labels', split, nome_base + '.txt')
            with open(caminho_rotulo, 'w') as f:
                f.write('\n'.join(linhas))
                if linhas:
                    f.write('\n')

            n_imagens[split] += 1
            n_pessoas[split] += len(linhas)

    caminho_yaml = os.path.join(saida_dir, 'dataset.yaml')
    with open(caminho_yaml, 'w') as f:
        f.write(
            f'path: {os.path.abspath(saida_dir)}\n'
            f'train: images/train\n'
            f'val: images/val\n'
            f'names:\n  0: {NOME_CLASSE}\n'
        )

    print(f'Convertido em {saida_dir}')
    print(f'  train: {n_imagens["train"]} imagens, {n_pessoas["train"]} pessoas rotuladas')
    print(f'  val:   {n_imagens["val"]} imagens, {n_pessoas["val"]} pessoas rotuladas')
    print(f'  dataset.yaml escrito em {caminho_yaml}')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        '--kitti_dir', required=True,
        help='pasta "training/" do KITTI tracking (contem image_02/ e label_02/)')
    ap.add_argument('--saida', required=True, help='pasta de saida do dataset YOLO')
    ap.add_argument(
        '--val_sequencias', default='17,18,19,20',
        help='indices de sequencia (0-20) reservados pra validacao, separados por '
             'virgula - por SEQUENCIA inteira, nao por frame solto, pra nao vazar '
             'frames quase identicos entre treino e val')
    ap.add_argument(
        '--incluir_person_sitting', action='store_true',
        help='tambem conta "Person_sitting" do KITTI como pessoa')
    args = ap.parse_args()

    val_sequencias = {int(s) for s in args.val_sequencias.split(',') if s.strip() != ''}
    converter(args.kitti_dir, args.saida, val_sequencias, args.incluir_person_sitting)


if __name__ == '__main__':
    main()
