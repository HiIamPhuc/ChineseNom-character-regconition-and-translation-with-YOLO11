import json
import os

# Adjust the directories as needed
text_dir = 'datasets/nom/label_converted1'
label_filename = 'datasets/nom/Label.txt'
results_dir = 'datasets/nom/'
os.makedirs(results_dir, exist_ok=True)

# Merge all the text files in the directory into a single JSON file with a page number in each item
def merge_text_files(text_dir, output_file):
    """
    Merge all the text files in the directory into a single JSON file with a page number in each item.
    
    Args:
        text_dir: directory containing text files
        output_file: path to the output JSON file
    """
    data = []
    for file in os.listdir(text_dir):
        if file.endswith(".json"):
            page_number = int(file.split('.')[0])
            with open(os.path.join(text_dir, file), 'r') as f:
                text = json.loads(f.read())
            data.append({
                'page': page_number,
                'boxes': text
            })

    data = sorted(data, key=lambda x: -x['page'])
    
    with open(output_file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_OCR_data(label_filename: str, result_filename: str) -> list:
    '''
        Load OCR result from Label.txt file
    '''

    json_data = []
    with open(label_filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        
        for line in lines:
            splitted = line.split('\t')

            # Extract page index from images_label/82.jpeg
            pg_idx = int(splitted[0].split('/')[1].split('.')[0])

            # Get dict data
            data = json.loads(splitted[1])

            processed_data = []
            for d in data:
                if len(d["transcription"]) == 1:
                    processed_data.append(
                        {
                            "transcription": d["transcription"],
                            "bbox": d["points"]
                        }
                    )


            json_data.append(
                {
                    "page": pg_idx,
                    "text": processed_data
                }
            )

        json_data = sorted(json_data, key=lambda x: x["page"])

    with open(result_filename, "w", encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # merge_text_files(text_dir, os.path.join(results_dir, 'boxes1.json'))
    load_OCR_data(label_filename, os.path.join(results_dir, "boxes_OCRed.json"))