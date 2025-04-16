import json
import re
import numpy as np

INPUT_FILE = 'result.json'
TRUE_INPUT_FILE = 'true_result.txt'
OUTPUT_FILE = 'result.txt'

def extract_predictions():
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)['predictions']

    ext_data = []
    for item in data:
        # ext_data.append(
        #     {
        #         'x': item['x'],
        #         'y': item['y'],
        #         'class': item['class'],
        #     }
        # )
        ext_data.append([item['class'], float(item['x']), float(item['y'])])

    indexed_data = [[idx, item[1], item[2]] for idx, item in enumerate(ext_data)]

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
        # print(x_centers_sorted[1:])
        
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
        
        # return np.array(sorted_boxes)
        return sorted_boxes

    sorted_boxes = sort_boxes(indexed_data, tolerance=20)
    result = []
    # for sorted_column in sorted_boxes:
    #     column = []
    #     for item in sorted_column:
    #         column.append(ext_data[int(item[0])][0])
    #     result.append(column)
    for word in sorted_boxes:
        result.append(ext_data[int(word[0])][0])

    return result

def extract_orginal():
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    def remove_accents(input_str):
        s = ''
        for c in input_str:
            if c in s1:
                s += s0[s1.index(c)]
            else:
                s += c
        return s

    def process_qn_stc(sentence):
        # Sử dụng regex để chỉ giữ lại các chữ cái và khoảng trắng
        filtered_sentence = re.sub(r'[^a-zA-ZÀ-ỹ\s]', ' ', sentence)

        # Loại bỏ các khoảng trắng dư thừa
        filtered_sentence = re.sub(r'\s+', ' ', filtered_sentence).strip()

        # Chuyển thành danh sách từ, viết thường
        filtered_words = [remove_accents(word.lower()) for word in filtered_sentence.split()]

        return filtered_words

    def process_qn_text(sentences):
        words = []
        for sentence in sentences:
            words.extend(process_qn_stc(sentence))

        return words

    with open(TRUE_INPUT_FILE, 'r', encoding='utf-8') as f:
        true_result = process_qn_text(f.readlines())

    return true_result

def levenshtein_alignment_np(org_words, pred_words):
    m, n = len(org_words), len(pred_words)
    
    # Tạo ma trận khoảng cách với NumPy
    dp = np.zeros((m + 1, n + 1), dtype=np.float32)
    
    # Khởi tạo giá trị ban đầu cho hàng và cột
    dp[:, 0] = np.arange(m + 1)  # Chi phí xóa
    dp[0, :] = np.arange(n + 1)  # Chi phí chèn
    
    # Điền ma trận DP
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if org_words[i - 1] == pred_words[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])     
    
    # Backtrace để tìm sự dóng hàng
    i, j = m, n
    aligned_org, aligned_pred = [], []
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and (org_words[i - 1] == pred_words[j - 1] or dp[i][j] == dp[i - 1][j - 1] + 1):
            aligned_org.append(i - 1)
            aligned_pred.append(j - 1)
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or dp[i][j] == dp[i - 1][j] + 1):
            aligned_org.append(i - 1)
            aligned_pred.append(np.nan)
            i -= 1
        else:  # j > 0
            aligned_org.append(np.nan)
            aligned_pred.append(j - 1)
            j -= 1
    
    return list(reversed(aligned_org)), list(reversed(aligned_pred))

org_words = extract_orginal()
pred_words = extract_predictions()

aligned_org, aligned_pred = levenshtein_alignment_np(org_words, pred_words)
result = [
    {
        'org': org_words[ord_idx] if not np.isnan(ord_idx) else '',
        'pred': pred_words[pred_idx] if not np.isnan(pred_idx) else '',
    }
    for ord_idx, pred_idx in zip(aligned_org, aligned_pred)
]

total_len = len(result)
correct_len = sum([1 for item in result if item['org'] == item['pred']])

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for item in result:
        f.write(f'{item["org"]} - {item["pred"]}\n')

    f.write(f'Total: {correct_len}/{total_len}')