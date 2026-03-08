import pandas as pd
import pdfplumber
import re

def leer_excel_santander(path):

    df = pd.read_excel(path)

    tickers = []

    for col in df.columns:
        for val in df[col].astype(str):
            if re.match(r'^[A-Z]{2,6}$', val):
                tickers.append(val)

    return list(set(tickers))


def leer_pdf_balanz(path):

    tickers = []

    with pdfplumber.open(path) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            matches = re.findall(r'\b[A-Z]{2,5}\b', text)

            tickers.extend(matches)

    return list(set(tickers))


def obtener_cartera():

    santander = leer_excel_santander("cartera_santander.xlsx")

    balanz = leer_pdf_balanz("cartera_balanz.pdf")

    return list(set(santander + balanz))