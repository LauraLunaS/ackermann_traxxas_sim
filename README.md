# Ackermann Vehicle Simulation — CIn/UFPE

Simulação de um rover Ackermann (Traxxas Slash 4x4 VXL Ultimate) com ROS2 Jazzy e Gazebo Harmonic, desenvolvida como ambiente de teste para o projeto de rover autônomo do time.

## Pré-requisitos

- Ubuntu 24.04
- ROS2 Jazzy
- Gazebo Harmonic

## Instalação

```bash
# Clonar o repositório
git clone <url_do_repositorio> ~/ackermann_sim
cd ~/ackermann_sim

# Instalar dependências
sudo apt install ros-jazzy-ros-gz ros-jazzy-nav2-* \
  ros-jazzy-slam-toolbox ros-jazzy-rtabmap-ros -y

rosdep install --from-paths src --ignore-src -r -y

# Compilar
colcon build

# Instalar o nó de desvio de obstáculos
cd src/obstacle_avoider
pip install . --break-system-packages
cp ~/.local/bin/obstacle_avoider ~/ackermann_sim/install/obstacle_avoider/lib/obstacle_avoider/obstacle_avoider
cp ~/.local/bin/camera_info_publisher ~/ackermann_sim/install/obstacle_avoider/lib/obstacle_avoider/camera_info_publisher
```

## Como rodar

### 1. Simulação básica

**Terminal 1 — Simulação:**
```bash
source ~/ackermann_sim/install/setup.bash
ros2 launch saye_bringup traxxas_spawn.launch.py
```

**Terminal 2 — Desvio de obstáculos:**
```bash
source ~/ackermann_sim/install/setup.bash
python3 -m obstacle_avoider.ackermann_obstacle_avoider
```

### 2. SLAM (gerar mapa)

**Terminal 2 — slam_toolbox:**
```bash
ros2 launch slam_toolbox online_async_launch.py \
  use_sim_time:=true \
  slam_params_file:=$HOME/ackermann_sim/slam_toolbox_params.yaml
```

**Terminal 3 — Desvio para explorar:**
```bash
python3 -m obstacle_avoider.ackermann_obstacle_avoider
```

**Salvar o mapa quando estiver completo:**
```bash
ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap \
  "name: {data: '/home/$USER/ackermann_sim/src/ackermann-vehicle-gzsim-ros2/saye_bringup/maps/map'}"
```

**Recompilar após salvar o mapa:**
```bash
cd ~/ackermann_sim
colcon build --packages-select saye_bringup
source install/setup.bash
```

### 3. Navegação por waypoints (Nav2)

**Terminal 1 — Simulação:**
```bash
source ~/ackermann_sim/install/setup.bash
ros2 launch saye_bringup traxxas_spawn.launch.py
```

**Terminal 2 — Nav2:**
```bash
source ~/ackermann_sim/install/setup.bash
ros2 launch saye_bringup nav_fisico_sim.launch.py
```

**Terminal 3 — RViz2:**
```bash
rviz2 -d /opt/ros/jazzy/share/nav2_bringup/rviz/nav2_default_view.rviz
```

No RViz2:
1. **"2D Pose Estimate"** → clique e arraste onde o robô está
2. **"Nav2 Goal"** → clique no destino


# Integração de Waypoints: Simulação para o Robô Real
Este guia prático descreve como a equipe deve integrar o script de automação (trajectory_waypoints.py) e o arquivo de coordenadas (waypoints.json) no ambiente físico do Rover.

## 1. Transferência dos Arquivos para a Raspberry Pi
O script de automação e o arquivo de coordenadas devem ser copiados para a Raspberry Pi embarcada do robô.

### Passo 1.1: Cópia via Terminal (SCP)
A partir do computador onde a simulação foi desenvolvida, envie os arquivos para a Pi (substitua usuario e ip_da_raspberry_pi pelos dados reais do robô):

```bash
# Copiar o script de waypoints
scp ~/ackermann_sim/src/ackermann-vehicle-gzsim-ros2/saye_bringup/scripts/trajectory_waypoints.py usuario@ip_da_raspberry_pi:~/
```

```bash
# Copiar o arquivo de configuração de pontos
scp ~/ackermann_sim/src/ackermann-vehicle-gzsim-ros2/saye_bringup/config/waypoints.json usuario@ip_da_raspberry_pi:~/
```

### Passo 1.2: Permissão de Execução e Ajuste de Caminho
Aceda à Raspberry Pi via SSH para configurar o ambiente:

Dar permissão de execução:

``` bash
chmod +x ~/trajectory_waypoints.py
```

Ajustar o caminho do JSON no código:
Abra o script na Pi (nano ~/trajectory_waypoints.py) e altere a linha que lê o arquivo para apontar para o diretório local da Pi:

```
# Altere esta linha para localizar o JSON corretamente na Pi:
caminho_json = os.path.expanduser('~/waypoints.json')
```

## Coleta de Coordenadas Reais da Arena
No ambiente real, a origem (0,0) do mapa é estabelecida no ponto exato onde o Rover se encontra quando a equipa sincroniza o mapa físico. 
1. Com o SLAM/Cartographer ativo e o robô visível no RViz2, movimente o Rover manualmente (via rádio ou teleoperação) pelos pontos de interesse da sala.
2. No RViz2, anote a posição exata (X, Y) e a orientação em radianos (Yaw) fornecida pelo frame do robô em cada local desejado.
3. Abra o arquivo waypoints.json na Raspberry Pi e substitua os valores simulados pelas coordenadas reais capturadas em campo:

``` 
JSON{
  "waypoints": [
    {"name": "Ponto de Interesse 1", "x": 1.50, "y": -0.40, "yaw": 0.0},
    {"name": "Ponto de Interesse 2", "x": 2.20, "y": 1.05, "yaw": 1.57},
    {"name": "Retorno ao Início", "x": 0.0, "y": 0.0, "yaw": 3.14}
  ]
}
```

## 3. Execução da Rota 
Execute o script diretamente no terminal da Raspberry Pi:

``` Bash
python3 ~/trajectory_waypoints.py
``` 
