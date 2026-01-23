"""
Unified Inference Pipeline for Screw Detection
Integrates Slicing Aided Hyper Inference (SAHI) with the optimized Sliced-Trained YOLOv8 model.

Usage:
    python scripts/inference_pipeline.py --input path/to/image.jpg --output_dir results/
"""

import os
import sys
import json
import argparse
import time
from pathlib import Path
import cv2
import yaml
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction

def parse_args():
    parser = argparse.ArgumentParser(description="Screw Detection Inference Pipeline")
    parser.add_argument("--input", type=str, required=True, help="Path to input image")
    parser.add_argument("--weights", type=str, default="models/yolov8_sliced_best.pt", help="Path to model weights")
    parser.add_argument("--conf", type=float, default=0.7, help="Confidence threshold")
    parser.add_argument("--nms", type=float, default=0.6, help="NMS threshold (postprocess_match_threshold)")
    parser.add_argument("--slice_size", type=int, default=640, help="SAHI slice size")
    parser.add_argument("--overlap", type=float, default=0.2, help="SAHI overlap ratio")
    parser.add_argument("--output_dir", type=str, default="results/pipeline_outputs", help="Directory to save results")
    parser.add_argument("--device", type=str, default="cpu", help="Device (cpu or cuda:0)")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Setup paths
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Resolve relative weights path from project root
    weights_path = Path(args.weights)
    if not weights_path.exists():
        # Try relative to the script's parent
        script_dir = Path(__file__).parent.parent
        weights_path = script_dir / args.weights

    if not input_path.exists():
        print(f"Error: Input image {args.input} does not exist.")
        return

    # 1. Initialize Model
    print(f"Loading model: {weights_path}")
    try:
        detection_model = AutoDetectionModel.from_pretrained(
            model_type='yolov8',
            model_path=str(weights_path),
            confidence_threshold=0.1, # Keep low base threshold, filter in SAHI call
            device=args.device
        )
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # 2. Run SAHI Inference
    print(f"Running SAHI inference on {input_path.name}...")
    start_time = time.time()
    
    result = get_sliced_prediction(
        str(input_path),
        detection_model,
        slice_height=args.slice_size,
        slice_width=args.slice_size,
        overlap_height_ratio=args.overlap,
        overlap_width_ratio=args.overlap,
        postprocess_type=\"NMS\",
        postprocess_match_threshold=args.nms,
        verbose=0
    )
    
    end_time = time.time()
    latency = (end_time - start_time) * 1000
    
    # 3. Process Results
    detections = []
    # Class mapping (Assuming standard Bolt, Bottle, Washer)
    class_names = {0: \"Bolt\", 1: \"Bottle\", 2: \"Washer\"}
    
    for obj in result.object_prediction_list:
        if obj.score.value >= args.conf:
            detections.append({
                \"bbox\": [int(c) for c in obj.bbox.to_xyxy()],
                \"confidence\": round(float(obj.score.value), 4),
                \"class_id\": int(obj.category.id),
                \"class_name\": obj.category.name if obj.category.name else class_names.get(obj.category.id, \"Unknown\")
            })

    # 4. Save Outputs
    # A. JSON Results
    json_path = output_dir / f\"{input_path.stem}_results.json\"
    with open(json_path, \"w\") as f:
        json.dump({
            \"image\": str(input_path),
            \"latency_ms\": round(latency, 2),
            \"detection_count\": len(detections),
            \"parameters\": {
                \"conf_threshold\": args.conf,
                \"nms_threshold\": args.nms,
                \"slice_size\": args.slice_size
            },
            \"detections\": detections
        }, f, indent=4)
    
    # B. Annotated Image
    image = cv2.imread(str(input_path))
    for det in detections:
        x1, y1, x2, y2 = det[\"bbox\"]
        label = f\"{det['class_name']} {det['confidence']}\"
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    image_path = output_dir / f\"{input_path.stem}_annotated.jpg\"
    cv2.imwrite(str(image_path), image)
    
    print(\"-\" * 30)
    print(f\"Inference Complete!\")
    print(f\"Time: {latency:.2f} ms\")
    print(f\"Objects Found: {len(detections)}\")
    print(f\"Results saved to: {output_dir}\")
    print(\"-\" * 30)

if __name__ == \"__main__\":
    main()
