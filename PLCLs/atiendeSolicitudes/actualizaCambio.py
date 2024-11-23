import os

# Configura las rutas de las carpetas y archivos
solicitudes_folder = "solicitudes"
playlist_file = "testing_PLCLs.m3u"
historial_file = "historial.dat"

def add_file_to_playlist_and_update_historial():
    # Busca el primer archivo en la carpeta 'solicitudes'
    try:
        files = os.listdir(solicitudes_folder)
        if not files:
            print("No se encontraron archivos en la carpeta 'solicitudes'.")
            return

        # Obtiene el primer archivo
        first_file = files[0]
        file_path = os.path.join(solicitudes_folder, first_file)
        print(f"Se encontró el archivo '{first_file}' en la carpeta '{solicitudes_folder}'.")

        # Agrega el nombre del archivo al archivo 'testing_PLCLs.m3u'
        with open(playlist_file, "a") as playlist:
            playlist.write(first_file + "\n")
        print(f"El archivo '{first_file}' se ha añadido al playlist '{playlist_file}'.")

        # Agrega el nombre del archivo al historial
        with open(historial_file, "a") as historial:
            historial.write(first_file + "\n")
        print(f"El archivo '{first_file}' se ha registrado en el historial '{historial_file}'.")

        # Elimina el archivo de la carpeta 'solicitudes'
        os.remove(file_path)
        print(f"El archivo '{first_file}' ha sido eliminado de la carpeta '{solicitudes_folder}'.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Se produjo un error: {e}")

# Ejecuta la función
if __name__ == "__main__":
    add_file_to_playlist_and_update_historial()
