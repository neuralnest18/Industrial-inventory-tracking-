from flask import Flask, request, jsonify
from flask_cors import CORS
import serial
import csv
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow frontend requests

# Adjust this port to your weight machine's COM port
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600

@app.route('/')
def home():
    return "Welcome to the Saqib Industry backend API!"

@app.route('/read-weight', methods=['GET'])
def read_weight():
    try:
        # Open the serial port to read the weight from the connected machine
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        raw = ser.readline().decode('utf-8').strip()  # Read the raw data and decode
        ser.close()

        weight = float(raw)  # Convert to float for the weight value
        return jsonify({"weight": weight})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/save', methods=['POST'])
def save_data():
    data = request.json
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    record = [
        now,
        data.get('twist', ''),  # Get the twist value from the request
        data.get('date', ''),   # Get the date
        data.get('grade', ''),  # Get the grade (fixed value "AA")
        data.get('cones', ''),  # Get the cones value
        data.get('gw', ''),     # Get the gross weight (G.W.)
        data.get('nw', ''),     # Get the net weight (N.W.)
        data.get('lotNo', ''),  # Get the lot number
        data.get('barcode', '') # Get the barcode
    ]

    # Open the CSV file and append the data
    with open('records.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(record)

    return jsonify({"status": "saved"})


# Ensure the app runs with debug mode enabled and accessible on all interfaces
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
