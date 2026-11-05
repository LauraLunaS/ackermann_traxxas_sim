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
| 2 | `projecao3d_node` — le a nuvem organizada nos pixels da mascara, TF camera→odom (Caminho B) | feito |
| 3 | `tracker_node` — OC-SORT 3D (KF `[x,y,vx,vy]` em odom) | feito |
| 4 | Bancada de avaliacao — deteccao real + ground truth + metricas motmetrics + suite de cenarios | feito |
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
| 2.5 | Validacao com erro vs. ground truth do Gazebo | feito (`test_2_5_vies_superficie.py` + validado com o rosbag contra os 3 obstaculos do `simple_world.sdf`) |

**Resultado do 2.5 (medido com o rosbag):** usando os 3 obstaculos ja
presentes no mundo (`dynamic_obstacle_sphere/box/cylinder`, posicao real via
`/world/.../dynamic_pose/info`) como alvos de posicao conhecida, o pipeline
completo (2.1→2.4) errou em media **7.6 cm** (mediana 7.7 cm, maximo 12.3 cm)
em 6 amostras entre 2.5 e 5.8 m de distancia - apos corrigir pelo raio do
objeto (ver abaixo). Sem correcao o "erro" seria de ~30-40 cm, mas isso nao e
bug: e o fato de a nuvem so enxergar a face voltada pra camera, entao a
mediana da deteccao fica perto da **superficie visivel**, nao do centro
geometrico do objeto (`test_2_5_vies_superficie.py` formaliza e mede esse
vies com dado sintetico). Isso e esperado e relevante pra Fase 3/4: o
rastreador segue o centroide da superficie visivel de uma pessoa, nao o
centro de massa dela.

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

### Fase 3 — submodulos

| Sub | Conteudo | Status |
|-----|----------|--------|
| 3.0 | Decisao de contrato de saida + scaffold do `tracker_node` (assina `Detection3DArray`, so loga) | feito (`test_3_0_scaffold.py`) |
| 3.1 | Filtro de Kalman de 1 track (`predict`/`update`, estado `[x,y,vx,vy]`), puro numpy, sem ROS | feito (`kalman.py` + `test_3_1_kalman.py`) |
| 3.2 | Ciclo de vida do track (tentativo/confirmado/perdido/apagado, por tempo) | feito (`track.py` + `test_3_2_ciclo_de_vida.py`) |
| 3.3 | Associacao: matriz de custo + gate + Hungaro | feito (`associacao.py` + `test_3_3_associacao.py`) |
| 3.4 | OCM - termo de consistencia de direcao na associacao | feito (`ocm.py` + `Track.direcao_momentum` + `test_3_4_ocm.py`) |
| 3.5 | OCR + ORU - recuperacao de track perdido + re-atualizacao pela trajetoria virtual | feito (`recuperacao.py` + `test_3_5_recuperacao.py`) |
| 3.6 | Laco do rastreador (predict→associate→recover→update→manage) juntando 3.1-3.5 | feito (`rastreador.py` + `test_3_6_rastreador.py`) |
| 3.7 | Integracao no no ROS + publicacao (`Detection3DArray` + `MarkerArray` com setas) | feito (`tracker_node.py` + `test_3_7_integracao.py`) |
| 3.8 | Validacao com os obstaculos do 2.5 em movimento (ID estavel) | feito - validado com rosbag real |

**Resultado do 3.8:** alimentando o `Rastreador3D` com a posicao real (ground
truth) dos 3 obstaculos de `simple_world.sdf` se movendo AO MESMO TEMPO
(~19s, quase 60Hz, exercitando associacao/OCM de verdade com 3 alvos
simultaneos), cada objeto manteve **um unico ID do inicio ao fim, sem
nenhuma troca** - inclusive num teste bem mais exigente do que planejado
(ver abaixo). A comparacao de velocidade estimada vs. a velocidade nominal
do SDF nao foi conclusiva - motivo documentado abaixo, e nao e uma falha
do rastreador.

**Achado no caminho:** os 3 obstaculos tinham `<waypoints>`/`<velocity>`
configurados mas NUNCA se moviam - faltava `<link_name>` no plugin
`gz-sim-trajectory-follower-system` de cada um (corrigido, ver commit
`fix(saye_description)`). Depois do fix eles passaram a se mover, mas de
forma nao-limpa (a esfera acelerou sem limite ao longo da gravacao,
chegando a >400m da origem; o cilindro por vezes ainda nao se moveu) -
parece um problema mais profundo do plugin nesta versao do Gazebo, fora do
escopo deste submodulo. Por isso a velocidade nominal do SDF (0.8/0.6/0.5
m/s) nao serve de gabarito confiavel ainda - mas o ponto forte do 3.8, a
estabilidade de ID, na real ficou mais bem testado: a esfera se movendo
de forma rapida e erratica e um teste mais duro pro rastreador do que um
objeto comportado a velocidade constante, e mesmo assim o ID nao trocou.
Fica registrado para quem for montar a Fase 4 (bancada de avaliacao com
atores moveis) investigar o comportamento do TrajectoryFollower antes de
usa-lo pra medir precisao de velocidade.

**Decisao registrada no 3.0 (Opcao B):** sem mensagem customizada por
enquanto. `saye_tracking` e `ament_python` e nao gera mensagens - isso
exigiria um pacote `ament_cmake` irmao (como o `saye_msgs` do outro repo).
A velocidade sai so visualmente (seta no `MarkerArray`) ate a Fase 5
(costmap dinamico) precisar consumir o numero de verdade, nao so exibi-lo.

### Fase 4 — submodulos

| Sub | Conteudo | Status |
|-----|----------|--------|
| 4.0 | Pessoa detectavel no mundo (Gazebo Fuel, no lugar de `<actor>` - ver achado abaixo) | feito |
| 4.1 | `gravador_node` — grava hipoteses do tracker + verdade do Gazebo em CSV | feito (`test_4_1_gravador.py` + validado ao vivo) |
| 4.2 | Comparador com `motmetrics` (MOTA, trocas de ID, FP/FN) | feito (`test_4_2_comparador.py` + validado ao vivo) |
| 4.3 | Suite de cenarios (parado, linear, curva, entra/sai do FOV, oclusao) | feito (`test_4_3_cenarios.py` + validado ao vivo) |
| 4.4 | Rodar a suite e gerar relatorio | feito (`test_4_4_relatorio.py` + validado ao vivo, suite inteira) |
| 4.5 | Pessoa detectavel ANDANDO de verdade (alvo com movimento proprio, nao so a camera se movendo) | feito (`test_4_5_caminhada.py` + validado ao vivo) |
| 4.6 | Multiplas pessoas, visualmente diferentes, com CICLO DE CAMINHADA real (pernas se movendo) | feito (validado ao vivo) |
| 4.7 | Supressao de duplicata no rastreador - corrige ids fantasmas perto de cruzamentos (ver achado abaixo) | feito (`test_4_7_supressao_duplicata.py`) |
| 4.8 | Gate adaptativo + OCM na recuperacao (OCR) - corrige troca de id entre pessoas DIFERENTES (ver achado abaixo) | feito (`test_4_8_gate_adaptativo_recuperacao.py`); limitacao residual conhecida em cruzamento geometrico real |

**Achado do 4.0:** o sistema de `<actor>` do Gazebo (mesh animado tipo
Collada) carrega normalmente e aparece na GUI, mas **nao renderiza pra
camera de sensor** nesta maquina (testado isolado, com controle: uma caixa
na mesma pose renderiza perfeita, o ator na mesma pose fica com o frame em
branco). Resolvido trocando por um `<model>` estatico do Gazebo Fuel
("Standing person", OpenRobotics/MakeHuman, com textura real) - este
renderiza normalmente e o YOLOv8 detecta como "person" (0.93 de confianca
isolado, 0.45 pelo pipeline real de producao - a diferenca e porque um dos
obstaculos dinamicos passou na frente da pessoa bem na hora da captura,
oclusao parcial por coincidencia, nao um bug). Modelo incluido em
`simple_world.sdf` como `pessoa_detectavel`, parado em `(2.0, 1.0)`, de
frente pro spawn do robo.

**Achado do 4.1 (importante pro 4.2 tambem):**
1. Comparado ao vivo: `/odom` do robo e IDENTICO a pose dele no `world` do
   Gazebo (mesmos valores, sem casas decimais de diferenca) - spawn em
   yaw=0, entao o frame `odom` deste projeto E o frame `world`, sem
   deslocamento nem rotacao. Isso permite comparar a saida do tracker (que
   sai em `odom`) direto com a verdade do Gazebo (que sai em `world`), sem
   nenhuma conta de transformacao.
2. A ponte `ros_gz_bridge` de `gz.msgs.Pose_V` para `tf2_msgs/TFMessage`
   **nao preenche nome nem timestamp de cada transform** (ambos ficam
   vazios/zero) - so a ORDEM e a posicao vem certas. Por isso a verdade e
   identificada por indice (posicao na lista, ver docstring do
   `gravador_node.py`), nao por nome, e o tempo de cada leitura usa o
   relogio do proprio no (`use_sim_time`) em vez do timestamp da mensagem.
   Essa mesma limitacao ja tinha aparecido no 2.5/3.8 (usaram "ordem fixa"
   pelo mesmo motivo) - agora esta documentada de vez.
3. Validado ao vivo com o pipeline completo rodando (sim + deteccao +
   projecao3d + tracker + gravador, ~12s): `hipoteses.csv` e `verdade.csv`
   saem com posicoes coerentes (verdade constante em `(2.0, 1.0)` pra pessoa
   parada; hipotese do track que segue ela fica bem proxima disso).

**Achado importante (revisado no 4.2 - corrige o que o 4.1 tinha registrado
como "cosmetico"):** o `header.stamp` que sai do `deteccao_node` (propagado
de `/camera/realsense/image_raw`) alterna entre tempo de sim correto e
timestamp de RELOGIO DE PAREDE (epoch Unix) - e nao e raro: em gravacoes
reais, a MAIORIA das mensagens (~90%) saiu com o timestamp errado, nao so
as primeiras. Confirmado que nao e processo duplicado (refeito do zero com
verificacao rigorosa de 1 unica instancia de cada no em cada etapa, mesmo
resultado). E um bug de verdade na ponte `ros_gz_bridge`/sensor de camera
do Gazebo nesta maquina - mesma familia da flakiness de renderizacao ja
documentada (`libEGL: failed to create dri2 screen`, ver
[[env-gpu-sim]]) - fora do escopo do `saye_tracking` consertar. Efeito
pratico: o `comparador` (4.2) tem que descartar essas leituras contaminadas
por um TETO ABSOLUTO de tempo (nao por desvio da mediana - com 90% de
contaminacao a mediana vira relogio de parede e um filtro relativo
descartaria as leituras BOAS por engano). Quem for investigar essa ponte
de verdade: comecar comparando o timestamp que a Gazebo bota no sensor de
camera com o que chega no lado ROS, sensor a sensor.

**Resultado do 4.2:** `comparador.py` (sem ROS, so `motmetrics` + os CSVs
do 4.1) agrupa hipotese/verdade em frames de largura fixa (`round()`, nao
`int()` - truncar quebra por erro de ponto flutuante, ex.: `0.3/0.1 ==
2.9999999999999996`), mapeia nome->numero pra verdade (`motmetrics` exige
id numerico, nao aceita string), e descarta timestamps de relogio de
parede por teto absoluto antes de comparar. 7 testes sinteticos (match
perfeito, falso negativo, falso positivo, gate de distancia, troca de ID,
outlier isolado, maioria contaminada) + validado ao vivo 2x (pipeline
completo rodando de verdade, com verificacao de instancia unica de cada
no): primeira rodada deu metricas absurdas (MOTA -3.08) por causa do
achado de timestamp acima (a maioria das linhas sendo descartada por
engano por um filtro relativo a mediana testado inicialmente); com o filtro
corrigido pra teto absoluto, a segunda rodada deu MOTA=0.29, motp=0.0099
(~10cm de erro medio nos matches - boa precisao posicional), 18 trocas de
ID e 2 tracks extras poluindo a cena.

**Correcao importante (feita no 4.3): os "2 tracks fantasmas" NAO eram
YOLO confundindo outros objetos com pessoa** - essa hipotese, registrada
aqui originalmente, estava errada. A causa real: um script de teste do
scratchpad (`adaptador_gt_para_deteccoes.py`, criado la na validacao do
3.8 pra alimentar o rastreador com ground truth em vez de deteccao real)
tinha ficado **rodando havia muitas sessoes**, publicando silenciosamente
na mesma `/projecao3d_node/deteccoes_3d` que o no de verdade. Descoberto
no 4.3 com `ros2 topic info <topico> -v`, que mostrou 2 publishers no
mesmo topico - a checagem de "so 1 instancia" feita ate entao so conferia
processos pelo NOME do executavel esperado (`deteccao_node`,
`tracker_node`, etc.), que nunca pegaria um script solto com outro nome.
Depois de matar esse processo, o mesmo cenario saiu limpo (1 so track,
zero falso positivo, zero troca de ID) - ver resultado do 4.3 abaixo.
CLI pronta pra uso manual: `ros2 run saye_tracking comparador <diretorio>`.

**Licao de processo (registrada tambem em memoria):** verificar "so 1
instancia" por nome de processo NAO E SUFICIENTE - um script solto do
scratchpad com outro nome passa batido. A forma confiavel e perguntar ao
proprio ROS: `ros2 topic info <topico> -v` mostra TODOS os publishers
reais de um topico, non-negociavel antes de confiar em qualquer gravacao.

`cenarios.py` (sem ROS) define roteiros de `/cmd_vel` (`vx, wz, duracao`)
pra cada cenario - como so existe uma pessoa DETECTAVEL e ela e ESTATICA
(4.0), os cenarios de movimento sao feitos movendo o ROBO (a camera), nao
a pessoa; do ponto de vista do rastreamento relativo camera-alvo da no
mesmo. `executar_cenario_node.py` liga isso ao `/cmd_vel` de verdade, via
contagem de ticks do timer (nao subtracao de `Time` absoluto - o mesmo
problema do `self.get_clock().now()` vindo zerado no `__init__`, antes do
1o `/clock` chegar, fazia o cenario "terminar" na primeira chamada do
timer, ~1.7s depois de iniciado em vez de 8s; achado e corrigido ao vivo).
6 testes sinteticos (roteiros bem formados, duracao total, comando por
instante nas fronteiras dos segmentos).

**Resultado do 4.3 (com o publisher fantasma do 4.1/4.2 devidamente morto):**
- `parado` (10s, baseline): MOTA=0.82, motp=0.032 (~18cm), 0 trocas de ID,
  0 falsos positivos, 27/147 frames sem deteccao (~18% de "buraco" mesmo
  com camera e alvo parados - falta investigar se e confianca do YOLO
  oscilando perto do limiar ou instabilidade da mascara/profundidade).
- `linear` (8s, robo avança 0.4m/s em direcao a pessoa e passa por ela):
  MOTA=0.11, motp=0.037, 0 trocas de ID, 0 falsos positivos, mas 115/129
  frames sem deteccao - o rastreador perde a pessoa na maior parte do
  percurso (plausivel: de perto/no angulo errado a mascara de segmentacao
  piora, e depois que o robo passa a pessoa sai do campo de visao). ID
  nunca trocou nas duas rodadas - a garantia mais importante do
  rastreador (nao confundir alvos) se sustenta mesmo quando a deteccao
  falha bastante.
- `curva` e `entra_sai_fov`: roteiros prontos e testados (unitario +
  `executar_cenario_node` rodando via `ros2 launch saye_tracking
  cenario.launch.py cenario:=<nome>`), mas ainda NAO validados ao vivo
  (fica pro 4.4, que roda a suite inteira e agrega os resultados).
- `oclusao_obstaculo`: roteiro existe mas e MELHOR ESFORCO - depende dos
  obstaculos dinamicos do mundo cruzarem a linha de visao por conta
  propria (patrulha sozinha, ja documentada como nao-limpa desde o 3.8),
  nao e determinístico. Cruzamento (2 alvos se cruzando) foi DEIXADO DE
  FORA - exigiria uma segunda pessoa movel, que esbarra no mesmo problema
  do `TrajectoryFollower` ja aceito como limitacao desde o 3.8.

### Rodando um cenario manualmente

```bash
# Terminal 1: simulacao (+ ponte de ground truth, ver 4.1)
ros2 launch saye_bringup traxxas_spawn.launch.py
ros2 run ros_gz_bridge parameter_bridge \
  '/world/beach_world/pose/info@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V' \
  --ros-args -r /world/beach_world/pose/info:=/gt/pose_info

# Terminal 2-4: pipeline
ros2 launch saye_tracking deteccao.launch.py
ros2 launch saye_tracking projecao3d.launch.py
ros2 launch saye_tracking tracker.launch.py

# Terminal 5: gravador (comeca a gravar)
ros2 launch saye_tracking gravador.launch.py diretorio_saida:=/tmp/cenario_X

# Terminal 6: roda o cenario (encerra sozinho quando acabar)
ros2 launch saye_tracking cenario.launch.py cenario:=linear

# depois do cenario acabar: salva e calcula metricas
ros2 service call /gravador_node/salvar std_srvs/srv/Trigger "{}"
ros2 run saye_tracking comparador /tmp/cenario_X
```

Cenarios disponiveis (`saye_tracking/cenarios.py`: `CENARIOS`): `parado`,
`linear`, `curva`, `entra_sai_fov`, `oclusao_obstaculo`.

### 4.4 — roda a suite inteira e gera o relatorio

`relatorio.py` (sem ROS) formata os resumos do `comparador` numa tabela
Markdown - testavel com dados sinteticos. `rodar_suite.py` automatiza o
que o 4.3 fazia manualmente: para cada cenario, reseta a pose do robo
(`/world/<mundo>/set_pose` via `gz service` - sem isso cenarios em
sequencia comecariam de onde o anterior parou), sobe um `gravador_node`
num diretorio proprio, roda o cenario, salva, calcula metricas, e no final
imprime a tabela com todos.

```bash
# com a simulacao + pipeline + ponte de ground truth ja rodando
# (ver "Rodando um cenario manualmente" acima)
ros2 run saye_tracking rodar_suite --diretorio-base /tmp/minha_suite
# ou so alguns cenarios:
ros2 run saye_tracking rodar_suite --cenarios parado linear
```

**Achado ao automatizar:** `Popen.terminate()` (SIGTERM) no processo do
`ros2 launch` do gravador NAO derruba o `gravador_node` filho - numa
primeira tentativa, 4 instancias ficaram orfas rodando ao mesmo tempo
(todas assinando os mesmos topicos), e o 4o cenario da suite falhou por
causa disso (o servico `~/salvar` foi atendido por uma instancia errada).
Trocado para `send_signal(SIGINT)` - o mesmo que Ctrl+C no terminal, que
`ros2 launch` trata corretamente pra cascatear o desligamento pros filhos.
`rodar_suite.py` tambem confere que os dois CSVs existem antes de seguir
pro proximo cenario, em vez de so confiar que o servico respondeu OK.

**Resultado da suite completa** (pipeline verificado limpo via `ros2 topic
info -v` antes de rodar, pose do robo resetada entre cada cenario):

| cenario | frames | MOTA | MOTP | trocas ID | falsos positivos | perdas | acertos |
|---|---|---|---|---|---|---|---|
| parado | 156 | 0.910 | 0.031 | 0 | 0 | 14 | 142 |
| linear | 131 | 0.305 | 0.033 | 0 | 0 | 91 | 40 |
| curva | 144 | 0.317 | 0.033 | 0 | 2 | 95 | 47 |
| entra_sai_fov | 116 | 0.793 | 0.032 | 0 | 0 | 24 | 92 |
| oclusao_obstaculo | 209 | 0.938 | 0.031 | 0 | 0 | 13 | 196 |

**Leitura dos resultados:**
- **Zero trocas de ID em TODOS os 5 cenarios** - a garantia mais importante
  do rastreador (nunca confundir alvos) se sustenta mesmo sob rotacao da
  camera (`curva`), entrada/saida do campo de visao (`entra_sai_fov`) e
  grande perda de deteccao (`linear`).
- MOTP (erro de posicao nos acertos) e estavel entre ~3.1-3.3cm em todos
  os cenarios - a precisao posicional nao degrada com o movimento.
- MOTA varia muito mais que MOTP: `parado` e `oclusao_obstaculo` (que, na
  pratica, teve pouca ou nenhuma oclusao real - ver nota de "melhor
  esforco" no 4.3) ficam acima de 0.9; `linear` e `curva` ficam abaixo de
  0.32, dominados por PERDAS de deteccao (nao falsos positivos nem trocas
  de ID). Ou seja: o gargalo atual nao e o RASTREADOR, e a DETECCAO -
  especificamente, manter a pessoa detectada de perto e em angulos
  variados. Candidatos a investigar depois (fora do escopo do
  `saye_tracking` em si): `confianca_min` do YOLO (0.4 pode estar cortando
  deteccoes validas em angulos ruins), ou o proprio modelo (`yolov8n-seg`
  e o menor da familia).
- `entra_sai_fov` com MOTA alto (0.79) apesar de ter perdas por design
  (a pessoa sai do quadro de proposito) sugere que a deteccao e boa
  QUANDO a pessoa esta de frente/perto do centro da imagem - reforca que
  o problema do `linear`/`curva` e mais sobre angulo/distancia do que
  sobre o pipeline de deteccao estar quebrado.

**Nota de ruido (nao-bloqueante):** ao receber o SIGINT, o `gravador_node`
as vezes loga um traceback (`RuntimeError: Unable to convert call
argument...`) numa corrida entre o shutdown do rclpy e uma mensagem
chegando - mas em todos os casos observados os CSVs ja tinham sido salvos
ANTES do traceback aparecer, entao nao perde dado; e um comportamento
conhecido do rclpy/pybind11 no shutdown, nao um bug do `saye_tracking`.

Isso fecha a Fase 4 (bancada de avaliacao MOT) completa: deteccao real
(YOLO, nao ground truth), gravacao, metricas via `motmetrics`, e suite de
cenarios automatizada com relatorio.

### 4.5 — pessoa andando de verdade (alvo com movimento proprio)

Limitacao percebida apos o 4.4: em todos os 5 cenarios, quem se movia era
o ROBO (a camera) - a pessoa (`pessoa_detectavel`) ficava sempre parada em
`(2.0, 1.0)`. Isso nunca testou o rastreador contra um alvo que anda
sozinho, detectado de verdade pelo YOLO (so o 3.8, na Fase 3, testou alvo
em movimento - 3 obstaculos, mas via ground truth, nao deteccao real).

**Tentativa descartada - fisica de verdade (`TrajectoryFollower`):**
primeira ideia foi mover a pessoa com o mesmo plugin de forca/torque ja
usado pelos 3 obstaculos dinamicos (fase 3.8). Diferente deles (esfera,
caixa, cilindro - baixos e simetricos), a pessoa e um corpo ALTO com
centro de massa perto de 1m do chao: empurrado por forca/torque bruto
sem nenhum amortecimento, ela **tomba** (confirmado pelo quaternion
resultante - rotacao de ~180° em torno de um eixo horizontal, deitada no
chao). Tentado:
- Remover a colisao da malha do corpo (deixar so uma caixa "pes" como
  colisao fisica, igual aos obstaculos) - ainda tombava, só mais devagar.
- Aumentar a base de apoio (0.5x0.35 -> 1.0x1.0) e a inercia rotacional
  em x/y ate 20x o valor real (pra resistir mais a tombar) - piorou:
  deslizamentos erraticos (posicao chegou a `x=16` fora do caminho
  pretendido de `x=2`).
- Varias combinacoes de forca/torque (40 ate 5000) - ou ficava
  praticamente parada (forca fraca demais pra vencer o atrito), ou
  tombava rapido (forca forte demais), sem um meio-termo confiavel.

Virou um problema de MODELAGEM FISICA (precisaria de uma junta
restringindo a rotacao a só o eixo de guinada - tipo um "carrinho" por
baixo do corpo visual), nao so de ajuste de parametro. Abandonado.

**Solucao adotada - teleporte cinematico (sem fisica nenhuma):**
`caminhada.py` (sem ROS) calcula a posicao de um vai-e-vem entre dois
pontos a velocidade constante, em funcao do tempo - puro calculo,
testavel sem Gazebo. `mover_pessoa_node.py` liga isso ao Gazebo chamando
o servico `/world/<mundo>/set_pose` (o MESMO servico ja usado pra
resetar a pose do robo na Fase 4.4) direto via `gz-transport` em Python
(`gz.transport13`/`gz.msgs10`, ja disponiveis no ambiente - sem
subprocess, sem overhead), num timer a 10Hz. Como e teleporte puro (nao
fisica), **nao ha como tombar, nao ha friccao, nao ha overshoot** - o
movimento sai perfeitamente limpo e prederminado.

```bash
ros2 launch saye_tracking mover_pessoa.launch.py
# ou com outra velocidade:
ros2 launch saye_tracking mover_pessoa.launch.py velocidade:=0.5
```

**Resultado validado ao vivo:** com o pipeline completo rodando (sim +
deteccao + projecao3d + tracker, instancia unica confirmada via `ros2
topic info -v`), a pessoa andou um ciclo inteiro vai-e-vem (incluindo as
DUAS viradas de direcao) em ~13s. YOLO manteve deteccao consistente o
tempo todo (359 deteccoes em 18s, confianca ~0.88-0.92, bem mais estavel
que o teste parado isolado do 4.0). O rastreador manteve **um unico ID do
inicio ao fim**, inclusive atravessando as duas reversoes de direcao -
primeiro teste real de alvo com movimento proprio, detectado de verdade,
sem trocar de identidade.

### 4.6 — multiplas pessoas, diferentes, com pernas se movendo de verdade

Pedido explicito do usuario: 1) multiplos pedestres ao mesmo tempo
(objetivo do projeto - rastreamento + simulacao dinamica), 2) aparencia
DIFERENTE entre eles (uma mesma pessoa 3x nao valida a associacao
visualmente), 3) **caminhada de verdade** (pernas alternando), nao so a
pose 4.5 deslizando.

**Tentativa 1 - usar o repositorio sugerido
(`gazebo-ros-actor-plugin`):** investigado a fundo (nao so descartado de
cara). O plugin controla bem o MOVIMENTO de um `<actor>` (velocidade ou
caminho), mas isso nunca foi o problema - o problema e RENDERIZACAO.
Testado com o skin exato do repositorio (`DoctorFemaleWalk`):
- Numa camera `camera` (RGB simples) de perto (1.5m), invisivel - mesmo
  resultado da Fase 4.0.
- Numa camera `camera` mais longe (3m+), o ator RENDERIZA normalmente -
  ou seja, nao e "nunca renderiza".
- Mas em `rgbd_camera` **e** `depth_camera` (os dois tipos que geram
  profundidade - o que o robo real usa), o ator **nunca** aparece, em
  nenhuma distancia testada - confirmado olhando o mapa de profundidade
  bruto (so o chao e objetos comuns aparecem, nenhum pixel do ator).

Consequencia pro projeto: mesmo que o YOLO detectasse o ator na imagem
RGB, o `projecao3d_node` nunca acharia profundidade valida pra ele - a
deteccao cairia sempre no filtro de `pixels_validos`. Atores continuam
descartados - nao e so "nao aparece bonito", e um problema que quebra a
extracao 3D de qualquer jeito.

**Solucao - extrair o ciclo de caminhada real e "tocar" como flipbook de
malhas estaticas:** como atores tem o MOVIMENTO certo (esqueleto
articulado) mas nao SAO VISIVEIS pro robo, e modelos estaticos SAO
visiveis mas nao tem movimento de pernas - a solucao foi tirar o melhor
dos dois: extrair N poses REAIS do ciclo de caminhada de um `.dae` com
esqueleto (via skinning manual, nao um exportador pronto - nenhuma
ferramenta disponivel no ambiente importava COLLADA com esqueleto direito;
`pycollada` fez o parsing, o algoritmo de linear blend skinning foi
implementado na mao em `scripts/bake_walk_frames.py`) e "tocar" essas N
malhas estaticas em sequencia, trocando qual fica visivel com base na
DISTANCIA percorrida - um flipbook 3D.

```bash
pip install pycollada --break-system-packages  # so pro script de bake, nao e dependencia do pacote

scripts/bake_walk_frames.py entrada.dae textura.png saida_dir/ n_quadros
scripts/empacotar_quadros.py saida_dir/ textura.png nome_pessoa n_quadros
```
O primeiro extrai os quadros (skinning manual: hierarquia de juntas do
`<visual_scene>`, matrizes de bind/animacao de `<source>`/`<sampler>`/
`<channel>`, aplica LBS e exporta cada pose como `.obj`); o segundo
empacota cada quadro como um modelo Gazebo (`model.config` + `model.sdf`)
dentro de `saye_description/models/`.

`mover_pessoas_node.py` (novo, ao lado do `mover_pessoa_node.py` da 4.5;
substituiu o `mover_pessoa_animada_node.py` original desta fase - ver
achado 4 da bancada 4.9, secao abaixo) gerencia os N modelos-quadro de
QUALQUER quantidade de pessoas num SO processo: a cada tick, calcula a
posicao (igual a 4.5) e o INDICE DO QUADRO ativo de cada uma
(`caminhada.indice_quadro`, baseado em distancia percorrida / comprimento
de passada), e teleporta todos os quadros ativos + os quadros que
acabaram de deixar de ser ativos (pra `z=-50`, fora de qualquer camera)
numa UNICA chamada em lote (`gz_pose_vector.TeleportadorEmLote`).

```bash
ros2 launch saye_tracking mover_pessoas_animadas.launch.py
```

**Achado tecnico no caminho:** o primeiro bake pareceu quebrado (malha
toda deformada/colapsada) - mas era bug no PREVIEW (o importador de `.obj`
do Blender aplica conversao Y-up->Z-up por padrao, destruindo a pose só na
visualizacao); os dados exportados sempre estiveram corretos (confirmado
comparando a caixa delimitadora calculada em Python puro antes de
qualquer import). Validado de verdade so depois de desligar essa conversao
no import. A textura (PNG via MTL) nao carregou dentro do Gazebo (malha
sai branca) - aceito como limitacao conhecida, ja que a forma/silhueta
(cabelo, roupa, corpo) ja basta pra distinguir as pessoas visualmente e
nao atrapalha a deteccao do YOLO.

**Resultado validado ao vivo:** pipeline completo (sim + deteccao +
projecao3d + tracker, publishers verificados via `ros2 topic info -v`), 3
pessoas com aparencias diferentes (DoctorFemaleWalk, MaleVisitorWalk,
Scrubs) andando ao mesmo tempo, 2 delas com o flipbook de 6 quadros - as
pernas alternam de verdade entre capturas sucessivas da camera de debug.
YOLO detecta as 3 simultaneamente (confianca 0.73-0.92). O rastreador
mantem ate 3 tracks simultaneos, mas com mais troca de ID (7 IDs vistos em
~23s pra 3 pessoas) do que nos cenarios de alvo unico da 4.4/4.5 -
resultado esperado e ja discutido: a cena agora tem oclusao visual real
entre pedestres e ruido de deteccao com multiplos alvos, algo que nenhum
cenario anterior expunha. Fica registrado como alvo pra investigar a
robustez da associacao sob essas condicoes mais realistas.

### 4.7 — supressao de duplicata (corrige ids fantasmas do 4.6)

Investigacao do item deixado pendente no 4.6: gravados 45s de
`/tracker_node/tracks` ao vivo com as 3 pessoas do 4.6 andando
simultaneamente (`gravador_node`/leitura direta do topico). Agrupando por
id, 3 ids de vida longa (quase os 45s inteiros) correspondem claramente
as 3 pessoas reais - a associacao funciona bem na maior parte do tempo.
Mas apareceram 3 ids "fantasma" de vida curta (um instantaneo em t=0, um
de ~10s em t≈16s, um de <1s em t≈42s) - **todos na mesma regiao
espacial**, perto de onde o caminho vertical de uma pessoa cruza
geometricamente o caminho retangular de outra.

**Causa raiz:** no ciclo em que uma pessoa real tem sua deteccao casada
normalmente com o track dela (turno 1 ou 2 da associacao), uma SEGUNDA
deteccao da MESMA pessoa surge a poucos centimetros da primeira (silhueta
particionada pela proximidade com a outra pessoa, ou um frame do
"flipbook" de caminhada capturado em transicao) e sobra sem par. O laco
principal (`rastreador.py`) tratava TODA deteccao sem par como objeto
novo, nascendo um track `TENTATIVO` bem em cima do track que ja existe -
o id fantasma.

**Correcao:** `Rastreador3D._filtrar_duplicatas` (novo, submodulo 4.7) -
antes de abrir track novo pra uma deteccao sem par, descarta ela se
estiver a `raio_supressao_duplicata` metros (padrao 0.5m, parametro ROS
`raio_supressao_duplicata` do `tracker_node`) ou menos de um track que JA
foi observado/atualizado NESTA MESMA rodada. So considera tracks
atualizados agora (nao qualquer track parado/antigo), pra nao impedir uma
pessoa nova de abrir track proprio so por aparecer perto de um track
velho sem atualizacao recente. Validado com cenarios fabricados
(`test_4_7_supressao_duplicata.py`): deteccao fantasma a 15cm de um track
recem-atualizado nao cria track novo; deteccao de verdade longe de tudo
continua criando; duas pessoas reais a 0.8m uma da outra (mais que o raio
de 0.5m) continuam confirmando como tracks distintos.

### 4.8 — gate adaptativo + OCM na recuperacao (corrige troca de id)

Pedido explicito do usuario: testar se o rastreador respeita o principio
basico de MOT de manter o MESMO id por pessoa ao longo do tempo quando
nao ha oclusao real - e corrigir se nao respeitar.

**Teste ao vivo (97s, pipeline limpo, 1 publisher confirmado por topico
via `ros2 topic info -v`):** resultado inicial pior do que o esperado - um
unico id sobrevivia a janela TODA (parecia perfeito), mas tracando a
trajetoria dele apareciam saltos de 0.6-1.0m em 0.2-0.3s (2.7-3.4 m/s,
~10x a velocidade maxima de qualquer pessoa configurada). O id estava
pulando silenciosamente entre pessoas DIFERENTES.

**Causa raiz:** o `gate_distancia` (1.5m, usado tanto no turno normal de
associacao quanto no OCR de recuperacao) era maior que a menor distancia
real entre pessoas distintas na cena (`atores.yaml`): pessoa_2-pessoa_3
ficam a so 0.5m, pessoa_1-pessoa_2 chegam a 1.0m (e literalmente SE
CRUZAM em (2,1) e (2,3) - distancia zero nesses 2 pontos). Alem disso, o
OCR (`recuperacao.recuperar_perdidos`) usava esse MESMO gate fixo
independente de ha quanto tempo o track estava perdido, e ignorava o
custo de direcao do OCM (3.4) - exatamente o mecanismo feito pra
desambiguar por movimento, nao so posicao.

**Correcao (2 iteracoes, cada uma medida ao vivo antes de seguir pra
proxima):**
1. OCR ganhou um gate ADAPTATIVO (`velocidade_maxima_esperada * tempo_perdido
   + margem_gate`, nunca acima de `gate_distancia`) em vez do gate fixo, e
   passou a somar o custo de direcao do OCM na recuperacao, nao so na
   associacao normal (`recuperacao.recuperar_perdidos`, `associacao.associar`
   generalizado pra aceitar um gate por track). Testado ao vivo de novo:
   melhorou (saltos ficaram menores, 0.3-0.5m), mas nao resolveu - o
   `gate_distancia` do turno NORMAL (nao so o OCR) ainda estava em 1.5m,
   deixando a associacao comum por si so casar o track com a deteccao de
   OUTRA pessoa em varios passos pequenos, cada um dentro do gate.
2. `gate_distancia` reduzido de 1.5m para 0.4m (abaixo da menor distancia
   real entre pessoas DIFERENTES, 0.5m, com margem de seguranca) - e os
   parametros do gate adaptativo do OCR junto (`velocidade_maxima_esperada`
   0.6→0.25, `margem_gate_recuperacao` 0.3→0.1), todos ainda bem acima do
   deslocamento real esperado entre 2 deteccoes consecutivas (pessoas andam
   a <=0.3 m/s a ~10-20Hz).

**Resultado validado ao vivo (97.7s, apos a 2a iteracao):** pessoa_3 (que
nunca se cruza geometricamente com ninguem, so fica a 0.5m de pessoa_2)
ficou limpa - nenhuma contaminacao entre ela e as outras 2 em toda a
gravacao. Pessoa_2 (retangulo) tambem aparece como tracks coerentes com
o formato certo do caminho. Ainda restam trocas de id ocasionais
especificamente pessoa_1↔pessoa_2 bem no ponto (2,1)/(2,3) - **e la elas
se cruzam de verdade** (distancia fisica zero no instante do cruzamento,
nao so "perto"): nenhum gate de distancia, por menor que seja, pode
diferenciar 2 objetos que estao literalmente na mesma posicao num motion-only
tracker sem ReID. Isso e consistente com o principio testado, nao uma
violacao dele - "sem oclusao real" exclui exatamente esse caso, porque 2
corpos na mesma posicao AO MESMO TEMPO sao, pela definicao de deteccao por
silhueta, uma forma de oclusao mutua. Registrado como limitacao conhecida,
nao como bug pendente.

Testes: `test_4_8_gate_adaptativo_recuperacao.py` (via `Rastreador3D`
completo - 2 pessoas reais a 1.0m uma da outra nao trocam de id so por 1
frame perdido; recuperacao legitima de oclusao longa continua funcionando)
+ `test_3_5_recuperacao.py` (unitario - gate adaptativo rejeita deslocamento
fisicamente impossivel mesmo dentro do gate global).

### 4.9 — bancada de avaliacao multi-pessoa

Estende a bancada original (4.1-4.4, 1 pessoa estatica + robo se movendo)
pro que o projeto realmente precisa validar: VARIAS pessoas andando (4.6)
+ robo parado OU andando. Novo em `saye_tracking/`: `verdade_atores.py`
(verdade analitica - recalcula a posicao de cada ator com a mesma formula
que `mover_pessoa_animada_node` usa, em vez de ler de volta do Gazebo,
fragil pro flipbook de quadros), `gravador_atores_node.py` (grava
hipotese do tracker + essa verdade), `rodar_suite_pessoas.py`
(orquestrador: pra cada combinacao de quantidade de pessoas (1/2/3) x
robo (parado/andando) - sempre os mesmos N primeiros atores de
`atores.yaml`, na mesma ordem, garantindo trajetoria identica entre
testes com quantidades diferentes).

**3 achados**, cada um achado rodando a bancada de verdade e vendo o
resultado nao bater com o esperado - nao adivinhados de antemao:

1. **Atores fantasma**: os atores com flipbook (4.6) ja vem spawnados no
   `simple_world.sdf` (quadro 0 de cada um, parado); um teste com so 1 das
   3 pessoas deixaria as outras 2 visiveis e PARADAS, contaminando a
   deteccao. Corrigido estacionando (teleporta pra z=-50) TODO quadro de
   TODO ator antes de cada combinacao, religando so os N que o teste
   precisa.
2. **Contaminacao entre testes via `tracker_node`**: ele e um processo de
   vida longa, nunca reiniciado entre combinacoes - um track `PERDIDO` de
   uma combinacao anterior podia sobreviver e ser "recuperado" (OCR) por
   engano contra a cena NOVA. Confirmado rodando a bancada inteira 2x: o
   MOTA de uma MESMA combinacao variou de -0.16 a 0.55 entre rodadas, e
   QUAL combinacao "dava errado" mudava a cada rodada - sintoma de
   contaminacao ordem-dependente, nao dificuldade real de alguma
   combinacao especifica. Corrigido com um servico novo,
   `/tracker_node/resetar` (`TrackerNode.callback_resetar`), chamado
   antes de cada combinacao.
3. **`/cmd_vel` residual entre testes**: mesmo apos o achado 2, sobrava
   instabilidade nos testes "andando" (MOTA entre -0.09 e 0.60 em rodadas
   diferentes). A suspeita inicial foi o bug ja documentado de timestamp
   de camera (`gravador_node.py`, Achado 3 - `header.stamp` as vezes vem
   com relogio de parede) - testado DIRETO (comparando `/clock` com o
   `header.stamp` da imagem, parado e andando, com os 3 atores andando
   junto pra replicar a carga real da bancada) e **nao reproduziu**
   (maior diferenca vista: 24ms, sempre normal). A causa real, achada
   reproduzindo sem querer: teleportar a pose do robo nao para as rodas -
   se `/cmd_vel` ficou com um valor diferente de zero de uma combinacao
   anterior (cenario interrompido antes do Twist zero final que
   `executar_cenario_node` publica ao terminar normalmente), o robo
   continua obedecendo o comando velho mesmo depois de teleportado pro
   spawn, podendo ir parar longe de qualquer ator - reproduzido ao vivo,
   um `/cmd_vel` residual levou o robo pra (-2.4, 9.1) e a deteccao ficou
   **100% vazia** (0 de 300 mensagens) ate ser corrigido. Corrigido
   publicando um Twist zero ANTES de resetar a pose, toda combinacao.
4. **Teleporte de ator falhando em silencio sob concorrencia** (o achado
   mais caro desta fase - levou a reabrir e depois DESCARTAR uma hipotese
   de "troca de id do rastreador" que na verdade era isto): cada ator
   (`mover_pessoa_animada_node`, antigo) subia como um PROCESSO PROPRIO,
   cada um com seu proprio cliente gz-transport chamando
   `/world/<mundo>/set_pose` (1 pose por chamada, 30Hz) - com 3 atores, 3
   clientes concorrentes martelando o MESMO servico nomeado. Reproduzido
   ao vivo (5+ rodadas): em ~33-50% delas, UM dos clientes passava a
   falhar 100% das chamadas pelo resto do teste (nao intermitente -
   sistematico), porque o `_teleportar` original descartava o retorno
   `(bool, resposta)` do `request()` sem checar - confirmado consultando a
   pose REAL no Gazebo (`gz model -p`) durante um teste "ruim": a pessoa
   estava literalmente parada no pose de estacionamento (z=-50) por boa
   parte do teste, o que a verdade ANALITICA antiga (calculada so pela
   formula, sem olhar o Gazebo) nao conseguia detectar - ela assumia que o
   teleporte sempre funcionava. Recriar o cliente gz-transport apos falhas
   consecutivas NAO recuperava (testado: ainda 0% de sucesso apos 6
   recriacoes).

   **Correcao** (detalhe tecnico completo em `gz_pose_vector.py`): troca
   por 1 SO processo (`mover_pessoas_node`, novo) que move TODOS os atores
   do teste numa unica chamada de `/world/<mundo>/set_pose_vector` por
   tick - sem concorrencia entre clientes, sem a falha. Toda chamada tem o
   retorno checado; uma falha e logada (nunca mais silenciosa). Alem
   disso, `gravador_atores_node` parou de CALCULAR a verdade pela formula
   e passou a LER a pose REAL de volta do Gazebo (gz-transport direto no
   topico nativo `/world/<mundo>/pose/info`, que preserva o campo `name` -
   diferente da ponte `ros_gz_bridge` pra `tf2_msgs/TFMessage` usada no
   `gravador_node`/4.1, que descarta nome e timestamp por transform).
   Detalhe que so apareceu testando ao vivo: inicialmente a verdade tentou
   CALCULAR qual quadro do flipbook deveria estar ativo (mesma formula do
   mover) e so entao ler a pose medida DAQUELE nome - isso gravou
   100% (0, 0) do inicio ao fim, porque o gravador sobe ~1-2s depois do
   mover (tempo de assentamento da bancada) e um ciclo INTEIRO do flipbook
   dura so ~1s, entao qualquer defasagem de tick faz a formula apontar pro
   quadro ERRADO (quase sempre um estacionado). Corrigido DETECTANDO o
   quadro ativo pelos dados medidos (o unico, entre os N quadros de um
   ator, que nao esta com `z` perto de -50), sem depender de nenhuma
   sincronizacao de tick entre os dois nos.

   Validado ao vivo apos a correcao: 3 atores andando simultaneamente por
   ~24s, 1416 amostras de verdade gravadas, **zero** amostras em (0, 0) ou
   em qualquer posicao de estacionamento - todas as posicoes medidas
   condizem com os caminhos configurados em `atores.yaml`.

**Resultado ANTES do achado 4** (3 rodadas completas, 6 combinacoes cada):
robo parado parecia consistentemente bom (MOTA 0.76-0.92 em todas as 9
execucoes "parado" das 3 rodadas); robo andando era instavel (MOTA de
-0.17 a 0.60). Esses numeros estavam contaminados pelo achado 4
(teleporte de ator falhando em silencio) - descartados.

**Baseline oficial** (pos-correcao, item 3 do roteiro: 3 rodadas
completas com a arquitetura corrigida - `mover_pessoas_node` + verdade
medida + checagens de validade do item 2, nenhuma combinacao invalidada
nas 18 execucoes):

| n_pessoas | robo | MOTA (media ± desvio) | **IDF1** (media ± desvio) | MOTP | switches (media) | falsos positivos (media) | perdas (media) |
|---|---|---|---|---|---|---|---|
| 1 | **parado** | 0.858 ± 0.026 | **0.923 ± 0.015** | 0.017 | 0.0 | 0.0 | 46.7 |
| 2 | **parado** | 0.804 ± 0.009 | **0.806 ± 0.059** | 0.016 | 2.7 | 0.3 | 122.0 |
| 3 | **parado** | 0.727 ± 0.009 | **0.722 ± 0.057** | 0.016 | 6.7 | 1.0 | 257.0 |
| 1 | andando | **0.610 ± 0.049** | 0.715 ± 0.043 | 0.019 | 6.7 | 2.0 | 117.7 |
| 2 | andando | **0.491 ± 0.017** | 0.603 ± 0.034 | 0.020 | 7.3 | 1.7 | 318.3 |
| 3 | andando | **0.524 ± 0.009** | 0.446 ± 0.009 | 0.018 | 10.7 | 1.7 | 443.0 |

(item 4 do roteiro - metrica em **negrito** por linha e a que importa pra
decidir se aquele cenario esta bom: `idf1` pro robo parado - prioridade e
manter o id certo por pessoa, por decisao do usuario -, `mota` pro robo
andando - prioridade e rastreamento geral, ja filtrado pelo FOV da
camera.)

Comparado com o resultado contaminado: **o desvio despencou** (ex.: robo
andando com 1 pessoa ia de -0.17 a 0.60 - amplitude de 0.77 - e agora e
0.610 ± 0.049, desvio de so 0.05) - forte confirmacao de que o achado 4
(nao a dificuldade intrinseca do cenario) era a causa dominante da
instabilidade anterior. MOTA cai de forma consistente (nao mais
erratica) conforme mais pessoas sao adicionadas - esperado, mais pessoas
= mais cruzamentos/oclusao real.

**Achado novo, exposto so agora que a verdade e confiavel**: mesmo com o
robo PARADO (onde, por acordo com o usuario, a prioridade e identidade -
nao trocar o id de uma pessoa), ha troca de id real (nao mais artefato de
infraestrutura): media de 2.7 switches/execucao com 2 pessoas, 6.7 com 3
pessoas - e o IDF1 cai de 0.923 (1 pessoa, sem cruzamento possivel) pra
0.806 e 0.722 conforme pessoas (e cruzamentos) sao adicionadas. Isso
confirma que a investigacao original de "troca de id com o robo parado"
(que motivou abrir toda esta correcao) tem, sim, uma causa residual real
no RASTREADOR, a ser investigada no item 5 do roteiro - so que agora com
um numero confiavel pra comparar antes/depois de qualquer mudanca no
rastreador, em vez do ruido de infraestrutura que mascarava tudo antes.
Note tambem que IDF1 e MOTA NEM SEMPRE se movem juntos (ex.: robo
andando com 3 pessoas: MOTA 0.524 mas IDF1 so 0.446) - exatamente a
razao de reportar os dois em vez de confiar em so um numero agregado.

CSVs completos das 18 execucoes (3 rodadas x 6 combinacoes) nao sao
versionados (arquivos grandes, regeneraveis rodando `rodar_suite_pessoas`
3x) - so este resumo agregado fica no README.

Testes: `test_4_9_verdade_atores.py` (formula de movimento/quadro ativo,
sem ROS - a verdade GRAVADA pela bancada ja nao usa mais essa formula
diretamente, ver achado 4) + `test_4_10_teleportador_em_lote.py`
(`TeleportadorEmLote` nunca mascara falha de teleporte como sucesso, sem
Gazebo de verdade - cliente gz-transport fake) + `test_4_11_validacao_
bancada.py` (checagens de validade do item 2 - distancia andada por
ator, robo parado no spawn - sem ROS).

## Dependencias

`ultralytics` e `motmetrics` nao tem rosdep key — instale via pip (convencao do workspace):

```bash
pip install ultralytics motmetrics --break-system-packages
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

### Treinando o detector com o KITTI (tentativa - revertida em producao)

O `yolov8n-seg.pt` em producao e o checkpoint generico do ultralytics
(pre-treinado so no COCO). Tentamos fine-tuning com o
[KITTI](https://docs.ultralytics.com/datasets/detect/kitti/) (dataset de
deteccao 2D, mirror pronto do proprio ultralytics - 5985 imagens de treino
+ 1496 de validacao, baixado direto de
`https://github.com/ultralytics/assets/releases/download/v0.0.0/kitti.zip`,
sem cadastro, ~390MB) esperando melhorar deteccao de pedestre. **Resultado:
piorou a deteccao na simulacao - revertido pro `yolov8n-seg.pt` original.**
Fica documentado porque o motivo do fracasso e especifico e vale saber
antes de tentar de novo.

**Pipeline usado:**
```bash
# os scripts/preparar_dataset_kitti.py + treinar_yolo_kitti.py documentados
# anteriormente tambem funcionam (pro KITTI Tracking Benchmark oficial,
# que exige cadastro em cvlibs.net) - o que foi USADO de fato na pratica
# foi o mirror do ultralytics, mais simples:

# 1. baixa o mirror (ja vem com images/{train,val} + labels/{train,val}
#    em formato YOLO de DETECCAO - caixa, nao poligono)
curl -L -o kitti.zip https://github.com/ultralytics/assets/releases/download/v0.0.0/kitti.zip
unzip kitti.zip -d kitti_extraido

# 2. converte caixa -> poligono (mesma razao do preparar_dataset_kitti.py:
#    projecao3d_node precisa de mascara) e filtra so pedestrian+Person_sitting
python3 scripts/converter_deteccao_para_seg.py \
    --origem kitti_extraido --saida dataset_kitti_pessoas_seg

# 3. fine-tuning (CPU, maquina sem GPU)
python3 scripts/treinar_yolo_kitti.py --dataset dataset_kitti_pessoas_seg/dataset.yaml
```

**Duas rodadas de treino**, cada uma validada contra o proprio conjunto
de validacao do KITTI antes de seguir:

| | COCO (sem fine-tuning) | v1 (640px, freeze=10, 15 epocas, 2h46) | v2 (960px, freeze=5, 25 epocas, 12h38) |
|---|---|---|---|
| mAP50 (caixa) | 0,416 | 0,616 | **0,756** |
| mAP50-95 (caixa) | 0,150 | 0,307 | **0,402** |
| mAP50 (mascara) | 0,042 | 0,502 | **0,634** |

Cada rodada melhorou de verdade **no proprio benchmark do KITTI** -
reduzir o `freeze`, aumentar `imgsz` e rodar mais epocas funcionou
exatamente como esperado para esse objetivo.

**O problema: essa validacao mede o dominio errado.** O KITTI e fotografia
real de camera de carro. As pessoas que o robo ve sao modelos 3D
RENDERIZADOS pelo Gazebo (fase 4.6) - um visual bem diferente (sem a
textura/ruido/iluminacao de foto real). Comparando os dois modelos nos
MESMOS 20 frames capturados ao vivo da simulacao (nao do KITTI):

| | COCO original | v2 (fine-tuned KITTI) |
|---|---|---|
| Frames com deteccao | 20/20 | 16/20 |
| Deteccoes totais | 51 | 21 |
| Confianca media | 0,790 | 0,512 |

O fine-tuning especializou o modelo pra reconhecer foto real de rua, e
isso o tornou PIOR em reconhecer gente sintetica do Gazebo - o COCO
generalista, por acaso, generaliza melhor pro visual estilizado da
simulacao do que um modelo nichado em fotografia real. Efeito colateral
observado no rastreador: menos deteccao por frame -> mais tracks indo
`PERDIDO` -> ids novos nascendo bem mais rapido (contador global passou de
~260 em poucos minutos de simulacao, varias vezes mais rapido que com o
COCO original).

**Licao:** validar um fine-tuning so no benchmark de origem (aqui, o
proprio KITTI) nao basta quando o dominio de implantacao e diferente -
precisa comparar nos dados reais de onde o modelo vai rodar. Os checkpoints
`models/yolov8n-seg-kitti-pessoas{,-v2}.pt` ficam guardados (nao
commitados - grandes demais / regenerar com o pipeline acima) para o dia
em que o robo rodar com camera de verdade no mundo real, onde o dominio do
KITTI (foto real de rua) faz sentido de novo. `config/deteccao.yaml`
permanece com `yolov8n-seg.pt` (o original) em producao na simulacao.

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
