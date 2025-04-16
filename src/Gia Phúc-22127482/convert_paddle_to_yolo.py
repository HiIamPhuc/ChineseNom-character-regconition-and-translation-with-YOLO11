import json 
import os

IMG_FOLDER = 'datasets/nom/raw/'

def load_json(src_filename):
    with open(src_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Convert from paddle box format to yolo box format:
# paddle box format: [[2482, 246], [2557, 246], [2557, 345], [2482, 345]]
# yolo box format: [x_center, y_center, width, height]
def convert_paddleBox_to_yoloBox(paddleBox, img_width, img_height):
    x1, y1 = paddleBox[0]
    x2, y2 = paddleBox[1]
    x3, y3 = paddleBox[2]
    x4, y4 = paddleBox[3]
    x_center = (x1 + x2 + x3 + x4) / 4 / img_width
    y_center = (y1 + y2 + y3 + y4) / 4 / img_height
    width = (x2 - x1) / img_width
    height = (y3 - y2) / img_height
    
    return x_center, y_center, width, height

def get_img_size(img_filename):
    from PIL import Image
    img = Image.open(img_filename)
    return img.size

def convert_boxes(data, result_filename):
    result = []

    for item in data:
        result_item = item

        img_filename = os.path.join(IMG_FOLDER, str(item['page']) + '.jpeg')
        img_width, img_height = get_img_size(img_filename)
        
        for idx, box in enumerate(result_item['boxes']):
            x_center, y_center, width, height = convert_paddleBox_to_yoloBox(box['bbox'], img_width, img_height)

            result_item['boxes'][idx]['bbox'] = f'{x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}'

        print(f'Converted {item["page"]}.jpeg')
        result.append(result_item)

        result = sorted(result, key=lambda x: -x['page'])

    with open(result_filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    src_filename = 'datasets/nom/char_rec_paddle.json'
    result_filename = 'datasets/nom/char_rec_yolo.json'

    data = load_json(src_filename)
    convert_boxes(data, result_filename)