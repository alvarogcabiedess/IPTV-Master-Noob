import asyncio
import aiohttp
import string
import random

async def generate_combinations(length=60, num_combinations=100000):
    """
    Genera un número limitado de combinaciones posibles de letras y números de longitud especificada.
    
    Args:
        length (int): Longitud de la cadena generada.
        num_combinations (int): Número de combinaciones a generar.
    
    Returns:
        list: Lista de combinaciones generadas.
    """
    characters = string.ascii_lowercase + string.digits
    combinations = [''.join(random.choices(characters, k=length)) for _ in range(num_combinations)]
    return combinations

async def check_valid_domains(base_url, start, end, port=444, path="index.html", session=None):
    """
    Verifica qué subdominios en un rango no devuelven error al acceder.
    
    Args:
        base_url (str): La URL base sin los números.
        start (int): El inicio del rango de números.
        end (int): El final del rango de números.
        port (int): El puerto a utilizar en las URLs.
        path (str): El path al archivo en las URLs.
        session (aiohttp.ClientSession): Sesión de aiohttp para realizar solicitudes.

    Returns:
        list: Una lista de URLs válidas (código HTTP 200).
    """
    valid_urls = []
    tasks = []

    for i in range(start, end + 1):
        domain = base_url.replace("XX", str(i))
        url = f"{domain}:{port}/{path}"
        tasks.append(check_domain(url, valid_urls, session))

    # Esperamos a que todas las solicitudes se completen
    await asyncio.gather(*tasks)
    return valid_urls

async def check_domain(url, valid_urls, session):
    """
    Realiza una solicitud HTTP para verificar si el dominio es válido.

    Args:
        url (str): La URL a verificar.
        valid_urls (list): Lista para almacenar los dominios válidos.
        session (aiohttp.ClientSession): La sesión de aiohttp.
    """
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                print(f"\n✔️ Dominio válido: {url}", end="")
                valid_urls.append(url)
            else:
                print(f"❌", end="")
    except asyncio.TimeoutError:
        # Ignorar el error de Timeout y pasar al siguiente
        print(f"⏳", end="")
    except aiohttp.ClientError:
        # Manejar otros errores de cliente
        print(f"❌", end="")

async def is_video_url_valid(video_url, session):
    """
    Verifica si una URL de video es válida y no contiene mensajes de error como "Wrong IP" o "Expired".
    
    Args:
        video_url (str): La URL del video a verificar.
        session (aiohttp.ClientSession): La sesión de aiohttp.

    Returns:
        bool: True si es un video válido, False en caso contrario.
    """
    try:
        async with session.get(video_url, timeout=100) as response:
            if response.status == 200:
                content = await response.text()
                if "wrong ip" in content.lower() or "expired" in content.lower():
                    print(f"⚠️", end="")
                    return False
                return True
            print(f"❌", end="")
            return False
    except asyncio.TimeoutError:
        # Ignorar el error de Timeout y pasar al siguiente
        print(f"⏳", end="")
        return False
    except aiohttp.ClientError as e:
        # Manejar otros errores de cliente
        print(f"❌", end="")
        return False

async def check_video_urls(valid_domains, attempts_per_domain=100000, session=None):
    """
    Realiza un barrido por una cantidad limitada de combinaciones de URLs con una cadena de longitud 60
    seguida de `/v.mp4`.
    
    Args:
        valid_domains (list): Lista de dominios válidos.
        attempts_per_domain (int): Número de intentos por dominio.
        session (aiohttp.ClientSession): La sesión de aiohttp.
        
    Returns:
        dict: Un diccionario con las URLs válidas encontradas por dominio.
    """
    valid_video_urls = {}
    total_attempts = 0

    for domain in valid_domains:
        print(f"\n🔍 Buscando en: {domain}")
        found_urls = []

        # Generar un número limitado de combinaciones
        combinations = await generate_combinations(num_combinations=attempts_per_domain)

        # Generar nuevas tareas para cada combinación, evitando reutilizar tareas ya esperadas
        tasks = []  # Se crea un nuevo contenedor para las tareas en cada dominio
        for combination in combinations:
            video_url = f"{domain}/" + combination + "/v.mp4"
            tasks.append(check_video_url(video_url, found_urls, session))

            total_attempts += 1  # Incrementar el contador de intentos
            
            # Imprimir una marca cada 1000 intentos, mostrando el último enlace procesado
            if total_attempts % 100000 == 0:
                print(f"🔄 Marcador: Se han realizado {total_attempts} búsquedas. Último enlace procesado: {video_url}")

        # Esperar a que se completen todas las tareas
        await asyncio.gather(*tasks)
        if found_urls:
            valid_video_urls[domain] = found_urls
    
    return valid_video_urls

async def check_video_url(video_url, found_urls, session):
    """
    Verifica si una URL de video es válida y la agrega a la lista de encontrados.

    Args:
        video_url (str): La URL del video a verificar.
        found_urls (list): La lista de URLs válidas encontradas.
        session (aiohttp.ClientSession): La sesión de aiohttp.
    """
    if await is_video_url_valid(video_url, session):
        print(f"✔️ Video válido encontrado: {video_url}")
        found_urls.append(video_url)

async def main():
    # Configuración inicial
    base_url = "https://sXX.gamovideo.com"
    start = 19
    end = 35
    attempts_per_domain = 100000  # Número de intentos por dominio

    # Crear una sesión de aiohttp
    async with aiohttp.ClientSession() as session:
        # Paso 1: Buscar dominios válidos
        print("🔎 Buscando dominios válidos...")
        valid_domains = await check_valid_domains(base_url, start, end, session=session)

        # Paso 2: Buscar videos válidos en cada dominio
        if valid_domains:
            print("\n🎯 Dominios válidos encontrados. Buscando videos...")
            valid_video_urls = await check_video_urls(valid_domains, attempts_per_domain, session=session)

            # Mostrar resultados
            print("\n🎥 Videos válidos encontrados:")
            for domain, urls in valid_video_urls.items():
                print(f"\nDominio: {domain}")
                for url in urls:
                    print(url)
        else:
            print("\n❌ No se encontraron dominios válidos.")

# Ejecutar el script asíncrono
if __name__ == "__main__":
    asyncio.run(main())
