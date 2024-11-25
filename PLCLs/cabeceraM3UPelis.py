import requests
from bs4 import BeautifulSoup

def google_search(query):
    """Realiza una búsqueda en Google y retorna el primer enlace a IMDb."""
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Buscar todos los enlaces en el resultado
        for link in soup.find_all("a", href=True):
            href = link['href']

            # Validar si el enlace apunta a una página de IMDb
            if "imdb.com/title" in href and not href.startswith('/'):
                return href.split('&')[0]  # Retorna el enlace limpio

            # Manejar enlaces que están ofuscados por /url?q=
            if "/url?q=" in href:
                clean_link = href.split("/url?q=")[1].split("&")[0]
                if "imdb.com/title" in clean_link:
                    return clean_link

    return None

def extract_imdb_details(imdb_url):
    """Extrae el logo y el género desde una página de IMDb."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    response = requests.get(imdb_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Buscar el logo de la película
        logo = None
        for meta in soup.find_all("meta", attrs={"property": "og:image"}):
            logo = meta.get("content")
            if not logo:
                exit()
            break

        # Buscar géneros de la película
        prioritized_genres = ["Action", "Drama", "Adventure", "Romance", "Thriller"]
        genre_elements = soup.find_all("span", class_="ipc-chip__text")
        genres = [g.text.strip() for g in genre_elements]

        # Filtrar por géneros prioritarios
        selected_genre = next((genre for genre in genres if genre in prioritized_genres), None)

        return logo, selected_genre
    return None, None

def update_m3u_file(file_path, title, logo, genre):
    """Actualiza el archivo M3U, reemplazando una entrada existente en el mismo lugar."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Crear la nueva línea
    new_line = f'#EXTINF:-1 tvg-name="{title}" tvg-logo="{logo}" group-title="{genre}", {title}\n'

    # Buscar la línea existente
    updated = False
    for i, line in enumerate(lines):
        if f'tvg-name="{title}"' in line:
            # Reemplazar la línea existente
            lines[i] = new_line
            updated = True
            break

    # Si no se encontró, añadir al final
    if not updated:
        lines.append(new_line)

    # Escribir de nuevo el archivo
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)

def main():
    word = input("Introduce el título de la película: ")
    m3u_file_path = "../testing_PLCLs.m3u"

    print("Realizando búsqueda en Google...")
    imdb_url = google_search(f"{word} imdb")
    if not imdb_url:
        print("No se encontró un enlace válido a IMDb.")
        return

    print("Extrayendo detalles desde IMDb...")
    logo, genre = extract_imdb_details(imdb_url)
    if not logo or not genre:
        print("No se pudieron extraer los detalles de la película.")
        return

    print(f"Detalles extraídos:\nTítulo: {word}\nLogo: {logo}\nGénero: {genre}")
    update_m3u_file(m3u_file_path, word, logo, genre)
    print(f"Se añadió o actualizó la película '{word}' en el archivo '{m3u_file_path}'.")

if __name__ == "__main__":
    main()
