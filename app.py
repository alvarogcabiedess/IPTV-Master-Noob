from flask import Flask, send_file, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Devuelve el archivo index.html desde el directorio actual
    return send_file('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        subprocess.run(["python3", "changeM3U.py"], check=True)
        return jsonify({"success": True, "message": "Archivo M3U generado exitosamente."})
    except subprocess.CalledProcessError:
        return jsonify({"success": False, "message": "Error al ejecutar el script."}), 500

if __name__ == '__main__':
    app.run(debug=True)
