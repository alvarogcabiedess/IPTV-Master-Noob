import requests

# URL de destino
url = "https://playdede.eu/ajax.php"

# Los datos del formulario (como en el cuerpo de la solicitud original)
data = {
    "_method": "getPlayer",
    "id": "9369581",  # El ID del reproductor, que parece estar basado en el HTML
    "tmdb_id": "845781",  # ID de TMDB
    "s": "0",  # Temporada
    "e": "0",  # Episodio
    "width": "1920",  # Ancho
    "height": "1080"  # Alto
}

# Los encabezados de la solicitud
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en,es;q=0.9,es-ES;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryeVQDwB6gBKTnVB8r",
    "Origin": "https://playdede.eu",
    "Referer": "https://playdede.eu/pelicula/red_one_845781",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
}

# Las cookies que podrían ser necesarias
cookies = {
    "PLAYDEDE_SESSION": "80b05a77a4e8bf39ac91e2b743de33f8",
    "_ga": "GA1.1.1955179996.1728075669",
    "utoken": "yUXPkPauOo9i1JpHzSYiVDidU3fGEXgs",
    "cf_clearance": "K2sr3xUS83s9ljJzULlfpCSmxlSdi91QWcJrMOkkjFg-1731104818-1.2.1.1-VDZDqMjieGkku2QqTVbOFpZWalJbu8Mb85a5WVzqnLskHTvtA35lGbHNa2Rx77uTfxLq7gpMyOGd1ns3Atun0392J9BirDBG7Khur8hKVPiOFl46Gjcw3BXVoJy1d2BtTnvARZHM6.SskHLyvW.SBUZZl.uLdFcUcVAeuhwA8vQDKfIBBt8jGvgu3YhYUsKu5yILVFmiGyGdsro.i39qTyf9gQT0rW6VAfsJGiITFrx9zSKhN.Nmd2rJ5lP_pQF9HU_AsZJwHwoSmZ05eoHVTP_D7ZPSrE9yfcxc9Ap5KDTEuQrJ30RYqJRYygGKE1FCoQaeP0y1t.L3uIQHKGokdQ8NavndXKY13FhHH.qyrW8ZBDG_4BsOlr6Nq5BjL1y9jDuI89wMMk1LhRf2So0Crg"
}

# Realizamos la solicitud POST
response = requests.post(url, data=data, headers=headers, cookies=cookies)

# Verificamos el código de estado
if response.status_code == 526:
    print("Error 526: Problema con el certificado SSL del servidor.")
elif response.status_code == 200:
    print("Solicitud exitosa")
    # Imprimimos el contenido de la respuesta
    print(response.text)
else:
    print(f"Error en la solicitud: {response.status_code}")
    print("Encabezados:", response.headers)
    print("Cuerpo de la respuesta:", response.text)
    print("Esto va a la rama nueva 2 distitna de main")
