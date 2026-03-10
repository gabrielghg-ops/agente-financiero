import requests


def analizar_noticias():

    print("Analizando noticias relevantes...")

    try:

        url = "https://newsapi.org/v2/top-headlines?category=business&pageSize=5&apiKey=demo"

        r = requests.get(url, timeout=10)

        data = r.json()

        noticias = ""

        if "articles" not in data:
            return "No se pudieron obtener noticias\n"

        for art in data["articles"][:5]:

            titulo = art.get("title", "")

            if titulo:
                noticias += "- " + titulo + "\n"

        if noticias == "":
            noticias = "No hay noticias relevantes\n"

        print("Noticias revisadas")

        return noticias

    except Exception as e:

        print("Error obteniendo noticias:", e)

        return "Error obteniendo noticias\n"