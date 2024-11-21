from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
from urllib.parse import urlparse, urljoin

def obtener_contenido_con_redireccion(url):
    # Configuración de Selenium con opciones para usar el navegador sin interfaz gráfica (headless)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecución sin abrir una ventana del navegador
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Ruta al driver de Chrome (asegúrate de tener el archivo adecuado para tu sistema operativo)
    service = Service("/path/to/chromedriver")  # Cambia esto con la ruta de tu chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Acceder a la URL inicial
        driver.get(url)
        
        # Esperar a que la página cargue completamente, si es necesario
        time.sleep(3)
        
        # Obtener el contenido HTML de la página
        contenido_html = driver.page_source

        # Comprobar si hay redirección JavaScript en la página
        if "window.location.href" in contenido_html:
            # Usar expresión regular para extraer la URL de redirección
            match = re.search(r'window.location.href="(.+?)"', contenido_html)
            if match:
                redirect_url = match.group(1)
                # Si la URL de redirección es relativa, construir la URL completa
                if redirect_url.startswith("/"):
                    redirect_url = urljoin(url, redirect_url)

                # Navegar a la URL de redirección
                driver.get(redirect_url)

                # Esperar a que la nueva página cargue completamente
                time.sleep(3)

                # Obtener el contenido HTML de la página de redirección
                contenido_html = driver.page_source
            else:
                return "Error: No se pudo encontrar la URL de redirección en el JavaScript."
        return contenido_html
    finally: 
        # Cerrar el navegador después de obtener el contenido
        driver.quit()

# URL de la página inicial
url_inicial = "https://playdede.eu/login"  # Cambiar a la URL de inicio de sesión que deseas usar

# Llamada a la función y mostrar el contenido de la página final
contenido_html = obtener_contenido_con_redireccion(url_inicial)
print(contenido_html)
