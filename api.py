from flask import Flask, jsonify, request
import math
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
#Tính độ dài tên miền
def calculate_length(text):
    if not text:
        return 0
    return len(text)
#Tính độ bất định ( entropy) của tên miền
def calculate_entropy(text):
    if not text:
        return 0
    entropy = 0
    for x in range(256):
        p_x = float(text.count(chr(x))) / len(text)
        if p_x > 0:
            entropy += -p_x * math.log(p_x, 2)
    return entropy
# Tải lại mô hình từ tệp H5
model = load_model('model.h5')
# Khởi tạo ứng dụng Flask
app = Flask(__name__)
# Định nghĩa một route và phương thức xử lý
@app.route('/api', methods=['POST'])
def api():
    entropy_train_vals = []
    length_train_vals = []
    threshold = 0.5
    # Lấy dữ liệu gửi từ client
    data = request.get_json()
    entropy_train_vals=calculate_entropy(data['domain'])
    length_train_vals=calculate_length(data['domain'])
    predict_data = pd.DataFrame({'entropy': entropy_train_vals, 'length': length_train_vals}, index=[0])
    predictions = model.predict(predict_data)
    if predictions > threshold:
        result="This may be DNS tunneling!"
        return jsonify(result)
    else:
        result="This may not be DNS tunneling!"
        return jsonify(result)
# Chạy ứng dụng Flask trên cổng 5000
if __name__ == 'api':
    app.run(port=5000)