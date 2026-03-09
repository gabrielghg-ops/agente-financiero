import pdfplumber
import re


def limpiar_ticker(ticker):

    ticker = ticker.strip().upper()

    # Correcciones comunes
    correcciones = {
        "BRK": "BRK-B",
        "BRKB": "BRK-B",
        "BRK.B": "BRK-B"
    }

    if ticker in correcciones:
        ticker = correcciones[ticker]

    ticker = ticker.replace(".", "-")

    # Acciones argentinas (Yahoo necesita .BA)
    argentinas = [
        "BYMA",
        "YPFD",
        "PAMP",
        "CEPU",
        "GGAL",
        "LOMA",
        "VIST"
    ]

    if ticker in argentinas:
        ticker = ticker + ".BA"

    # Criptos
    criptos = {
        "BTC": "BTC-USD",
        "ETH": "ETH-USD"
    }

    if ticker in criptos:
        ticker = criptos[ticker]

    return ticker


def obtener_cartera():

    tickers = set()

    palabras_ignorar = [
        "USD",
        "ARS",
        "TOTAL",
        "SALDO",
        "VALOR",
        "CANTIDAD"
    ]

    try:

        with pdfplumber.open("cartera.pdf") as pdf:

            for page in pdf.pages:

                text = page.extract_text()

                encontrados = re.findall(r'\b[A-Z]{2,6}\b', text)

                for t in encontrados:

                    if t in palabras_ignorar:
                        continue

                    ticker = limpiar_ticker(t)

                    tickers.add(ticker)

    except Exception as e:

        print(f"Error leyendo cartera: {e}")

        return []

    return sorted(list(tickers))