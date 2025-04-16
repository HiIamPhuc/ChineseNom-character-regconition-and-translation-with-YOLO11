import os

def load_yolo_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.strip().split(' ', 1) for line in lines]

def build_vocab(FOLDER_PATH):
    words = set()

    for file in os.listdir(FOLDER_PATH):
        vocab_filepath = os.path.join(FOLDER_PATH, file)
        
        with open(vocab_filepath, 'r', encoding='utf-8') as f:
            yolo_data = f.readlines()

        words.update({line.strip().split()[0] for line in yolo_data})

    vocab = {word: idx for idx, word in enumerate(sorted(words))}

    return vocab

def convert_yolo_to_index(yolo_data, vocab):
    converted = []
    for line in yolo_data:
        word, bbox = line[0], line[1] if len(line) > 1 else ""
        index = vocab.get(word, -1)  # -1 if word not found in vocab
        converted.append(f"{index} {bbox}")
    return converted

def save_converted_yolo(file_path, converted_data):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(converted_data))

# Build vocab
INPUT_FOLDER = 'datasets/qn/label_yolo/'
OUTPUT_FOLDER = 'datasets/qn/label_yolo_indexed/'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

vocab = build_vocab(INPUT_FOLDER)

for file in os.listdir(INPUT_FOLDER):
    input_filepath = os.path.join(INPUT_FOLDER, file)
    output_filepath = os.path.join(OUTPUT_FOLDER, file)

    # Load data
    yolo_data = load_yolo_file(input_filepath)

    # Convert YOLO data
    converted_data = convert_yolo_to_index(yolo_data, vocab)

    # Save converted file
    save_converted_yolo(output_filepath, converted_data)

    print(f"Converted {input_filepath} and save to {output_filepath}")

with open(OUTPUT_FOLDER + "data.yaml", 'w', encoding='utf-8') as file:
    file.write(f"train: ../raw\nval: ../raw\nnc: {len(vocab)}\nnames: ['{', '.join(vocab.keys())}']")