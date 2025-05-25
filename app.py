from flask import Flask, request, jsonify
import serial
import json
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/read-weight')
def read_weight():
    try:
        ser = serial.Serial('COM3', 9600, timeout=1)  # Change COM3 if needed
        raw = ser.readline().decode().strip()
        weight = float(raw)
        ser.close()
        return jsonify({'weight': weight})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save', methods=['POST'])
def save_data():
    try:
        data = request.json
        data['timestamp'] = datetime.now().isoformat()
        with open('records.json', 'a') as f:
            f.write(json.dumps(data) + '\n')
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
