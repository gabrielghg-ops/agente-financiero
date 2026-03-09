import os
import requests
import schedule
import time
import yfinance as yf

from cartera_reader import obtener_cartera
from oportunidades import analizar_activo
from macro import analizar_macro
from noticias import analizar_noticias

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def enviar_telegram(msg):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


# FILTRO DE TICKERS INVALIDOS
def ticker_valido(ticker):

    try:
        df = yf.download(ticker, period="5d", progress=False)

        if df.empty:
            print(f"{ticker} sin datos, se ignora")
            return False

        return True

    except:
        print(f"{ticker} error, se ignora")
        return False


def run_agent():

    cartera = obtener_cartera()

    report = "📊 REPORTE FINANCIERO DIARIO\n\n"

    macro = analizar_macro()

    report += f"Macro:\n{macro}\n\n"

    report += "Cartera:\n"

    for ticker in cartera:

        if not ticker_valido(ticker):
            continue

        try:

            r = analizar_activo(ticker)

            if r is None:
                continue

            report += f"""
{r['ticker']}
Precio: {r['price']}
RSI: {r['rsi']}
Señal: {r['signal']}
"""

        except Exception as e:

            print(f"Error analizando {ticker}: {e}")
            continue

    noticias = analizar_noticias()

    report += "\nNoticias relevantes:\n"
    report += noticias

    enviar_telegram(report)


run_agent()

schedule.every().day.at("09:00").do(run_agent)

while True:
    schedule.run_pending()
    time.sleep(60)