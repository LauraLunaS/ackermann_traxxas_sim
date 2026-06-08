import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math
from enum import Enum

# Definição clara dos Estados
class Estado(Enum):
    AVANCANDO = 1
    DESVIANDO_FRENTE = 2
    MANOBRA_RE = 3

class AckermannObstacleAvoider(Node):
    def __init__(self):
        super().__init__('ackermann_obstacle_avoider')

        # Parâmetros de distâncias
        self.DISTANCIA_SEGURA = 1.5
        self.DISTANCIA_CRITICA = 0.6  # Aumentado levemente para dar margem à cinemática
        
        # Parâmetros de atuadores
        self.VELOCIDADE_LINEAR = 0.2
        self.VELOCIDADE_RE = -0.15
        self.ANGULO_ESTERCO = 0.6

        # Inicialização do Estado
        self.estado_atual = Estado.AVANCANDO
        self.lado_desvio = 0 # -1 para Direita, 1 para Esquerda

        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('Ackermann FSM Obstacle Avoider iniciado!')

    def scan_callback(self, msg):
        ranges = msg.ranges
        total = len(ranges)
        meio = total // 2

        def valida(r):
            return not math.isinf(r) and not math.isnan(r) and r > 0.0

        cone = 30
        quarto = total // 4

        frente_indices   = list(range(meio - cone, meio + cone))
        esquerda_indices = list(range(meio + quarto - cone, meio + quarto + cone))
        direita_indices  = list(range(meio - quarto - cone, meio - quarto + cone))
        tras_indices     = list(range(max(0, meio + 2*quarto - cone), min(total, meio + 2*quarto + cone)))

        frente   = [ranges[i] for i in frente_indices   if valida(ranges[i])]
        esquerda = [ranges[i] for i in esquerda_indices if valida(ranges[i])]
        direita  = [ranges[i] for i in direita_indices  if valida(ranges[i])]
        tras     = [ranges[i] for i in tras_indices     if valida(ranges[i])]

        dist_frente   = min(frente)   if frente   else float('inf')
        dist_esquerda = min(esquerda) if esquerda else float('inf')
        dist_direita  = min(direita)  if direita  else float('inf')
        dist_tras     = min(tras)     if tras     else float('inf')

        # ==========================================
        # MAQUINA DE ESTADOS: LÓGICA DE TRANSIÇÃO
        # ==========================================
        
        if self.estado_atual == Estado.AVANCANDO:
            if dist_frente < self.DISTANCIA_CRITICA:
                self.estado_atual = Estado.MANOBRA_RE
                # Bloqueia o lado do desvio no momento do susto (evita oscilação)
                self.lado_desvio = 1 if dist_esquerda > dist_direita else -1
            elif dist_frente < self.DISTANCIA_SEGURA:
                self.estado_atual = Estado.DESVIANDO_FRENTE
                self.lado_desvio = 1 if dist_esquerda > dist_direita else -1

        elif self.estado_atual == Estado.DESVIANDO_FRENTE:
            if dist_frente < self.DISTANCIA_CRITICA:
                self.estado_atual = Estado.MANOBRA_RE
                self.lado_desvio = 1 if dist_esquerda > dist_direita else -1
            elif dist_frente >= self.DISTANCIA_SEGURA:
                self.estado_atual = Estado.AVANCANDO

        elif self.estado_atual == Estado.MANOBRA_RE:
            # SÓ SAI DA RÉ quando a frente estiver totalmente limpa (Histerese)
            # ou se houver risco iminente de bater a traseira
            if dist_frente >= self.DISTANCIA_SEGURA or dist_tras < self.DISTANCIA_CRITICA:
                self.estado_atual = Estado.AVANCANDO

        # ==========================================
        # MAQUINA DE ESTADOS: EXECUÇÃO DAS AÇÕES
        # ==========================================
        twist = Twist()

        if self.estado_atual == Estado.AVANCANDO:
            twist.linear.x = self.VELOCIDADE_LINEAR
            twist.angular.z = 0.0
            self.get_logger().info(f'AVANÇANDO → Tudo limpo ({dist_frente:.2f}m)')

        elif self.estado_atual == Estado.DESVIANDO_FRENTE:
            twist.linear.x = self.VELOCIDADE_LINEAR * 0.6
            # Executa a curva para o lado bloqueado anteriormente
            twist.angular.z = self.ANGULO_ESTERCO if self.lado_desvio == 1 else -self.ANGULO_ESTERCO
            direcao = "ESQUERDA" if self.lado_desvio == 1 else "DIREITA"
            self.get_logger().info(f'DESVIANDO FRENTE → Curva para {direcao} ({dist_frente:.2f}m)')

        elif self.estado_atual == Estado.MANOBRA_RE:
            twist.linear.x = self.VELOCIDADE_RE
            # ATENÇÃO À CINEMÁTICA ACKERRMANN NA RÉ:
            # Se há mais espaço na ESQUERDA (lado_desvio == 1), para a frente do carro apontar
            # para lá depois, você deve esterçar as rodas para a DIREITA ao dar ré!
            if self.lado_desvio == 1:
                twist.angular.z = -self.ANGULO_ESTERCO  # Esterça para a direita na ré
            else:
                twist.angular.z = self.ANGULO_ESTERCO   # Esterça para a esquerda na ré
                
            self.get_logger().info(f'MANOBRA RÉ → Afastando do obstáculo ({dist_frente:.2f}m)')

        self.cmd_pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = AckermannObstacleAvoider()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        stop = Twist()
        node.cmd_pub.publish(stop)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()