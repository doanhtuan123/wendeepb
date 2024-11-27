from flask import Flask, render_template, request
import os
import json

app = Flask(__name__)

# Đọc tất cả các file JSON trong thư mục 'data/'
def load_json_files_from_folder(folder_path):
    data_list = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                data_list.append(json.load(file))
    return data_list

# Đường dẫn đến thư mục chứa các file JSON
folder_path = '2024 24 10'  # Cập nhật lại đường dẫn này

@app.route('/')
def index():
    # Lấy dữ liệu từ các file JSON trong thư mục
    json_data = load_json_files_from_folder(folder_path)
    
    # Truyền dữ liệu vào template
    return render_template('index.html', data=json_data)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('filename', '')  # Lấy tên file từ query string
    json_data = load_json_files_from_folder(folder_path)
    
    # Lọc dữ liệu theo tên file chứa từ khóa
    results = []
    for data in json_data:
        # Lọc qua tất cả các phần tử trong 'attachments'
        for attachment in data.get('attachments', []):
            # Kiểm tra nếu tên file chứa từ khóa tìm kiếm
            if query.lower() in attachment.get('filename', '').lower():
                results.append({
                    'title': data.get('content', ''),
                    'link': data.get('link', ''),
                    'image': attachment.get('link', ''),
                    'source': data.get('source', {}).get('source_name', ''),
                    'filename': attachment.get('filename', '')
                })
    
    return render_template('search_results.html', results=results, query=query)

# Kiểm tra nếu là script chính
if __name__ == "__main__":
    app.run(debug=True)
