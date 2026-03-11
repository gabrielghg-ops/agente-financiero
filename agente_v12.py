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
from radar.sector_rotation import sector_rotation

from alerts.market_alerts import revisar_alertas

from macro.crash_detector import detect_crash_risk
from macro.macro_forecast import macro_forecast

from scanner.global_scanner import scan_assets
from scanner.opportunity_ranker import rank_opportunities


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


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


def run_agent():

    print("===== AGENTE FINANCIERO V12 INSTITUTIONAL =====")

    report = "AGENTE FINANCIERO V12\n\n"

    # -------------------
    # MACRO
    # -------------------

    print("Analizando entorno macroeconómico...")

    try:

        macro = analizar_macro_global()

        if isinstance(macro, dict):

            report += "🌍 MACRO GLOBAL\n\n"

            report += f"SPY: {macro.get('SPY','N/D')}\n"
            report += f"VIX: {macro.get('VIX','N/D')}\n"
            report += f"DXY: {macro.get('DXY','N/D')}\n"
            report += f"ORO: {macro.get('ORO','N/D')}\n"
            report += f"PETROLEO: {macro.get('PETROLEO','N/D')}\n\n"

            if macro.get("correlaciones"):

                report += "🔗 Correlaciones:\n"
                report += f"{macro['correlaciones']}\n\n"

        else:
            report += "Error obteniendo datos macro\n\n"

    except Exception as e:

        print("Error macro:", e)

        macro = {}
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
    report += f"{noticias_texto}\n\n"

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
    # CRASH DETECTOR
    # -------------------

    print("Analizando riesgo de crash...")

    try:

        crash = detect_crash_risk()

        report += "⚠️ CRASH RISK\n\n"
        report += f"Score: {crash['crash_score']}\n"
        report += f"Nivel: {crash['crash_risk']}\n\n"

    except Exception as e:

        print("Error crash detector:", e)

    # -------------------
    # MACRO FORECAST
    # -------------------

    print("Calculando forecast macro...")

    try:

        forecast = macro_forecast()

        report += "🔮 MACRO FORECAST\n\n"
        report += f"Risk On: {forecast['risk_on']}%\n"
        report += f"Neutral: {forecast['neutral']}%\n"
        report += f"Risk Off: {forecast['risk_off']}%\n\n"

    except Exception as e:

        print("Error forecast:", e)

    # -------------------
    # RADAR GLOBAL
    # -------------------

    print("Analizando radar global...")

    try:

        radar = radar_global()

        report += "🌎 RADAR GLOBAL\n\n"
        report += str(radar) + "\n\n"

    except Exception as e:

        print("Error radar:", e)

    # -------------------
    # ROTACION SECTORIAL
    # -------------------

    print("Analizando rotación sectorial...")

    try:

        sectors = sector_rotation()

        report += "🏭 ROTACION SECTORIAL\n\n"

        for s in sectors[:5]:

            report += f"{s[0]} : {s[1]}%\n"

        report += "\n"

    except Exception as e:

        print("Error rotación:", e)

    # -------------------
    # SCANNER GLOBAL
    # -------------------

    print("Buscando oportunidades globales...")

    try:

        scanner = scan_assets()

        ranking = rank_opportunities(scanner)

        report += "🚀 OPORTUNIDADES GLOBALES\n\n"

        for r in ranking:

            report += f"{r['ticker']} | Score {r['score']} | {r['nivel']}\n"

        report += "\n"

    except Exception as e:

        print("Error scanner:", e)

    # -------------------
    # CARTERA
    # -------------------

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

    enviar_telegram(report)

    print("Reporte enviado")


if __name__ == "__main__":

    while True:

        run_agent()

        print("Esperando 6 horas...")

        time.sleep(21600)