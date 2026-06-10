import os
import json
import math
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy

def quaternion_from_euler(roll, pitch, yaw):
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)
    return [
        sr * cp * cy - cr * sp * sy,
        cr * sp * cy + sr * cp * sy,
        cr * cp * sy - sr * sp * cy,
        cr * cp * cy + sr * sp * sy
    ]

def main():
    rclpy.init()
    navigator = BasicNavigator()

    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    initial_pose.pose.position.x = -1.0
    initial_pose.pose.position.y = 1.0
    initial_pose.pose.orientation.w = 1.0
    navigator.setInitialPose(initial_pose)

    caminho_json = os.path.expanduser(
        '~/ackermann_sim/src/ackermann-vehicle-gzsim-ros2/saye_bringup/config/waypoints.json'
    )

    if not os.path.exists(caminho_json):
        print(f"❌ Arquivo não encontrado: {caminho_json}")
        rclpy.shutdown()
        return

    with open(caminho_json, 'r') as f:
        dados = json.load(f)

    print("Aguardando o ciclo de vida do Nav2 iniciar...")
    navigator.waitUntilNav2Active()
    print("Nav2 está pronto para receber os Waypoints!")

    nomes = [pt['name'] for pt in dados['waypoints']]
    lista_de_poses = []
    for pt in dados['waypoints']:
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = navigator.get_clock().now().to_msg()
        pose.pose.position.x = pt['x']
        pose.pose.position.y = pt['y']
        q = quaternion_from_euler(0, 0, pt['yaw'])
        pose.pose.orientation.x = q[0]
        pose.pose.orientation.y = q[1]
        pose.pose.orientation.z = q[2]
        pose.pose.orientation.w = q[3]
        lista_de_poses.append(pose)

    print(f"Enviando {len(lista_de_poses)} waypoints para o Traxxas...")
    navigator.followWaypoints(lista_de_poses)

    i = 0
    ultimo_waypoint = -1
    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()
        if feedback:
            atual = feedback.current_waypoint
            if atual != ultimo_waypoint:
                print(f"[{atual}] Iniciando: '{nomes[atual]}'")
                ultimo_waypoint = atual
        i += 1

    resultado = navigator.getResult()
    if resultado == TaskResult.SUCCEEDED:
        print("🎉 SUCESSO: O Traxxas visitou todos os pontos!")
    elif resultado == TaskResult.CANCELED:
        print("⚠️ Rota cancelada.")
    elif resultado == TaskResult.FAILED:
        print("❌ ERRO: Falha em algum waypoint.")

    rclpy.shutdown()

if __name__ == '__main__':
    main()