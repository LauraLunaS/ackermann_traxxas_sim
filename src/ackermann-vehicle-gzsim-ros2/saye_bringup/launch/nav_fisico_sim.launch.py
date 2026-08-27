import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_nav2_dir = get_package_share_directory('nav2_bringup')
    pkg_saye_bringup = get_package_share_directory('saye_bringup')

    # Ajustado default para 'True' se for ambiente simulado no Gazebo/Ignition
    use_sim_time = LaunchConfiguration('use_sim_time', default='True')
    autostart = LaunchConfiguration('autostart', default='True')
    slam = LaunchConfiguration('slam', default='True')

    nav2_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2_dir, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'autostart': autostart,
            'slam': slam,  # <--- Ativa o SLAM Toolbox/Online em tempo real
            'params_file': os.path.join(pkg_saye_bringup, 'config', 'nav2_params_fisico_sim.yaml'),
            'slam_params_file': os.path.join(pkg_saye_bringup, 'config', 'slam_toolbox_params.yaml'),
        }.items()
    )

    rviz_launch_cmd = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=[
            '-d', os.path.join(pkg_nav2_dir, 'rviz', 'nav2_default_view.rviz')
        ]
    )

    # Nao usar um relay de /cmd_vel_nav para /cmd_vel aqui: o collision_monitor
    # (nav2_params_fisico_sim.yaml: cmd_vel_out_topic: "cmd_vel") ja publica o
    # comando final, suavizado pelo velocity_smoother e checado por colisao,
    # diretamente em /cmd_vel. Um relay de /cmd_vel_nav (saida crua do
    # controller_server, sem smoothing nem checagem de colisao) para /cmd_vel
    # cria dois publishers concorrentes no mesmo topico.

    ld = LaunchDescription()

    ld.add_action(nav2_launch_cmd)
    # ld.add_action(rviz_launch_cmd) # Descomente se quiser abrir o RViz diretamente por este launch

    return ld