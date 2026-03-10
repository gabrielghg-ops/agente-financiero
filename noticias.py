import requests
import xml.etree.ElementTree as ET


def analizar_noticias():

    print("Analizando noticias relevantes...")

    url = "https://news.google.com/rss/search?q=stock+market+economy+war+inflation+oil&hl=en-US&gl=US&ceid=US:en"

    try:

        r = requests.get(url, timeout=10)

        root = ET.fromstring(r.content)

        noticias = []
        riesgo = 0

        for item in root.findall(".//item")[:10]:

            titulo = item.find("title").text

            noticias.append(titulo)

            t = titulo.lower()

            # Detectores de riesgo
            if "war" in t or "conflict" in t:
                riesgo += 15

            if "inflation" in t or "stagflation" in t:
                riesgo += 10

            if "recession" in t:
                riesgo += 20

            if "oil" in t and "surge" in t:
                riesgo += 10

        texto = "\n".join(["- " + n for n in noticias])

        if texto == "":
            texto = "No hay noticias relevantes"

        return texto, riesgo

    except Exception as e:

        print("Error noticias:", e)

        return "No se pudieron obtener noticias", 0