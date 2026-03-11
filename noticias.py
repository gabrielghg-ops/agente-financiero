import re
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus
import os

HEADERS = {"User-Agent": "Mozilla/5.0"}

CRYPTOPANIC_TOKEN = os.environ.get("CRYPTOPANIC_TOKEN", None)

TOPICS = [
    "Iran war markets",
    "oil inflation stocks",
    "global recession markets",
    "stagflation economy",
]

IPROFESIONAL_RSS = [
    "https://www.iprofesional.com/rss/economia",
    "https://www.iprofesional.com/rss/finanzas",
]


def traducir(texto):

    try:

        url = "https://translate.googleapis.com/translate_a/single"

        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": "es",
            "dt": "t",
            "q": texto
        }

        r = requests.get(url, params=params, timeout=10)

        data = r.json()

        return data[0][0][0]

    except:
        return texto


def limpiar_xml(text):

    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", text)

    text = re.sub(
        r"&(?!amp;|lt;|gt;|apos;|quot;|#\d+;|#x[0-9A-Fa-f]+;)",
        "&amp;",
        text
    )

    return text


def rss_google(query):

    url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-US&gl=US&ceid=US:en"

    try:

        r = requests.get(url, headers=HEADERS, timeout=10)

        xml = limpiar_xml(r.text)

        root = ET.fromstring(xml)

        noticias = []

        for item in root.findall(".//item"):

            t = item.findtext("title", "").strip()

            if t:
                noticias.append(t)

            if len(noticias) >= 3:
                break

        return noticias

    except:
        return []


def rss_iprofesional(url):

    try:

        r = requests.get(url, headers=HEADERS, timeout=10)

        xml = limpiar_xml(r.text)

        root = ET.fromstring(xml)

        noticias = []

        for item in root.findall(".//item"):

            t = item.findtext("title", "").strip()

            if t:
                noticias.append(t)

            if len(noticias) >= 3:
                break

        return noticias

    except:
        return []


def cryptopanic():

    if not CRYPTOPANIC_TOKEN:
        return []

    try:

        url = "https://cryptopanic.com/api/v1/posts/"

        params = {
            "auth_token": CRYPTOPANIC_TOKEN,
            "public": "true"
        }

        r = requests.get(url, params=params, timeout=10)

        data = r.json()

        noticias = []

        for n in data["results"][:5]:
            noticias.append(n["title"])

        return noticias

    except:
        return []


def riesgo_noticias(lista):

    riesgo = 0

    palabras = {
        "war": 25,
        "iran": 25,
        "conflict": 20,
        "oil": 15,
        "inflation": 15,
        "stagflation": 20,
        "recession": 20,
        "crisis": 20,
        "meltdown": 25,
    }

    texto = " ".join(lista).lower()

    for p, score in palabras.items():

        if p in texto:
            riesgo += score

    return min(riesgo, 100)


def analizar_noticias():

    print("Analizando noticias relevantes...")

    noticias = []

    # GOOGLE NEWS

    for t in TOPICS:
        noticias += rss_google(t)

    # IPROFESIONAL

    for url in IPROFESIONAL_RSS:
        noticias += rss_iprofesional(url)

    # CRYPTO

    noticias += cryptopanic()

    # DEDUP

    únicas = []
    seen = set()

    for n in noticias:

        key = n.lower()

        if key not in seen:

            únicas.append(n)

            seen.add(key)

    únicas = únicas[:10]

    # TRADUCIR

    traducidas = []

    for n in únicas:

        t = traducir(n)

        traducidas.append(f"- {t}")

    texto = "\n".join(traducidas)

    riesgo = riesgo_noticias(únicas)

    return texto, riesgo