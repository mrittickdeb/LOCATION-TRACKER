cat <<EOF > app.py
from flask import Flask, request, send_file, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
locations = []

if os.path.exists('locations.log'):
    with open('locations.log', 'r') as f:
        for line in f:
            try:
                locations.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue

@app.route('/')
def index():
    return send_file('location.html')

@app.route('/location', methods=['POST'])
def location():
    data = request.get_json()
    data['timestamp'] = datetime.now().isoformat()
    locations.append(data)
    with open('locations.log', 'a') as f:
        f.write(json.dumps(data) + '\n')
    return jsonify({'status': 'received'})

@app.route('/view')
def view():
    return jsonify(locations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF
