#!/usr/bin/env python3
"""
Fine-tuning do `yolov8n-seg` com o dataset convertido do KITTI.

Parte do modelo atual do `deteccao_node` e do dataset gerado por
`preparar_dataset_kitti.py`. Receita conservadora de proposito (nao e
treino do zero):
  - parte do checkpoint que ja esta em producao (`models/yolov8n-seg.pt`,
    pre-treinado no COCO) - nao de um modelo generico do ultralytics.
  - `--freeze` congela as camadas iniciais (backbone) por padrao - os
    rotulos do KITTI aqui sao poligonos RETANGULARES (ver docstring do
    conversor), entao treinar o modelo inteiro sem cuidado arriscaria
    piorar a qualidade de mascara que o COCO real ja ensinou.
  - poucas epocas e LR baixa por padrao - mesmo motivo.
  - maquina sem GPU (CPU-only confirmado) - `device=cpu` por padrao;
    `imgsz` menor e `batch` pequeno ajudam a manter cada epoca viavel.

Uso:
    python3 treinar_yolo_kitti.py --dataset /caminho/pra/dataset_kitti_pessoas/dataset.yaml

Ao final, copia o melhor checkpoint pra
`saye_tracking/models/yolov8n-seg-kitti-pessoas.pt` - pra usar, aponte
`config/deteccao.yaml`:
    modelo: yolov8n-seg-kitti-pessoas.pt
(mantem o `yolov8n-seg.pt` original intacto, pra comparar ou reverter facil)
"""
import argparse
import os
import shutil

from ultralytics import YOLO

MODELOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models')
MODELO_BASE_PADRAO = os.path.join(MODELOS_DIR, 'yolov8n-seg.pt')
MODELO_SAIDA_PADRAO = os.path.join(MODELOS_DIR, 'yolov8n-seg-kitti-pessoas.pt')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dataset', required=True, help='caminho do dataset.yaml gerado')
    ap.add_argument(
        '--modelo_base', default=MODELO_BASE_PADRAO,
        help='checkpoint de partida (padrao: o que ja esta em producao)')
    ap.add_argument(
        '--saida', default=MODELO_SAIDA_PADRAO,
        help='onde salvar o .pt final (padrao: models/yolov8n-seg-kitti-pessoas.pt)')
    ap.add_argument('--epocas', type=int, default=20)
    ap.add_argument('--imgsz', type=int, default=640)
    ap.add_argument('--batch', type=int, default=8)
    ap.add_argument(
        '--lr0', type=float, default=0.0005,
        help='taxa de aprendizado inicial - baixa de proposito '
             '(fine-tune, nao treino do zero)')
    ap.add_argument(
        '--freeze', type=int, default=10,
        help='numero de camadas iniciais congeladas (backbone); 0 = treina tudo')
    ap.add_argument('--device', default='cpu', help='"cpu", "cuda:0", etc.')
    ap.add_argument(
        '--projeto', default=os.path.expanduser('~/ackermann_sim/runs_yolo_kitti'),
        help='pasta onde o ultralytics salva os runs de treino')
    args = ap.parse_args()

    if not os.path.exists(args.modelo_base):
        raise SystemExit(f'modelo base nao encontrado: {args.modelo_base}')

    print(f'Partindo de: {args.modelo_base}')
    print(f'Dataset:     {args.dataset}')
    print(f'Epocas={args.epocas}  imgsz={args.imgsz}  batch={args.batch}  '
          f'lr0={args.lr0}  freeze={args.freeze}  device={args.device}')

    modelo = YOLO(args.modelo_base)
    resultado = modelo.train(
        data=args.dataset,
        epochs=args.epocas,
        imgsz=args.imgsz,
        batch=args.batch,
        lr0=args.lr0,
        freeze=args.freeze,
        device=args.device,
        project=args.projeto,
        name='kitti_pessoas',
        exist_ok=True,
        patience=max(5, args.epocas // 2),  # early stopping, nao trava em epocas inuteis
        verbose=True,
    )

    melhor = os.path.join(resultado.save_dir, 'weights', 'best.pt')
    if not os.path.exists(melhor):
        raise SystemExit(f'treino terminou mas nao achei {melhor} - confira o log acima')

    os.makedirs(os.path.dirname(args.saida), exist_ok=True)
    shutil.copy(melhor, args.saida)
    print(f'\nMelhor checkpoint copiado pra: {args.saida}')
    print('Pra usar, em config/deteccao.yaml:')
    print(f'    modelo: {os.path.basename(args.saida)}')


if __name__ == '__main__':
    main()
