import requests
from datetime import datetime

API_KEY = "8a47643c5651489bbcc163f48e813016"


def obtener_noticias_globales():

    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"category=business&language=en&pageSize=5&apiKey={API_KEY}"
    )

    try:

        response = requests.get(url)
        data = response.json()

        noticias = []

        if data["status"] == "ok":

            for articulo in data["articles"]:

                titulo = articulo.get("title", "")
                fuente = articulo.get("source", {}).get("name", "")

                noticias.append(f"{titulo} ({fuente})")

        return noticias

    except Exception as e:

        return [f"Error obteniendo noticias globales: {e}"]


def obtener_noticias_argentina():

    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"country=ar&category=business&pageSize=5&apiKey={API_KEY}"
    )

    try:

        response = requests.get(url)
        data = response.json()

        noticias = []

        if data["status"] == "ok":

            for articulo in data["articles"]:

                titulo = articulo.get("title", "")
                fuente = articulo.get("source", {}).get("name", "")

                noticias.append(f"{titulo} ({fuente})")

        return noticias

    except Exception as e:

        return [f"Error obteniendo noticias Argentina: {e}"]


def resumen_noticias():

    globales = obtener_noticias_globales()
    argentina = obtener_noticias_argentina()

    fecha = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    reporte = f"""
NOTICIAS ECONÓMICAS

Actualizado: {fecha}

Contexto Global:
"""

    for noticia in globales[:3]:
        reporte += f"- {noticia}\n"

    reporte += "\nContexto Argentina:\n"

    for noticia in argentina[:3]:
        reporte += f"- {noticia}\n"

    return reporte