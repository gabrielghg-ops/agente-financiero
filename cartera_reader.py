import pdfplumber
import re


def limpiar_ticker(ticker):

    ticker = ticker.strip().upper()

    correcciones = {
        "BRK": "BRK-B",
        "BRKB": "BRK-B",
        "BRK.B": "BRK-B"
    }

    if ticker in correcciones:
        ticker = correcciones[ticker]

    ticker = ticker.replace(".", "-")

    return ticker


def obtener_cartera():

    tickers = set()

    with pdfplumber.open("cartera.pdf") as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            encontrados = re.findall(r'\b[A-Z]{2,5}\b', text)

            for t in encontrados:

                tickers.add(limpiar_ticker(t))

    return list(tickers)