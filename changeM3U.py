from flask import Flask, render_template, request, jsonify
import requests
import html

app = Flask(__name__)

def obtener_html(url):
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        return respuesta.text
    except requests.exceptions.RequestException as e:
        return f"Error al obtener la página: {e}"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/obtener_html', methods=['POST'])
def obtener_html_ruta():
    url = request.json.get("url")
    contenido_html = obtener_html(url)
    contenido_html_escapado = html.escape(contenido_html)
    return jsonify({"html": contenido_html_escapado})

if __name__ == "__main__":
    app.run(debug=True)
