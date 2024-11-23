from bs4 import BeautifulSoup
import requests

# Función para obtener el HTML de la página
def obtener_html(url):
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        return respuesta.text
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la página: {e}")
        return None

# Función para extraer el enlace del logo de un canal desde tvlogos.net
def obtener_logo(canal_nombre):
    # Reemplaza "1080p" y "720p", quita espacios, y construye la URL de búsqueda
    canal_nombre_limpio = canal_nombre.replace("1080p", "").replace("720p", "").replace(" ", "")
    url_busqueda = f"https://www.tvlogos.net/logos?search={canal_nombre_limpio}"
    print(f"Buscando logo de {canal_nombre} en {url_busqueda}")
    html = obtener_html(url_busqueda)

    if html:
        soup = BeautifulSoup(html, 'html.parser')
        # Busca el primer elemento con el atributo 'data-logo'
        logo_elemento = soup.find(attrs={"data-logo": True})
        if logo_elemento:
            return logo_elemento["data-logo"]  # Extrae el enlace del logo
    return None  # Retorna None si no encuentra el logo

# Función para extraer los elementos <strong> y sus enlaces acestream:// dentro del rango especificado
def extraer_datos(html):
    # Encuentra los índices de las secciones de inicio y fin
    start_index = html.find("ESP - TV")
    end_index = html.find("EUR / RU / NA / SA - TV")

    # Procesa solo el contenido entre estos índices si ambas secciones están presentes
    if start_index != -1 and end_index != -1 and start_index < end_index:
        html = html[start_index:end_index]

    soup = BeautifulSoup(html, 'html.parser')
    resultados = []

    # Encuentra todos los elementos <strong> y <a> relacionados dentro del rango
    for strong_tag in soup.find_all('strong'):
        texto = strong_tag.get_text()
        enlaces_acestream = []

        # Busca enlaces "acestream://" en los siguientes <a> del <strong>
        for sibling in strong_tag.find_next_siblings():
            if sibling.name == 'a' and sibling['href'].startswith('acestream://'):
                enlace_sin_prefijo = sibling['href'].replace("acestream://", "")
                enlaces_acestream.append(enlace_sin_prefijo)
            elif sibling.name == 'br':
                break  # Detenerse si llega a un <br> que indica fin de la lista

        # Agrega el texto y los enlaces en un array
        if enlaces_acestream:
            resultados.append([texto, enlaces_acestream])

    return resultados

# Función para generar el archivo M3U
def generar_m3u(datos, nombre_archivo="playlist.m3u"):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("#EXTM3U\n")  # Escribe la cabecera del archivo M3U
        ultimo_nombre = None  # Variable para guardar el último nombre usado

        for elemento in datos:
            nombre = elemento[0]
            enlaces = elemento[1]

            # Omitir elementos con corchetes o con las palabras "fem" o "golf"
            if ("[" in nombre and "]" in nombre) or "fem" in nombre.lower() or "golf" in nombre.lower():
                continue

            # Modificar el nombre si es "720p" basándose en el último nombre usado
            if "720p" in nombre:
                if ultimo_nombre:
                    nombre = ultimo_nombre.replace("1080p", "").strip() + " 720p"
            else:
                ultimo_nombre = nombre  # Actualizar el último nombre solo si no es una variante "720p"

            # Determinar el group-title basado en palabras clave en el nombre
            if "Liga" in nombre or "Campeones" in nombre:
                group_title = "Football"
            elif "F1" in nombre:
                group_title = "Formula 1"
            else:
                group_title = "Deportes"

            # Obtiene el logo desde tvlogos.net, omitiendo "1080p" y "720p"
            logo_url = obtener_logo(nombre) or "https://cdn.countryflags.com/thumbs/spain/flag-round-250.png"  # URL predeterminada si no se encuentra el logo

            # Escribe la entrada en el archivo M3U para cada enlace
            for enlace in enlaces:
                archivo.write(f'#EXTINF:-1 tvg-id="{nombre}" tvg-name="{nombre}" tvg-logo="{logo_url}" group-title="{group_title}", {nombre}\n')
                archivo.write(f'plugin://script.module.horus?action=play&id={enlace}\n')

# URL de ejemplo
url = "https://elplan94.github.io/hook/"  # Cambia esta URL por la página real
html = obtener_html(url)

if html:
    datos = extraer_datos(html)
    generar_m3u(datos, "playlist.m3u")
    print("Archivo M3U generado exitosamente. Gracias 12/11/2021")
