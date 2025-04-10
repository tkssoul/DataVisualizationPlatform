from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
import os

app = Flask(__name__)
CORS(app)

PRED_DIR="downloads"

@app.route('/plot', methods=['GET'])
def get_npy_data():
    try:
        # 读取 .npy 文件
        file_path = os.path.join(PRED_DIR, 'pred.npy')
        data = np.load(file_path)
        # 将 numpy 数组转换为列表
        data_list = data.tolist()
        return jsonify(data_list[0])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,port=5001)