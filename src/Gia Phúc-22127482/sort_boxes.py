import numpy as np
import os

def sort_boxes(boxes, tolerance=0.01):
    """
    Sort boxes from left to right, and top to bottom within each column.
    
    Args:
        boxes: numpy array of shape (N, 5) with each row as [class_id, x_center, y_center, width, height]
        num_columns: estimated number of columns in the image
        tolerance: maximum horizontal distance to consider boxes in the same column
        
    Returns:
        sorted_boxes: numpy array of boxes sorted by column (left to right) and position (top to bottom)
    """
    boxes = np.array(boxes)
    
    # Step 1: Estimate column positions
    x_centers = boxes[:, 1]
    x_centers_sorted = np.sort(x_centers)
    
    # Find natural column breaks
    columns = []
    current_column = [x_centers_sorted[0]]
    
    for x in x_centers_sorted[1:]:
        if x - current_column[-1] > tolerance:
            columns.append(np.mean(current_column))
            current_column = [x]
        else:
            current_column.append(x)
    columns.append(np.mean(current_column))
    
    # Step 2: Assign boxes to columns
    sorted_boxes = []
    for col_center in reversed(columns):
        col_boxes = boxes[np.abs(boxes[:, 1] - col_center) < tolerance]
        col_boxes = sorted(col_boxes, key=lambda x: x[2])
        sorted_boxes.extend(col_boxes)
    
    return np.array(sorted_boxes)

# Read boxes from file
def read_boxes(file_path):
    """
    Read boxes from a text file.
    
    Args:
        file_path: path to the text file containing boxes, each line in the format "class_id x_center y_center width height"
        
    Returns:
        boxes: list of boxes, each box in the format [class_id, x_center, y_center, width, height]
    """
    boxes = []
    with open(file_path, 'r') as f:
        for line in f:
            class_id, x_center, y_center, width, height = map(float, line.strip().split())
            boxes.append([class_id, x_center, y_center, width, height])
    return boxes

# Read multiple box files, sort boxes, and save to multiple new files:
def sort_boxes_in_files(input_files, output_files, tolerance=0.01):
    """
    Read boxes from multiple files, sort boxes, and save to multiple new files.
    
    Args:
        input_files: list of paths to input files containing boxes
        output_files: list of paths to output files to save sorted boxes
        num_columns: estimated number of columns in the image
        tolerance: maximum horizontal distance to consider boxes in the same column
    """
    for input_file, output_file in zip(input_files, output_files):
        boxes = read_boxes(input_file)

        processed_boxes = sort_boxes(boxes, tolerance=tolerance)
        
        with open(output_file, 'w') as f:
            for box in processed_boxes:
                f.write(f"{int(box[0])} {box[1]:.6f} {box[2]:.6f} {box[3]:.6f} {box[4]:.6f}\n")

if __name__ == "__main__":
    INPUT_FOLDER = "datasets/nom/label1"
    OUTPUT_FOLDER = "datasets/nom/label_sorted"
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    input_files = [os.path.join(INPUT_FOLDER, file) for file in os.listdir(INPUT_FOLDER) if file.endswith(".txt")]
    output_files = [os.path.join(OUTPUT_FOLDER, file) for file in os.listdir(INPUT_FOLDER) if file.endswith(".txt")]

    sort_boxes_in_files(input_files, output_files, tolerance=20)