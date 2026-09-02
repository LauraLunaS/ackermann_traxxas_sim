"""
No de deteccao YOLOv8-seg para o pipeline de rastreamento do rover "saye".

Fase 1 do pipeline de MOT. Assina a imagem RGB da RealSense simulada, roda
YOLOv8-seg e publica:

  - <ns>/deteccoes  (vision_msgs/Detection2DArray) : bbox + classe + score
  - <ns>/mascaras   (sensor_msgs/Image, mono8)     : mascara de instancias
  - <ns>/debug_image (sensor_msgs/Image, bgr8)      : overlay para inspecao

Contrato da mascara de instancias: o pixel com valor ``i + 1`` corresponde a
``deteccoes.detections[i]``; ``0`` e fundo. As tres mensagens compartilham o
mesmo ``header`` (stamp e frame_id) da imagem de entrada, para permitir a
sincronizacao exata na Fase 2 (extracao 3D).
"""

import os

from cv_bridge import CvBridge
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from vision_msgs.msg import (
    BoundingBox2D,
    Detection2D,
    Detection2DArray,
    ObjectHypothesisWithPose,
)

try:
    from ultralytics import YOLO
except ImportError as exc:  # pragma: no cover - dependencia externa via pip
    raise ImportError(
        'ultralytics nao encontrado. Instale com: '
        'pip install ultralytics --break-system-packages'
    ) from exc


class DeteccaoNode(Node):
    """Roda YOLOv8-seg em cada frame e publica deteccoes 2D + mascaras."""

    def __init__(self):
        super().__init__('deteccao_node')

        # --- Parametros -----------------------------------------------------
        self.declare_parameter('modelo', 'yolov8n-seg.pt')
        self.declare_parameter('topico_imagem', '/camera/realsense/image_raw')
        self.declare_parameter('confianca_min', 0.4)
        self.declare_parameter('iou_nms', 0.5)
        self.declare_parameter('imgsz', 640)
        self.declare_parameter('device', '')          # '' = auto, 'cpu', 'cuda:0'
        self.declare_parameter('classes', ['person'])  # nomes COCO a manter
        self.declare_parameter('publicar_debug', True)
        self.declare_parameter('half', False)

        modelo = self._resolver_modelo(self.get_parameter('modelo').value)
        topico_imagem = self.get_parameter('topico_imagem').value
        self.conf = float(self.get_parameter('confianca_min').value)
        self.iou = float(self.get_parameter('iou_nms').value)
        self.imgsz = int(self.get_parameter('imgsz').value)
        self.device = self.get_parameter('device').value or None
        self.half = bool(self.get_parameter('half').value)
        self.publicar_debug = bool(self.get_parameter('publicar_debug').value)
        nomes_classes = list(self.get_parameter('classes').value)

        # --- Modelo -------------------------------------------------------
        self.get_logger().info(f'Carregando modelo YOLO: {modelo}')
        self.model = YOLO(modelo)
        self.nomes = self.model.names  # {id: nome}
        nome_para_id = {v: k for k, v in self.nomes.items()}

        if nomes_classes:
            desconhecidas = [n for n in nomes_classes if n not in nome_para_id]
            if desconhecidas:
                self.get_logger().warn(
                    f'Classes ignoradas (nao existem no modelo): {desconhecidas}'
                )
            self.filtro_classes = [
                nome_para_id[n] for n in nomes_classes if n in nome_para_id
            ]
        else:
            self.filtro_classes = None  # todas as classes

        self.get_logger().info(
            f'Filtro de classes: '
            f'{[self.nomes[i] for i in self.filtro_classes] if self.filtro_classes else "todas"}'
        )

        # --- ROS I/O -----------------------------------------------------
        self.bridge = CvBridge()
        self.processando = False

        self.pub_det = self.create_publisher(
            Detection2DArray, '~/deteccoes', 10)
        self.pub_masc = self.create_publisher(
            Image, '~/mascaras', qos_profile_sensor_data)
        self.pub_debug = self.create_publisher(
            Image, '~/debug_image', qos_profile_sensor_data)

        self.sub = self.create_subscription(
            Image, topico_imagem, self.imagem_callback, qos_profile_sensor_data)

        self.get_logger().info(
            f'Deteccao iniciada. Assinando "{topico_imagem}" '
            f'(conf={self.conf}, imgsz={self.imgsz}, device={self.device or "auto"})'
        )

    # ------------------------------------------------------------------
    def imagem_callback(self, msg: Image):
        if self.processando:
            # Descarta o frame: o executor e single-thread e a inferencia
            # pode ser mais lenta que a taxa da camera (30 Hz).
            return
        self.processando = True
        try:
            self._processar(msg)
        except Exception as exc:  # noqa: BLE001 - nao derrubar o no por 1 frame
            self.get_logger().error(f'Falha ao processar frame: {exc}')
        finally:
            self.processando = False

    # ------------------------------------------------------------------
    def _processar(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        altura, largura = frame.shape[:2]

        resultados = self.model.predict(
            frame,
            conf=self.conf,
            iou=self.iou,
            imgsz=self.imgsz,
            classes=self.filtro_classes,
            device=self.device,
            half=self.half,
            verbose=False,
        )
        res = resultados[0]

        det_array = Detection2DArray()
        det_array.header = msg.header

        mascara_inst = np.zeros((altura, largura), dtype=np.uint8)

        n = 0 if res.boxes is None else len(res.boxes)
        mascaras = None
        if res.masks is not None and n > 0:
            # res.masks.data: (n, h, w) float na resolucao da inferencia.
            mascaras = res.masks.data.cpu().numpy()

        for i in range(n):
            box = res.boxes[i]
            cls_id = int(box.cls.item())
            score = float(box.conf.item())
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            det = Detection2D()
            det.header = msg.header
            det.id = str(i)

            bbox = BoundingBox2D()
            bbox.center.position.x = (x1 + x2) / 2.0
            bbox.center.position.y = (y1 + y2) / 2.0
            bbox.center.theta = 0.0
            bbox.size_x = float(x2 - x1)
            bbox.size_y = float(y2 - y1)
            det.bbox = bbox

            hip = ObjectHypothesisWithPose()
            hip.hypothesis.class_id = self.nomes.get(cls_id, str(cls_id))
            hip.hypothesis.score = score
            det.results.append(hip)

            det_array.detections.append(det)

            if mascaras is not None and i < len(mascaras):
                m = mascaras[i]
                if m.shape != (altura, largura):
                    m = self._redimensionar_mascara(m, largura, altura)
                mascara_inst[m > 0.5] = min(i + 1, 255)

        self.pub_det.publish(det_array)

        msg_masc = self.bridge.cv2_to_imgmsg(mascara_inst, encoding='mono8')
        msg_masc.header = msg.header
        self.pub_masc.publish(msg_masc)

        if self.publicar_debug and self.pub_debug.get_subscription_count() > 0:
            overlay = res.plot()  # BGR anotado
            msg_dbg = self.bridge.cv2_to_imgmsg(overlay, encoding='bgr8')
            msg_dbg.header = msg.header
            self.pub_debug.publish(msg_dbg)

    # ------------------------------------------------------------------
    def _resolver_modelo(self, modelo: str) -> str:
        """Resolve o caminho dos pesos; cai para download do ultralytics se ausente."""
        if os.path.isabs(modelo) or os.path.sep in modelo:
            return os.path.expanduser(modelo)
        pasta = os.path.expanduser('~/ackermann_sim/src/saye_tracking/models')
        candidato = os.path.join(pasta, modelo)
        if os.path.exists(candidato):
            return candidato
        self.get_logger().warn(
            f'"{modelo}" nao achado em {pasta}; ultralytics vai baixar no cwd.'
        )
        return modelo

    # ------------------------------------------------------------------
    @staticmethod
    def _redimensionar_mascara(m: np.ndarray, largura: int, altura: int) -> np.ndarray:
        import cv2
        return cv2.resize(
            m.astype(np.float32), (largura, altura), interpolation=cv2.INTER_NEAREST
        )


def main(args=None):
    rclpy.init(args=args)
    node = DeteccaoNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
