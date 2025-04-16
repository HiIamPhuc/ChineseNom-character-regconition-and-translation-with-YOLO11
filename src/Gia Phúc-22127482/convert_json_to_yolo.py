import json
import os

def load_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

def create_word_index(data):
    """
    Tạo một từ điển ánh xạ từ tiếng Việt (từ file JSON) sang các chỉ số duy nhất.
    """
    word_set = set()

    # Thu thập tất cả các từ
    for item in data:
        for char in item['aligned']:
            if char['qn']:  # Bỏ qua các từ rỗng
                word_set.add(char['qn'])

    # # Gán chỉ số cho mỗi từ
    # word_index = {word: idx for idx, word in enumerate(sorted(word_set))}

    # return word_index

    return word_set

def convert_page(output_folder, json_data):
    '''
        Convert an item in the json file to a list of strings (YOLO format)
    '''
    vocab = []

    page = json_data['page']
    output_filename = os.path.join(output_folder, str(page) + ".txt")

    with open(output_filename, 'w', encoding='utf-8') as file:
        for char in json_data['aligned']:
            if char['bbox'] != None and char['qn'] != "":
                line = char['qn'] + " " + char['bbox']
                file.write(line + "\n")

                vocab.append(char['qn'])

    return vocab

def convert_json_to_yolo(json_file, output_folder):
    vocab = set()
    data = load_json(json_file)

    for item in data:
        words = convert_page(output_folder, item)
        vocab.update(words)

    return vocab


if __name__ == "__main__":
    ALIGNED_DATA_FILE = 'char_aligned.json'
    OUTPUT_FOLDER = 'datasets/qn/label_yolo/'
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    vocab = convert_json_to_yolo(ALIGNED_DATA_FILE, OUTPUT_FOLDER)

    with open('datasets/qn/vocab.txt', 'w', encoding='utf-8') as file:
        for word in vocab:
            file.write(word + "\n")