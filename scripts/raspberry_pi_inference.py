"""
Lightweight Inference Script for Raspberry Pi
- Processes 1920x1080 images using 416x416 tiles.
- Sequential tile processing to minimize RAM usage.
- Uses Optimized INT8 Quantized ONNX model.
"""

import os
import sys
import time
import numpy as np
import cv2
import onnxruntime as ort
from pathlib import Path

# Project root setup
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class PiDetector:
    def __init__(self, model_path, classes):
        options = ort.SessionOptions()
        options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
        options.intra_op_num_threads = 4
        
        print(f"Loading optimized model: {model_path}")
        self.session = ort.InferenceSession(model_path, options, providers=['CPUExecutionProvider'])
        self.classes = classes
        self.input_name = self.session.get_inputs()[0].name
        self.img_size = 416

    def preprocess(self, tile):
        img = cv2.cvtColor(tile, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (self.img_size, self.img_size))
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0)
        return img

    def postprocess(self, outputs, conf_threshold=0.5):
        output = outputs[0][0]
        boxes = output[:4, :].T
        scores = output[4:, :].T
        class_ids = np.argmax(scores, axis=1)
        confidences = np.max(scores, axis=1)
        mask = confidences > conf_threshold
        return boxes[mask], confidences[mask], class_ids[mask]

    def slice_and_detect(self, image_path, tile_size=416, overlap=0.15):
        image = cv2.imread(image_path)
        h, w = image.shape[:2]
        stride = int(tile_size * (1 - overlap))
        all_detections = []
        
        start_time = time.time()
        for y in range(0, h - tile_size + 1, stride):
            for x in range(0, w - tile_size + 1, stride):
                tile = image[y:y+tile_size, x:x+tile_size]
                blob = self.preprocess(tile)
                outputs = self.session.run(None, {self.input_name: blob})
                boxes, confs, clss = self.postprocess(outputs)
                for box, conf, cls in zip(boxes, confs, clss):
                    cx, cy, bw, bh = box
                    x1 = (cx - bw/2) + x
                    y1 = (cy - bh/2) + y
                    x2 = x1 + bw
                    y2 = y1 + bh
                    all_detections.append([x1, y1, x2, y2, conf, cls])
                del blob
        
        final_boxes = self.non_max_suppression(all_detections, 0.45)
        latency = (time.time() - start_time) * 1000
        return final_boxes, latency

    def non_max_suppression(self, detections, iou_threshold):
        if not detections: return []
        dets = sorted(detections, key=lambda x: x[4], reverse=True)
        keep = []
        while dets:
            best = dets.pop(0)
            keep.append(best)
            remaining = []
            for d in dets:
                if self.calculate_iou(best[:4], d[:4]) < iou_threshold:
                    remaining.append(d)
            dets = remaining
        return keep

    def calculate_iou(self, box1, box2):
        x1, y1 = max(box1[0], box2[0]), max(box1[1], box2[1])
        x2, y2 = min(box1[2], box2[2]), min(box1[3], box2[3])
        inter = max(0, x2 - x1) * max(0, y2 - y1)
        area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
        area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
        return inter / (area1 + area2 - inter + 1e-6)

def main():
    MODEL_PATH = str(PROJECT_ROOT / 'models' / 'pi_optimized' / 'yolov8s_sliced_int8.onnx')
    CLASSES = ['Bolt', 'Bottle', 'Washer']
    IMAGE_PATH = str(PROJECT_ROOT / 'data' / 'samples' / 'sample1.jpg')
    
    if not os.path.exists(MODEL_PATH):
        print(f\"Error: Optimized model not found at {MODEL_PATH}\")
        return

    detector = PiDetector(MODEL_PATH, CLASSES)
    results, latency = detector.slice_and_detect(IMAGE_PATH)
    
    print(f\"Results: {len(results)} objects, Latency: {latency:.1f}ms\")

if __name__ == \"__main__\":
    main()
