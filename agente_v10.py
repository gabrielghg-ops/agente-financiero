import os
import time
import requests

from cartera_reader import obtener_cartera
from oportunidades import analizar_activo
from noticias import analizar_noticias

from macro.macro_engine import analizar_macro_global
from ai.ai_portfolio import analizar_cartera_ia
from ai.ai_strategy import generar_estrategia_ia
from alerts.market_alerts import revisar_alertas


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def enviar_telegram(msg):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg[:4000]
        })

    except Exception as e:

        print("Error telegram:", e)


def run_agent():

    print("===== AGENTE FINANCIERO V10 =====")

    report = "📊 AGENTE FINANCIERO V10\n\n"

    print("Analizando entorno macroeconómico...")

    macro = analizar_macro_global()

    report += macro + "\n\n"

    cartera = obtener_cartera()

    report += "📈 CARTERA\n\n"

    resultados = []

    for ticker in cartera:

        print("Analizando", ticker)

        try:

            r = analizar_activo(ticker)

            if r:

                resultados.append(r)

                report += f"""
{r['ticker']}
Precio: {r['price']}
MA50: {r['ma50']}
Señal: {r['signal']}
"""

        except Exception as e:

            print("Error activo:", ticker, e)

    print("IA analizando cartera...")

    analisis_cartera = analizar_cartera_ia(resultados)

    report += "\n🧠 IA CARTERA\n"
    report += analisis_cartera

    print("Analizando noticias...")

    noticias = analizar_noticias()

    report += "\n📰 NOTICIAS\n"
    report += noticias

    print("Generando estrategia IA...")

    estrategia = generar_estrategia_ia(macro, resultados, noticias)

    report += "\n📊 ESTRATEGIA IA\n"
    report += estrategia

    alertas = revisar_alertas()

    if alertas:

        report += "\n🚨 ALERTAS\n"
        report += alertas

    enviar_telegram(report)

    print("Reporte enviado")


if __name__ == "__main__":

    while True:

        run_agent()

        print("Esperando 6 horas...")

        time.sleep(21600)