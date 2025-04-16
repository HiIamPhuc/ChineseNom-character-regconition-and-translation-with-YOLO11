import os
import yaml

# def update_class_ids(dataset_dir, old_yaml_path, new_yaml_path):
#     """
#     Update class IDs in dataset based on new YAML mapping
    
#     Args:
#         dataset_dir: Directory containing .txt annotation files
#         old_yaml_path: Path to original YAML file
#         new_yaml_path: Path to new group YAML file
#     """
#     # Load YAML files
#     with open(old_yaml_path, 'r') as f:
#         old_yaml = yaml.safe_load(f)
#     with open(new_yaml_path, 'r') as f:
#         new_yaml = yaml.safe_load(f)
    
#     # Create mapping from old to new class IDs
#     old_classes = old_yaml['names']
#     new_classes = new_yaml['names']
#     class_mapping = {i: new_classes.index(cls) for i, cls in enumerate(old_classes) if cls in new_classes}
    
#     # Process each .txt file
#     for filename in os.listdir(dataset_dir):
#         if not filename.endswith('.txt'):
#             continue
            
#         filepath = os.path.join(dataset_dir, filename)
#         updated_lines = []
        
#         with open(filepath, 'r') as f:
#             for line in f:
#                 parts = line.strip().split()
#                 if not parts:
#                     continue
                    
#                 old_id = int(parts[0])
#                 if old_id in class_mapping:
#                     parts[0] = str(class_mapping[old_id])
#                     updated_lines.append(' '.join(parts))
                
#         # Write updated content
#         with open(filepath, 'w') as f:
#             f.write('\n'.join(updated_lines))


# update_class_ids('đánh thứ tự/aligned_tx_files copy', 'đánh thứ tự/dataset copy.yaml', 'đánh thứ tự/data.yaml')


def update_class_ids(dataset_dir, output_dir, yaml_path):
    """
    Update class IDs in dataset based on YAML mapping
    
    Args:
        dataset_dir: Directory containing .txt annotation files
        yaml_path: Path to group YAML file
    """
    # Load YAML files
    with open(yaml_path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)
    
    # Create mapping from old to new class IDs
    classes = yaml_data['names']
    class_mapping = {cls: classes.index(cls) for i, cls in enumerate(classes)}
    
    # Process each .txt file
    for filename in os.listdir(dataset_dir):
        if not filename.endswith('.txt'):
            continue
            
        filepath = os.path.join(dataset_dir, filename)
        output_filepath = os.path.join(output_dir, filename)
        updated_lines = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                    
                old_class = parts[0]
                if old_class in class_mapping:
                    parts[0] = str(class_mapping[old_class])
                    updated_lines.append(' '.join(parts))
                else:
                    print(f'Class "{old_class}" not found in YAML file')
                
        # Write updated content
        with open(output_filepath, 'w') as f:
            f.write('\n'.join(updated_lines))

INPUT_DIR = 'datasets/qn/label_yolo'
OUTPUT_DIR = 'datasets/train/label'
os.makedirs(OUTPUT_DIR, exist_ok=True)

update_class_ids(dataset_dir=INPUT_DIR, output_dir=OUTPUT_DIR, yaml_path='datasets/train/data.yaml')