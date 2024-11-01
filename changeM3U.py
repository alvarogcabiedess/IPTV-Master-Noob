from bs4 import BeautifulSoup
import requests

# Función para extraer el HTML de la página
def obtener_html(url):
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        return respuesta.text
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la página: {e}")
        return None

# Función para extraer los elementos <strong> y sus enlaces acestream://
def extraer_datos(html):
    soup = BeautifulSoup(html, 'html.parser')
    resultados = []

    # Encuentra todos los elementos <strong> y <a> relacionados
    for strong_tag in soup.find_all('strong'):
        texto = strong_tag.get_text()
        enlaces_acestream = []

        # Busca enlaces "acestream://" en los siguientes <a> del <strong>
        for sibling in strong_tag.find_next_siblings():
            if sibling.name == 'a' and sibling['href'].startswith('acestream://'):
                enlaces_acestream.append(sibling['href'])
            elif sibling.name == 'br':
                break  # Detenerse si llega a un <br> que indica fin de la lista

        # Agrega el texto y los enlaces en un array
        if enlaces_acestream:
            resultados.append([texto, enlaces_acestream])

    return resultados

# URL de ejemplo (cámbiala por la URL real)
url = "https://example.com"  # Cambia esta URL por la página real
html = obtener_html(url)

if html:
    datos = extraer_datos(html)
    print(datos)
    print("Hola, aquí tienes los datos extraídos:")
    for elemento in datos:
        print("Título:", elemento[0])
        print(elemento)