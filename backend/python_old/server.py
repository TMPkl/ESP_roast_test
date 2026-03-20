from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/data')
def data():
    return jsonify({
        'input_air_temp': random.uniform(0,200),
        'time': random.uniform(0,100)
    })

@app.route('/report', methods=['POST'])
def report():
    print("Received report:", request.json)
    return {"status": 'success'}

app.run(host="0.0.0.0", port=5555)