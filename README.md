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


