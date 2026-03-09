import os
import time
import requests
import schedule

from cartera_reader import obtener_cartera
from oportunidades import analizar_activo
from macro import analizar_macro
from noticias import analizar_noticias


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def enviar_telegram(msg):

    url=f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url,data={
        "chat_id":CHAT_ID,
        "text":msg
    })


def run_agent():

    cartera = obtener_cartera()

    report = "📊 REPORTE FINANCIERO\n\n"

    # macro
    macro = analizar_macro()
    report += f"Macro:\n{macro}\n\n"

    report += "Cartera:\n"

    for ticker in cartera:

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

    noticias = analizar_noticias()

    report += "\nNoticias:\n"
    report += noticias

    enviar_telegram(report)


run_agent()

schedule.every().day.at("09:00").do(run_agent)

while True:

    schedule.run_pending()
    time.sleep(60)