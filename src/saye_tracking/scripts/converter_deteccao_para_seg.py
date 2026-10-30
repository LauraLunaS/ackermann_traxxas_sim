#!/usr/bin/env python3
"""
Converte um dataset YOLO de deteccao (caixas) num dataset YOLO-seg (poligonos).

Feito especificamente pro mirror do KITTI que o proprio ultralytics baixa
(https://docs.ultralytics.com/datasets/detect/kitti/, via
`kitti.yaml`/download automatico) - esse mirror ja vem pronto, dividido em
`images/{train,val}` + `labels/{train,val}`, mas com rotulo de CAIXA
(`classe cx cy w h`, 5 campos normalizados). Diferente do benchmark
oficial do KITTI (que `preparar_dataset_kitti.py` conversa com - sequencias
+ `label_02`), aqui nao ha estrutura de sequencia nem precisa ler o
tamanho da imagem: a caixa ja vem normalizada 0-1.

Por que precisa virar poligono: igual ao `preparar_dataset_kitti.py`, o
`deteccao_node` roda `yolov8n-seg` e `projecao3d_node` amostra profundidade
pela MASCARA, nao pela caixa - entao o fine-tuning continua precisando de
rotulo de segmentacao. Cada caixa vira um poligono retangular (os 4
cantos) - rotulo valido, mas nao e silhueta de verdade (mesma ressalva:
ver docstring de `preparar_dataset_kitti.py` sobre a receita conservadora
de treino).

Tambem filtra e renomeia classes - o dataset original do KITTI tem 8
classes (car, van, truck, pedestrian, Person_sitting, cyclist, tram,
misc); aqui so interessa pedestre, remapeado pra classe 0 "person" (igual
a `classes: ["person"]` do `config/deteccao.yaml`).

Uso:
    python3 converter_deteccao_para_seg.py \
        --origem /caminho/pra/kitti_extraido \
        --saida /caminho/pra/dataset_kitti_pessoas_seg \
        [--classes_manter 3,4] [--nome_classe person]

`--classes_manter` sao os IDs de classe do dataset de ORIGEM a manter (ver
o `names:` do `kitti.yaml` de origem) - padrao 3,4 = pedestrian +
Person_sitting do mirror do ultralytics.
"""
import argparse
import os


def _linha_caixa_para_poligono(campos):
    """Campos `cx cy w h` (normalizados) -> 4 cantos da caixa, mesma escala."""
    cx, cy, w, h = (float(c) for c in campos)
    esq, dir_ = cx - w / 2.0, cx + w / 2.0
    topo, baixo = cy - h / 2.0, cy + h / 2.0
    pontos = [(esq, topo), (dir_, topo), (dir_, baixo), (esq, baixo)]
    coords = []
    for x, y in pontos:
        coords.append(f'{max(0.0, min(1.0, x)):.6f}')
        coords.append(f'{max(0.0, min(1.0, y)):.6f}')
    return ' '.join(coords)


def converter(origem, saida, classes_manter, classe_saida, nome_classe):
    for split in ('train', 'val'):
        dir_imgs_origem = os.path.join(origem, 'images', split)
        dir_labels_origem = os.path.join(origem, 'labels', split)
        if not os.path.isdir(dir_imgs_origem):
            print(f'  aviso: "{dir_imgs_origem}" nao existe, pulando split "{split}"')
            continue

        dir_imgs_saida = os.path.join(saida, 'images', split)
        dir_labels_saida = os.path.join(saida, 'labels', split)
        os.makedirs(dir_imgs_saida, exist_ok=True)
        os.makedirs(dir_labels_saida, exist_ok=True)

        n_imgs, n_objetos = 0, 0
        for nome_label in sorted(os.listdir(dir_labels_origem)):
            if not nome_label.endswith('.txt'):
                continue
            base = os.path.splitext(nome_label)[0]

            nome_img = _achar_imagem(dir_imgs_origem, base)
            if nome_img is None:
                continue  # label sem imagem correspondente - pula

            linhas_saida = []
            with open(os.path.join(dir_labels_origem, nome_label)) as f:
                for linha in f:
                    campos = linha.split()
                    if len(campos) != 5:
                        continue
                    cls = int(campos[0])
                    if cls not in classes_manter:
                        continue
                    poligono = _linha_caixa_para_poligono(campos[1:])
                    linhas_saida.append(f'{classe_saida} {poligono}')

            caminho_link = os.path.join(dir_imgs_saida, nome_img)
            if not os.path.exists(caminho_link):
                os.symlink(
                    os.path.abspath(os.path.join(dir_imgs_origem, nome_img)), caminho_link)

            with open(os.path.join(dir_labels_saida, base + '.txt'), 'w') as f:
                f.write('\n'.join(linhas_saida))
                if linhas_saida:
                    f.write('\n')

            n_imgs += 1
            n_objetos += len(linhas_saida)

        print(f'  {split}: {n_imgs} imagens, {n_objetos} "{nome_classe}" rotulados')

    with open(os.path.join(saida, 'dataset.yaml'), 'w') as f:
        f.write(
            f'path: {os.path.abspath(saida)}\n'
            f'train: images/train\n'
            f'val: images/val\n'
            f'names:\n  0: {nome_classe}\n'
        )
    print(f'dataset.yaml escrito em {os.path.join(saida, "dataset.yaml")}')


def _achar_imagem(dir_imgs, base):
    for ext in ('.png', '.jpg', '.jpeg'):
        if os.path.exists(os.path.join(dir_imgs, base + ext)):
            return base + ext
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        '--origem', required=True,
        help='raiz do dataset de deteccao (contem images/{train,val} e labels/{train,val})')
    ap.add_argument('--saida', required=True, help='pasta de saida do dataset YOLO-seg')
    ap.add_argument(
        '--classes_manter', default='3,4',
        help='IDs de classe de origem a manter, separados por virgula '
             '(padrao 3,4 = pedestrian + Person_sitting do mirror do ultralytics)')
    ap.add_argument('--classe_saida', type=int, default=0, help='ID da classe na saida')
    ap.add_argument('--nome_classe', default='person')
    args = ap.parse_args()

    classes_manter = {int(c) for c in args.classes_manter.split(',') if c.strip() != ''}
    converter(args.origem, args.saida, classes_manter, args.classe_saida, args.nome_classe)


if __name__ == '__main__':
    main()
