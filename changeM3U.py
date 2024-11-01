import requests

def obtener_html(url):
    try:
        # Realiza la solicitud GET a la URL
        respuesta = requests.get(url)
        respuesta.raise_for_status()  # Verifica si hubo un error en la solicitud
        
        # Devuelve el contenido HTML de la página
        return respuesta.text
    
    except requests.exceptions.RequestException as e:
        # En caso de error, muestra el mensaje de error
        print(f"Error al obtener la página: {e}")
        return None

# Ejemplo de uso
url = "https://www.ejemplo.com"
contenido_html = obtener_html(url)

if contenido_html:
    print(contenido_html)
