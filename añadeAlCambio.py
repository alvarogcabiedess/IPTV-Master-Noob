import os

# Configura las rutas de las carpetas y archivos
solicitudes_folder = "solicitudes"
playlist_file = "testing_PLCLs.m3u"

def add_file_to_playlist():
    # Busca el primer archivo en la carpeta 'solicitudes'
    try:
        files = os.listdir(solicitudes_folder)
        if not files:
            print("No se encontraron archivos en la carpeta 'solicitudes'.")
            return

        # Obtiene el primer archivo
        first_file = files[0]
        print(f"Se encontró el archivo '{first_file}' en la carpeta '{solicitudes_folder}'.")

        # Agrega el nombre del archivo al archivo 'testing_PLCLs.m3u'
        with open(playlist_file, "a") as playlist:
            playlist.write(first_file + "\n")
        
        print(f"El archivo '{first_file}' se ha añadido al playlist '{playlist_file}'.")

    except FileNotFoundError:
        print(f"La carpeta '{solicitudes_folder}' o el archivo '{playlist_file}' no existen.")
    except Exception as e:
        print(f"Se produjo un error: {e}")

# Ejecuta la función
if __name__ == "__main__":
    add_file_to_playlist()

