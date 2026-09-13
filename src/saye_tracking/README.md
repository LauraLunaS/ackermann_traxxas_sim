# saye_tracking

Rastreamento de multiplos objetos (MOT) 3D para o rover Ackermann **"saye"**,
alimentando um costmap dinamico para o Nav2.

Abordagem escolhida: **tracking-by-detection, motion-only** (sem rede de ReID),
com filtro de Kalman e associacao operando em **3D no frame `odom`** (nao no
plano da imagem). Nucleo baseado nas ideias do **OC-SORT** (re-update
observation-centric + consistencia de direcao), adaptado para 3D. A associacao
em dois estagios do ByteTrack (deteccoes de alta/baixa confianca) pode ser
adicionada depois como melhoria aditiva se as deteccoes ficarem ruidosas.

## Roadmap

| Fase | Conteudo | Status |
|-----|----------|--------|
| 0 | Scaffold do pacote, contrato de mensagens | feito |
| 1 | `deteccao_node` — YOLOv8-seg → `Detection2DArray` + mascara de instancias | feito |
| 2 | `projecao3d_node` — le a nuvem organizada nos pixels da mascara, TF camera→odom (Caminho B) | em andamento |
| 3 | `tracker_node` — OC-SORT 3D (KF `[x,y,vx,vy]` em odom) | a fazer |
| 4 | Bancada de avaliacao — atores moveis no Gazebo + ground truth via `/model/<ator>/pose` | a fazer |
| 5 | Costmap dinamico (experimento isolado: `OccupancyGrid` / `MarkerArray`) | a fazer |
| 6 | Preditor de trajetoria melhor; associacao 2 estagios ByteTrack | a fazer |

### Fase 2 — submodulos

Abordagem "Caminho B": em vez de deprojetar a imagem de profundidade (precisa de
`camera_info` + correcao de eixo optico), le direto o ponto 3D ja calculado na
nuvem organizada `/camera/realsense/points` (indice do pixel = `v*width + u`),
que ja vem no frame de corpo `traxxas/base_link/realsense_d435`.

| Sub | Conteudo | Status |
|-----|----------|--------|
| 2.0 | Verificar pre-condicoes no sim (K, encoding do depth, cadeia de TF, convencao de eixo) | feito |
| 2.1 | Assinatura + sincronizacao (deteccoes + mascara + nuvem) por timestamp | feito (`test_2_1_sincronizacao.py`) |
| 2.2 | Extrair ponto 3D de cada deteccao (pixels da mascara → pontos da nuvem → mediana) | feito (`test_2_2_extracao_3d.py` + validado com frame real do rosbag) |
| 2.3 | Transformar a posicao para o frame `odom` (tf2) | feito (`test_2_3_transform_odom.py` + validado com o rosbag: erro 0mm vs. `/odom` em 6 instantes com o robo em movimento) |
| 2.4 | Publicar `Detection3DArray` + `MarkerArray` | feito (`test_2_4_publicacao.py` + validado ponta-a-ponta com o rosbag) |
| 2.5 | Validacao com erro vs. ground truth do Gazebo | a fazer |

**Achados do 2.0:** K = fx=fy=337.2, cx=320, cy=240, sem distorcao. Depth `32FC1`
em metros, sem-retorno = `+inf` (filtrar com `isfinite`). Cadeia de TF
`odom → traxxas → traxxas/base_link → .../realsense_d435` completa (o `/tf_static`
e latched, esperar ~1-2 s no boot). A nuvem `/camera/realsense/points` ja vem
organizada 640x480 no frame de corpo — Caminho B nao precisa de `_optical` nem de K.

**Limitacao de ambiente:** nesta maquina (2 GPUs, PRIME) a renderizacao de
sensores do Gazebo (camera, gpu_lidar) as vezes trava (`libEGL: failed to
create dri2 screen`) - nao e falta de driver (GPU RTX 5070, driver 570.211,
CUDA 12.8, tudo presente), e uma questao de qual GPU o processo do Gazebo usa
para renderizar. (A parte de o YOLO cair para CPU e outro problema, tambem de
versao: o torch instalado e compilado para CUDA 13.0, mas o driver so suporta
ate 12.8.) Testes que precisam de dados de camera ao vivo dependem de gravar
um rosbag quando os sensores funcionam, ou de rodar em outra maquina.

## Dependencias

`ultralytics` nao tem rosdep key — instale via pip (convencao do workspace):

```bash
pip install ultralytics --break-system-packages
```

O restante e resolvido por rosdep:

```bash
rosdep install --from-paths src/saye_tracking --ignore-src -r -y
```

## Build

```bash
cd ~/ackermann_sim
colcon build --packages-select saye_tracking
source install/setup.bash
```

## Fase 1 — no de deteccao

```bash
# Terminal 1: simulacao
ros2 launch saye_bringup traxxas_spawn.launch.py

# Terminal 2: deteccao
ros2 launch saye_tracking deteccao.launch.py
```

### Topicos

| Topico | Tipo | Conteudo |
|--------|------|----------|
| `/camera/realsense/image_raw` (entrada) | `sensor_msgs/Image` | RGB 640x480 da RealSense simulada |
| `/deteccao_node/deteccoes` | `vision_msgs/Detection2DArray` | bbox + classe + score |
| `/deteccao_node/mascaras` | `sensor_msgs/Image` (`mono8`) | mascara de instancias |
| `/deteccao_node/debug_image` | `sensor_msgs/Image` (`bgr8`) | overlay para inspecao |

**Contrato da mascara de instancias:** o pixel de valor `i + 1` corresponde a
`deteccoes.detections[i]`; `0` e fundo. As tres saidas compartilham o mesmo
`header` (stamp + `frame_id`) da imagem de entrada.

### Verificar

```bash
# ver deteccoes
ros2 topic echo /deteccao_node/deteccoes --once

# ver o overlay
ros2 run rqt_image_view rqt_image_view /deteccao_node/debug_image
```

Para ter algo para detectar, adicione um ator/pedestre ao mundo do Gazebo
(`saye_description/worlds/simple_world.sdf`) — feito na Fase 4.

### Parametros (`config/deteccao.yaml`)

| Parametro | Padrao | Nota |
|-----------|--------|------|
| `modelo` | `yolov8n-seg.pt` | baixado no 1o uso; use `yolov8s-seg.pt` se tiver GPU |
| `topico_imagem` | `/camera/realsense/image_raw` | |
| `confianca_min` | `0.4` | threshold baixo demais → mais ruido para o tracker |
| `imgsz` | `640` | |
| `device` | `""` | `""` = auto, `cpu`, `cuda:0` |
| `classes` | `["person"]` | nomes COCO; adicionar `car`, `bicycle`, etc. depois |
| `publicar_debug` | `true` | overlay so e gerado se houver assinante |

## Fase 2 — projecao 3D

```bash
# Terminal 1: simulacao
ros2 launch saye_bringup traxxas_spawn.launch.py

# Terminal 2: deteccao
ros2 launch saye_tracking deteccao.launch.py

# Terminal 3: projecao 3D
ros2 launch saye_tracking projecao3d.launch.py
```

### Topicos

| Topico | Tipo | Conteudo |
|--------|------|----------|
| `/camera/realsense/points` (entrada) | `sensor_msgs/PointCloud2` | nuvem organizada da RealSense simulada, ja no frame de corpo |
| `/projecao3d_node/deteccoes_3d` | `vision_msgs/Detection3DArray` | posicao + classe + score, no frame `odom` |
| `/projecao3d_node/marcadores` | `visualization_msgs/MarkerArray` | bolinha + texto por deteccao, para o RViz |

### Verificar

```bash
ros2 topic echo /projecao3d_node/deteccoes_3d --once
# no RViz: Fixed Frame = odom, adicionar um display MarkerArray no topico
# /projecao3d_node/marcadores
```

Assim como na Fase 1, precisa de algo pra detectar na cena — sem ator/pedestre
no mundo, `deteccoes_3d` sai vazio (o pipeline roda, so nao ha o que projetar).

### Parametros (`projecao3d_node`)

| Parametro | Padrao | Nota |
|-----------|--------|------|
| `topico_deteccoes` | `/deteccao_node/deteccoes` | |
| `topico_mascaras` | `/deteccao_node/mascaras` | |
| `topico_nuvem` | `/camera/realsense/points` | |
| `frame_alvo` | `odom` | referencial de saida das posicoes |
| `sync_slop` | `0.08` (s) | folga do sincronizador entre as 3 entradas |
| `min_pixels_mascara` | `20` | rejeita deteccao com mascara pequena demais |
| `min_pixels_validos` | `10` | rejeita deteccao sem retorno de profundidade suficiente |
| `tf_timeout` | `0.2` (s) | espera pelo TF antes de desistir do instante |
