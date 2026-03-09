import os
import requests
import time

from cartera_reader import obtener_cartera
from oportunidades import analizar_activo
from macro import analizar_macro
from noticias import analizar_noticias


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def enviar_telegram(msg):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:

        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg
        })

    except Exception as e:

        print("Error enviando telegram:", e)


def run_agent():

    print("===== AGENTE FINANCIERO V5 =====")

    cartera = obtener_cartera()

    report = "📊 REPORTE DEL AGENTE\n\n"

    # MACRO
    macro = analizar_macro()
    report += f"Macro:\n{macro}\n\n"

    report += "Cartera:\n"

    for ticker in cartera:

        print(f"Analizando {ticker}")

        try:

            r = analizar_activo(ticker)

            if r is None:
                continue

            report += f"""
{ticker}
Precio: {r['price']}
Media50: {r['ma50']}
Señal: {r['signal']}
"""

        except Exception as e:

            print(f"Error analizando {ticker}: {e}")

            continue

    noticias = analizar_noticias()

report += "\nNoticias relevantes:\n"

if noticias:
    report += noticias
else:
    report += "Sin noticias relevantes"

    enviar_telegram(report)

    print("Reporte enviado a Telegram")


if __name__ == "__main__":

    while True:

        run_agent()

        print("Esperando 6 horas...\n")

        time.sleep(21600)