import requests
import xml.etree.ElementTree as ET


def analizar_noticias():

    print("Analizando noticias relevantes...")

    try:

        url = "https://news.google.com/rss/search?q=stock+market+economy+war+inflation&hl=en-US&gl=US&ceid=US:en"

        r = requests.get(url, timeout=10)

        root = ET.fromstring(r.content)

        noticias = ""

        for item in root.findall(".//item")[:5]:

            titulo = item.find("title").text

            noticias += "- " + titulo + "\n"

        if noticias == "":
            noticias = "No hay noticias relevantes\n"

        print("Noticias revisadas")

        return noticias

    except Exception as e:

        print("Error noticias:", e)

        return "No se pudieron obtener noticias\n"