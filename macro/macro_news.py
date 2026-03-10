import requests

NEWS_API = "https://newsapi.org/v2/everything"


def resumen_noticias():

    print("Analizando noticias macro...")

    try:

        temas = [
            "global economy",
            "inflation",
            "interest rates",
            "Argentina economy",
            "emerging markets",
            "oil market",
            "china economy",
            "US economy"
        ]

        noticias_resumen = ""

        for tema in temas:

            url = f"https://newsapi.org/v2/everything?q={tema}&language=en&sortBy=publishedAt&pageSize=3"

            r = requests.get(url)

            data = r.json()

            if "articles" not in data:
                continue

            for art in data["articles"]:

                titulo = art["title"]

                noticias_resumen += f"- {titulo}\n"

        if noticias_resumen == "":
            return "Sin noticias relevantes."

        return noticias_resumen

    except Exception as e:

        print("Error leyendo noticias:", e)

        return