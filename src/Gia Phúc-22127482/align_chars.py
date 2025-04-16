import json
import re
import numpy as np
import pandas as pd

QN_SinoNom_dic = 'QuocNgu_SinoNom_Dic.xlsx'
SinoNom_similar_dic = 'SinoNom_similar_Dic.xlsx'

def load_QN_SinoNom_dic(filename : str) -> dict:
    '''
        Load QN-SinoNom dictionary form excel file
    '''

    # Save data from the excel file to a data frame
    df = pd.read_excel(filename)

    dict = {}

    for idx, row in df.iterrows():
        qn_word = row['QuocNgu']
        sinonom_char = row['SinoNom']

        # If the dict doesn't have this QN word inside, create a new key
        if qn_word not in dict:
            dict[qn_word] = []

        dict[qn_word].append(sinonom_char)

    return dict

def load_SinoNom_similar_dic(filename : str) -> dict:
    '''
        Load SinoNom-similar-character dictionary form excel file
    '''

    # Save data from the excel file to a data frame
    df = pd.read_excel(filename)

    dict = {}

    for idx, row in df.iterrows():
        input_char = row['Input Character']
        sim_chars = row['Top 20 Similar Characters']

        # Process the string
        sim_chars = sim_chars.strip("['']")
        sim_chars = sim_chars.split("', '")

        dict[input_char] = []
        dict[input_char].append(input_char)
        dict[input_char].extend(sim_chars)

    return dict

qn_nom_dic = load_QN_SinoNom_dic(QN_SinoNom_dic)
nom_sim_dic = load_SinoNom_similar_dic(SinoNom_similar_dic)

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def process_qn_stc(sentence):
    # Sử dụng regex để chỉ giữ lại các chữ cái và khoảng trắng
    filtered_sentence = re.sub(r'[^a-zA-ZÀ-ỹ\s]', ' ', sentence)

    # Loại bỏ các khoảng trắng dư thừa
    filtered_sentence = re.sub(r'\s+', ' ', filtered_sentence).strip()

    # Chuyển thành danh sách từ, viết thường
    filtered_words = [word.lower() for word in filtered_sentence.split()]

    return filtered_words

def process_qn_text(sentences):
    words = []
    for sentence in sentences:
        words.extend(process_qn_stc(sentence))

    return words

def compare_qn_nom(qn_word, nom_char):
    S1 = set(nom_sim_dic.get(nom_char, []))
    S2 = set(qn_nom_dic.get(qn_word, []))

    intersection = S1.intersection(S2)

    return len(intersection)

def levenshtein_alignment_np(qn_words, nom_chars):
    # Kích thước chuỗi quốc ngữ và Nôm
    m, n = len(qn_words), len(nom_chars)
    
    # Tạo ma trận khoảng cách với NumPy
    dp = np.zeros((m + 1, n + 1), dtype=np.float32)
    
    # Khởi tạo giá trị ban đầu cho hàng và cột
    dp[:, 0] = np.arange(m + 1)  # Chi phí xóa
    dp[0, :] = np.arange(n + 1)  # Chi phí chèn
    
    # Hàm tính chi phí thay thế sử dụng compare_qn_nom
    def compute_substitution_cost(i, j):
        qn_word = qn_words[i - 1]
        nom_char = nom_chars[j - 1]
        return 1 - compare_qn_nom(qn_word, nom_char)  # Chi phí thấp nếu có giao
    
    # Điền ma trận DP
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            substitution_cost = compute_substitution_cost(i, j)
            dp[i, j] = min(
                dp[i - 1, j] + 1,               # Xóa
                dp[i, j - 1] + 1,               # Chèn
                dp[i - 1, j - 1] + substitution_cost  # Thay thế
            )
    
    # Backtrace để tìm sự dóng hàng
    i, j = m, n
    aligned_qn, aligned_nom = [], []
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i, j] == dp[i - 1, j - 1] + compute_substitution_cost(i, j):
            aligned_qn.append(i - 1)
            aligned_nom.append(j - 1)
            i -= 1
            j -= 1
        elif i > 0 and dp[i, j] == dp[i - 1, j] + 1:
            aligned_qn.append(i - 1)
            aligned_nom.append(np.nan)  # Không có ký tự Nôm tương ứng
            i -= 1
        else:  # j > 0
            aligned_qn.append(np.nan)
            aligned_nom.append(j - 1)  # Không có ký tự quốc ngữ tương ứng
            j -= 1
    
    # Kết quả là hai danh sách dóng hàng ngược, cần đảo lại
    return list(reversed(aligned_qn)), list(reversed(aligned_nom))


NOM_DATA_FILE = 'datasets/nom/char_rec_yolo.json'
QN_DATA_FILE = 'datasets/qn/extracted_corrected.json'
OUTPUT_FILE = 'char_aligned.json'

nom_data = load_json(NOM_DATA_FILE)
qn_data = load_json(QN_DATA_FILE)

if len(nom_data) != len(qn_data):
    raise Exception('The 2 documents are not of the same length.')

result = []

for (nom_item, qn_item) in zip(nom_data, qn_data):
    page = nom_item['page']
    nom_chars = nom_item['boxes']
    qn_words = np.array(process_qn_text(qn_item['text']))

    # Extract the list of transcription characters from nom_chars
    nom_transcriptions = np.array([box['transcription'] for box in nom_chars])

    # Align using only the transcriptions
    aligned_qn, aligned_nom = levenshtein_alignment_np(qn_words, nom_transcriptions)

    # Create aligned pairs with both transcription and bbox information
    aligned_pairs = [
        {
            'qn': qn_words[qn_idx] if not np.isnan(qn_idx) else "",
            'nom': nom_chars[int(nom_idx)]['transcription'] if not np.isnan(nom_idx) else "",
            'bbox': nom_chars[int(nom_idx)]['bbox'] if not np.isnan(nom_idx) else None
        }
        for qn_idx, nom_idx in zip(aligned_qn, aligned_nom)
    ]

    page_dict = {
        'page': page,
        'aligned': aligned_pairs
    }

    result.append(page_dict)

with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
    json.dump(result, output_file, indent=4, ensure_ascii=False)