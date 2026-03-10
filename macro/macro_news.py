import requests


def resumen_noticias():

    print("Analizando noticias macro...")

    texto = ""

    try:

        url = "https://newsapi.org/v2/everything?q=economy OR inflation OR fed OR argentina&language=en&pageSize=5&sortBy=publishedAt&apiKey=demo"

        r = requests.get(url)

        data = r.json()

        if "articles" in data:

            for n in data["articles"][:3]:

                titulo = n.get("title","")

                texto += f"- {titulo}\n"

    except Exception as e:

        print("Error noticias:", e)

        texto = "No se pudieron obtener noticias"

    if texto == "":
        texto = "Sin noticias relevantes"

    return texto