import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image
from rclpy.qos import QoSProfile, ReliabilityPolicy

class CameraInfoPublisher(Node):
    def __init__(self):
        super().__init__('camera_info_publisher')

        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)

        # Subscreve na imagem para copiar o timestamp exato
        self.sub = self.create_subscription(
            Image, '/camera/front_raw', self.image_callback, qos)
        self.pub = self.create_publisher(CameraInfo, '/camera/front_info', 10)
        self.get_logger().info('Camera info publisher iniciado!')

    def image_callback(self, img_msg):
        msg = CameraInfo()

        # Copia o header exato da imagem — timestamp e frame_id iguais
        msg.header = img_msg.header

        # Resolução correta da câmera simulada
        msg.width  = img_msg.width   # 720
        msg.height = img_msg.height  # 1080

        # Matriz intrínseca K ajustada para 720x1080
        fx = 360.0
        fy = 360.0
        cx = float(img_msg.width)  / 2.0
        cy = float(img_msg.height) / 2.0

        msg.k = [fx,  0.0, cx,
                 0.0, fy,  cy,
                 0.0, 0.0, 1.0]

        msg.d = [0.0, 0.0, 0.0, 0.0, 0.0]
        msg.distortion_model = 'plumb_bob'

        msg.r = [1.0, 0.0, 0.0,
                 0.0, 1.0, 0.0,
                 0.0, 0.0, 1.0]

        msg.p = [fx,  0.0, cx,  0.0,
                 0.0, fy,  cy,  0.0,
                 0.0, 0.0, 1.0, 0.0]

        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = CameraInfoPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
