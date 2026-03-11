import os
import time
import requests

from cartera_reader import obtener_cartera
from oportunidades import analizar_activo
from noticias import analizar_noticias

from macro.macro_engine import analizar_macro_global
from macro.macro_risk_model import calcular_risk_score

from ai.ai_portfolio import analizar_cartera_ia
from ai.ai_strategy import generar_estrategia_ia
from ai.ai_market_regime import detectar_regimen

from radar.global_radar import radar_global

from alerts.market_alerts import revisar_alertas


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


# -------------------
# TELEGRAM
# -------------------

def enviar_telegram(msg):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    partes = [msg[i:i+4000] for i in range(0, len(msg), 4000)]

    for parte in partes:

        try:

            requests.post(url, data={
                "chat_id": CHAT_ID,
                "text": parte
            })

        except Exception as e:

            print("Error telegram:", e)

# -------------------
# AGENTE PRINCIPAL
# -------------------

def run_agent():

    print("===== AGENTE FINANCIERO V11 INSTITUTIONAL =====")

    report = "📊 AGENTE FINANCIERO V11\n\n"

    # -------------------
    # MACRO
    # -------------------

    print("Analizando entorno macroeconómico...")

    try:

        macro = analizar_macro_global()

        if macro:
            report += str(macro) + "\n\n"
        else:
            report += "Error obteniendo datos macro\n\n"

    except Exception as e:

        print("Error macro:", e)

        macro = "Error macro"
        report += "Error analizando macro\n\n"

    # -------------------
    # NOTICIAS
    # -------------------

    print("Analizando noticias...")

    try:

        noticias_texto, riesgo_noticias = analizar_noticias()

    except Exception as e:

        print("Error noticias:", e)

        noticias_texto = "No se pudieron obtener noticias"
        riesgo_noticias = 0

    report += "📰 CONTEXTO GLOBAL\n"
    report += str(noticias_texto) + "\n\n"

    # -------------------
    # RISK MODEL
    # -------------------

    print("Calculando riesgo global...")

    try:

        risk_score = calcular_risk_score(riesgo_noticias)

        regimen = detectar_regimen(risk_score)

        report += "🌍 RIESGO GLOBAL\n\n"
        report += f"Risk Score: {risk_score}/100\n"
        report += f"Modo de mercado: {regimen}\n\n"

    except Exception as e:

        print("Error risk model:", e)

        report += "No se pudo calcular riesgo global\n\n"

    # -------------------
    # RADAR GLOBAL
    # -------------------

    print("Analizando radar global...")

    try:

        radar = radar_global()

        report += "🌎 RADAR GLOBAL\n\n"
        report += radar + "\n"

    except Exception as e:

        print("Error radar:", e)

    # -------------------
    # CARTERA
    # -------------------

    cartera = obtener_cartera()

    report += "\n📈 CARTERA\n\n"

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

    # -------------------
    # IA CARTERA
    # -------------------

    print("IA analizando cartera...")

    try:

        analisis_cartera = analizar_cartera_ia(resultados)

        report += "\n🧠 IA CARTERA\n"
        report += str(analisis_cartera)

    except Exception as e:

        print("Error IA cartera:", e)

    # -------------------
    # IA ESTRATEGIA
    # -------------------

    print("Generando estrategia IA...")

    try:

        estrategia = generar_estrategia_ia(macro, resultados, noticias_texto)

        report += "\n\n📊 ESTRATEGIA IA\n"
        report += str(estrategia)

    except Exception as e:

        print("Error estrategia IA:", e)

    # -------------------
    # ALERTAS
    # -------------------

    try:

        alertas = revisar_alertas()

        if alertas:

            report += "\n\n🚨 ALERTAS\n"
            report += str(alertas)

    except Exception as e:

        print("Error alertas:", e)

    # -------------------
    # TELEGRAM
    # -------------------

    enviar_telegram(report)

    print("Reporte enviado")


# -------------------
# LOOP
# -------------------

if __name__ == "__main__":

    while True:

        run_agent()

        print("Esperando 6 horas...")

        time.sleep(21600)