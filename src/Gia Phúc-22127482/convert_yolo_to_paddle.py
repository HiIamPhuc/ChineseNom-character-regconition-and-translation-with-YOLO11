import json
import os
from pathlib import Path
from PIL import Image
import numpy as np

# Adjust the directories as needed
images_dir = 'datasets/nom/raw1'
annotations_dir = 'datasets/nom/label_sorted1'
results_dir = 'datasets/nom/label_converted'
os.makedirs(results_dir, exist_ok=True)

def convert_yolo_to_corners(boxes, image_width, image_height):
    """
    Convert YOLO format boxes to corner coordinates
    
    Args:
        boxes: numpy array of shape (N, 5) with each row as [class_id, x_center, y_center, width, height]
        image_width: original image width
        image_height: original image height
        
    Returns:
        corner_boxes: list of dictionaries containing:
            - corners: list of [x,y] coordinates in clockwise order
            - class_id: original class ID
    """
    corner_boxes = []
    
    for box in boxes:
        class_id = int(box[0])
        
        # Convert normalized coordinates to absolute coordinates
        # x_center = box[1] * image_width
        # y_center = box[2] * image_height
        # width = box[3] * image_width
        # height = box[4] * image_height
        x_center = box[1]
        y_center = box[2]
        width = box[3]
        height = box[4]
        
        # Calculate corner coordinates
        x1 = int(x_center - width/2)  # Top-left
        y1 = int(y_center - height/2)
        x2 = int(x_center + width/2)  # Top-right
        y2 = int(y_center - height/2)
        x3 = int(x_center + width/2)  # Bottom-right
        y3 = int(y_center + height/2)
        x4 = int(x_center - width/2)  # Bottom-left
        y4 = int(y_center + height/2)
        
        # Store corners as list of [x,y] coordinates
        corners = [
            [x1, y1],  # Top-left
            [x2, y2],  # Top-right
            [x3, y3],  # Bottom-right
            [x4, y4]   # Bottom-left
        ]
        
        corner_boxes.append({
            'corners': corners,
            'class_id': class_id
        })
    
    return corner_boxes

def save_corner_format(corner_boxes, output_file):
    """
    Save boxes in corner format to file
    Each box is saved as a list of [x,y] coordinates
    """
    items = []
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, box in enumerate(corner_boxes):
            item = {}
            # Convert corners to string in required format
            item['transcription'] = ''
            item['bbox'] = json.dumps(box['corners'])
            items.append(item)

        json.dump(items, f, ensure_ascii=False, indent=4)

for image_path in Path(images_dir).glob("*.*"):
    if image_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
    # if Path(image_path).suffix.lower() not in [".jpg", ".jpeg", ".png"]:
        continue
    
    with Image.open(image_path) as img:
        img_width, img_height = img.size
        
    annotation_path = os.path.join(annotations_dir, f"{image_path.stem}.txt")

    boxes = []
    with open(annotation_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            class_id, x_center, y_center, width, height = map(float, line.strip().split())
            boxes.append([class_id, x_center, y_center, width, height])
            # f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

    # Convert to corner format
    corner_boxes = convert_yolo_to_corners(boxes, img_width, img_height)

    result_path = os.path.join(results_dir, f"{image_path.stem}.json")
    save_corner_format(corner_boxes, result_path)

    print(f"Annotated {image_path.name}, saved to {result_path}")

print(f"Annotations saved to {results_dir}")