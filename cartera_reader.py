import pandas as pd
import pdfplumber
import re

# lista básica de palabras que NO son tickers
PALABRAS_INVALIDAS = {
"BONOS","FCI","MEP","USD","ARS","DEL","INC","VOTO",
"TOMO","REGS","REP","ARG","ADS"
}

def limpiar_tickers(lista):

    tickers = []

    for t in lista:

        t = t.strip().upper()

        if len(t) > 5:
            continue

        if t in PALABRAS_INVALIDAS:
            continue

        if not re.match(r'^[A-Z]{2,5}$', t):
            continue

        tickers.append(t)

    return list(set(tickers))


def leer_excel_santander(path):

    df = pd.read_excel(path)

    posibles = []

    for col in df.columns:
        for val in df[col].astype(str):
            posibles.append(val)

    return limpiar_tickers(posibles)


def leer_pdf_balanz(path):

    posibles = []

    with pdfplumber.open(path) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            matches = re.findall(r'\b[A-Z]{2,5}\b', text)

            posibles.extend(matches)

    return limpiar_tickers(posibles)


def obtener_cartera():

    santander = leer_excel_santander("cartera_santander.xlsx")

    balanz = leer_pdf_balanz("cartera_balanz.pdf")

    return list(set(santander + balanz))