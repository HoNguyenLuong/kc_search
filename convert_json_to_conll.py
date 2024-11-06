import json

def json_to_conll(json_data, output_file):
    """Chuyển đổi dữ liệu từ JSON sang định dạng CoNLL và ghi vào file."""
    with open(output_file, "w") as f:
        for entry in json_data:
            sentence = entry["sentence"]
            for token in sentence:
                word = token["word"]
                label = token["label"]
                f.write(f"{word}\t{label}\n")
            f.write("\n")  # Ngăn cách các câu bằng dòng trống

if __name__ == '__main__':
    # Giả sử JSON đã được tạo trong quá trình xử lý và lưu tại path_to_file_json
    path_to_file_json = "vlsp2016/dev.csv.json"
    output_conll_file = "vlsp2016/output_dev.conll"
    
    # Đọc JSON
    with open(path_to_file_json, "r") as json_file:
        json_data = json.load(json_file)
    
    # Chuyển đổi và lưu dưới dạng CoNLL
    json_to_conll(json_data, output_conll_file)
    print(f"Data has been converted to CoNLL format and saved to {output_conll_file}")
