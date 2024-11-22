import hashlib
import itertools
from concurrent.futures import ProcessPoolExecutor

# Configuración y valores conocidos
BASE_URL = "https://24q0stgk4bnr.cdn-jupiter.com/hls2/01/03238/hg9yueae5he0_x/master.m3u8"
KNOWN_TOKENS = [
    "f4b7a8b7e3d445679acb0d7d9e1234567890abcdef1234567890abcdef123456",  # Token caso 1
]
KNOWN_VALUES = [
    {"s": 1732279134, "e": 129600},  # Valores del caso 1
]
CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789"  # Conjunto de caracteres de la clave
MAX_KEY_LENGTH = 10  # Longitud máxima de la clave
NUM_WORKERS = 20  # Número de procesos paralelos

# Función para generar un token con la clave secreta
def generar_token(secret_key, s, e, ruta):
    datos = f"{secret_key}{s}{e}{ruta}"
    return hashlib.sha256(datos.encode()).hexdigest()

# Función para probar un rango específico de claves
def probar_claves(start_index, step):
    for length in range(1, MAX_KEY_LENGTH + 1):
        print(f"Probando claves de longitud {length}...")
        for key in itertools.islice(itertools.product(CHARSET, repeat=length), start_index, None, step):
            secret_key = ''.join(key)
            for i, token in enumerate(KNOWN_TOKENS):
                valores = KNOWN_VALUES[i]
                s, e = valores["s"], valores["e"]
                print(f"Probando clave: {secret_key}")
                if generar_token(secret_key, s, e, BASE_URL) == token:
                    return secret_key
    return None

# Función principal para búsqueda paralela
def buscar_clave_paralela():
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        # Dividir la carga entre NUM_WORKERS procesos
        futures = [executor.submit(probar_claves, i, NUM_WORKERS) for i in range(NUM_WORKERS)]
        for future in futures:
            result = future.result()
            if result:  # Si un proceso encuentra la clave, terminamos
                return result
    return None

if __name__ == "__main__":
    print(f"Buscando clave con {NUM_WORKERS} procesos...")
    clave = buscar_clave_paralela()
    if clave:
        print(f"Clave secreta encontrada: {clave}")
    else:
        print("No se encontró la clave secreta.")
