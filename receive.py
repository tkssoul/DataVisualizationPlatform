from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/process-csv', methods=['POST'])
def process_csv():
    if 'csvFile' not in request.files:
        return jsonify({'error': '未找到 CSV 文件'}), 400
    file = request.files['csvFile']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    if file:
        # 保存 CSV 文件
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # 处理 CSV 文件，生成 NPY 文件
        # 这里需要根据具体需求实现处理逻辑
        # 假设生成了一些 NPY 文件，存放在 DOWNLOAD_FOLDER 中
        npy_files = ['metrics.npy', 'real_prediction.npy', 'pred.npy', 'true.npy']

        return jsonify({'files': npy_files,'csvFilename':file.filename})

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)