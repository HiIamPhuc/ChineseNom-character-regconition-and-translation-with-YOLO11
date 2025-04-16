*Đề tài của nhóm em là đề tài số 13 về Chinese OCR using Google Doc’s  API, tuy nhiên về sau thầy Điền nhận thấy đề tài này không khả thi khi train Documment AI và không có ngữ liệu thô để làm nên thầy quyết định chuyển đề tài của nhóm thành OCR chữ Nôm với YOLO ạ.
Cấu trúc nội dung các thư mục của nhóm chúng em như sau:
- Report.pdf :Báo cáo các kết quả tìm hiểu và thực hiện đồ án cuối kì của nhóm.
- Folder "dataset":
                    + Folder "valid" và "train" chứa:
                                                   ++ Folder "labels": chứa các file txt gồm thông tin của các box được nhận diện thông qua mô hình.
                                                   ++ Folder "images": chứa ảnh được dùng để nhận diện.
                    => các folder "valid" và "train" chứa các dataset để huấn luyện mô hình và đánh giá trong quá trình huấn luyện.
                    + File "data.yaml" chứa các nhãn ánh xạ đầu ra của mô hình với các nhãn thực tế trong tập dữ liệu.
-Folder "scr":
              + File "train.ipynb" để train mô hình và test thử mô hình trên một ảnh chữ nôm bất kì.
              + Các folder "Ngọc Trang-22127421", "Gia Phúc-22127482", "Đức Anh-22127020", "Hoàng Linh-22127233" chứa các code mà mỗi bạn đã dùng trong suốt quá trình gán nhãn cho bộ ngữ liệu riêng của mình (do mỗi bộ ngữ liệu có tính chất khác nhau nên cách xử lí của các bạn cũng khác nhau như chúng em đã trình bày trong báo cáo).
              + Folder "train_results":
                        ++ "Weights": chứa các model "best.py" được train với 1647 ảnh và "last.py" được train với 3294 ảnh ( mỗi ảnh có từ một hoặc hai trang sách Nôm).
                        ++ Các hình ảnh và file "results.csv" trong folder như train_batch0.jpg, labels.jpg.... là các file minh họa cho kết quả đạt được.