import os
import requests
import time

from cartera_reader import obtener_cartera
from oportunidades import analizar_activo
from macro.macro_engine import analizar_macro_global
from macro.macro_ai_report import generar_informe_ia
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

    cartera_texto = ""

    # MACRO

    macro = analizar_macro_global()

    report += f"{macro}\n\n"

    report += "📈 CARTERA ANALIZADA\n"

    for ticker in cartera:

        print(f"Analizando {ticker}")

        try:

            r = analizar_activo(ticker)

            if r is None:
                continue

            if isinstance(r, bool):

                texto = f"{ticker} señal {'alcista' if r else 'bajista'}"

                report += texto + "\n"
                cartera_texto += texto + "\n"

            elif isinstance(r, dict):

                texto = f"""
{r.get('ticker',ticker)}
Precio: {r.get('price','?')}
Media50: {r.get('ma50','?')}
Señal: {r.get('signal','?')}
"""

                report += texto
                cartera_texto += texto

        except Exception as e:

            print(f"Error analizando {ticker}: {e}")

            continue

    # NOTICIAS

    try:

        noticias = analizar_noticias()

        report += "\n📰 NOTICIAS RELEVANTES\n"

        if noticias:
            report += str(noticias)
        else:
            report += "Sin noticias relevantes"

    except Exception as e:

        report += "\nError obteniendo noticias"

    # INFORME IA

    print("Generando informe estratégico con IA...")

    informe_ia = generar_informe_ia(macro, cartera_texto)

    report += "\n\n🧠 INFORME ESTRATÉGICO IA\n"
    report += informe_ia

    enviar_telegram(report)

    print("Reporte enviado a Telegram")


if __name__ == "__main__":

    while True:

        run_agent()

        print("Esperando 6 horas...\n")

        time.sleep(21600)