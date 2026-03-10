import os
import time
import requests

from cartera_reader import obtener_cartera
from oportunidades import analizar_activo
from noticias import analizar_noticias

from macro.macro_engine import analizar_macro_global
from ai.ai_market_brain import generar_estrategia
from ai.ai_portfolio_advisor import analizar_cartera


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
        print("Error telegram:", e)


def run_agent():

    print("===== AGENTE FINANCIERO V7 =====")

    report = "📊 REPORTE AGENTE FINANCIERO V7\n\n"

    # MACRO
    macro = analizar_macro_global()

    report += macro + "\n\n"

    # CARTERA
    cartera = obtener_cartera()

    report += "📈 CARTERA\n\n"

    datos_activos = []

    for ticker in cartera:

        print("Analizando", ticker)

        try:

            r = analizar_activo(ticker)

            if not r:
                continue

            datos_activos.append(r)

            report += f"""
{r.get('ticker')}
Precio: {r.get('price')}
Media50: {r.get('ma50')}
Señal: {r.get('signal')}
"""

        except Exception as e:

            print("Error activo:", e)

    # NOTICIAS
    noticias = analizar_noticias()

    report += "\n📰 NOTICIAS RELEVANTES\n"

    if noticias:
        report += str(noticias)
    else:
        report += "Sin noticias relevantes"

    # IA MERCADO
    estrategia = generar_estrategia(macro, noticias)

    report += "\n\n🧠 ESTRATEGIA IA\n"
    report += estrategia

    # IA CARTERA
    analisis_cartera = analizar_cartera(datos_activos)

    report += "\n\n📊 ANALISIS DE CARTERA\n"
    report += analisis_cartera

    enviar_telegram(report)

    print("Reporte enviado a Telegram")


if __name__ == "__main__":

    while True:

        run_agent()

        print("Esperando 6 horas...\n")

        time.sleep(21600)