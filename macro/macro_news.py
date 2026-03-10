import requests
import xml.etree.ElementTree as ET


def analizar_noticias():

    print("Analizando noticias macro...")

    try:

        url = "https://news.google.com/rss/search?q=stock+market+economy+war+inflation+oil&hl=en-US&gl=US&ceid=US:en"

        r = requests.get(url, timeout=10)

        root = ET.fromstring(r.content)

        noticias_lista = []
        riesgo = 0

        for item in root.findall(".//item")[:10]:

            titulo = item.find("title").text

            noticias_lista.append(titulo)

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

        if len(noticias_lista) == 0:

            texto = "Sin noticias relevantes"

        else:

            texto = "\n".join(["- " + n for n in noticias_lista])

        return texto, riesgo

    except Exception as e:

        print("Error obteniendo noticias:", e)

        return "Sin noticias relevantes", 0