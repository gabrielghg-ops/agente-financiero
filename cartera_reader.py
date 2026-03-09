import re
import pdfplumber


def limpiar_ticker(t):

    t = t.upper()

    # acciones argentinas
    argentinos = ["YPFD","GGAL","PAMP","LOMA","BYMA","CEPU"]

    if t in argentinos:
        return t + ".BA"

    if t == "BRKB":
        return "BRK-B"

    if t == "ETHA":
        return "ETH-USD"

    return t


def obtener_cartera():

    tickers = []

    with pdfplumber.open("cartera_balanz.pdf") as pdf:

        text = ""

        for page in pdf.pages:
            text += page.extract_text()

    palabras = re.findall(r"\b[A-Z]{2,6}\b", text)

    blacklist = [
        "BALANZ","HOUSE","FULL","INVESTMENT",
        "ARGENTINA","CUIT","TOTAL","USD"
    ]

    for p in palabras:

        if p in blacklist:
            continue

        ticker = limpiar_ticker(p)

        tickers.append(ticker)

    return list(set(tickers))