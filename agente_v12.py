import os
import time
import requests

from cartera_reader import obtener_cartera
from oportunidades import analizar_activo
from noticias import analizar_noticias

from macro.macro_engine import analizar_macro_global
from macro.macro_risk_model import calcular_risk_score
from macro.market_theme_detector import detectar_market_theme
from macro.crash_detector import detect_crash_risk
from macro.macro_forecast import macro_forecast

from ai.ai_portfolio import analizar_cartera_ia
from ai.ai_strategy import generar_estrategia_ia
from ai.ai_market_regime import detectar_regimen
from ai.market_report import generar_informe_final

from radar.global_radar import radar_global
from radar.sector_rotation import sector_rotation

from scanner.global_scanner import scan_assets
from scanner.opportunity_ranker import rank_opportunities

from alerts.market_alerts import revisar_alertas


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    partes = [msg[i:i + 4000] for i in range(0, len(msg), 4000)]

    for parte in partes:
        try:
            requests.post(
                url,
                data={
                    "chat_id": CHAT_ID,
                    "text": parte
                },
                timeout=20
            )
        except Exception as e:
            print("Error telegram:", e)


def run_agent():
    print("===== AGENTE FINANCIERO V12 INSTITUTIONAL =====")

    report = "AGENTE FINANCIERO V12\n\n"

    # valores por defecto para evitar variables sin definir
    macro = {}
    noticias_texto = "No se pudieron obtener noticias"
    riesgo_noticias = 0
    risk_score = 50
    regimen = "NEUTRAL"
    crash = {"crash_score": 0, "crash_risk": "SIN DATOS"}
    forecast = {"risk_on": 0, "neutral": 100, "risk_off": 0}
    radar = "Sin datos disponibles"
    sectors = []
    scanner = []
    ranking = []
    cartera = []
    resultados = []
    analisis_cartera = "Sin análisis disponible"
    estrategia = "Sin estrategia disponible"
    alertas = ""
    informe = ""
    theme = {
        "theme": "Sin tema dominante claro",
        "confidence": 0,
        "bias": "NEUTRAL",
        "drivers": [],
        "favored_assets": [],
        "harmed_assets": [],
        "summary_es": "No se pudo detectar un tema dominante del mercado."
    }

    # -------------------
    # MACRO
    # -------------------
    print("Analizando entorno macroeconómico...")

    try:
        macro = analizar_macro_global()

        if isinstance(macro, dict):
            report += "🌍 MACRO GLOBAL\n\n"
            report += f"SPY: {macro.get('SPY', 'N/D')}\n"
            report += f"VIX: {macro.get('VIX', 'N/D')}\n"
            report += f"DXY: {macro.get('DXY', 'N/D')}\n"
            report += f"ORO: {macro.get('ORO', 'N/D')}\n"
            report += f"PETROLEO: {macro.get('PETROLEO', 'N/D')}\n\n"

            if macro.get("correlaciones"):
                report += "🔗 Correlaciones:\n"
                report += f"{macro.get('correlaciones', 'N/D')}\n\n"
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
        report += f"Score: {crash.get('crash_score', 'N/D')}\n"
        report += f"Nivel: {crash.get('crash_risk', 'N/D')}\n\n"

    except Exception as e:
        print("Error crash detector:", e)

    # -------------------
    # MACRO FORECAST
    # -------------------
    print("Calculando forecast macro...")

    try:
        forecast = macro_forecast()

        report += "🔮 MACRO FORECAST\n\n"
        report += f"Risk On: {forecast.get('risk_on', 0)}%\n"
        report += f"Neutral: {forecast.get('neutral', 0)}%\n"
        report += f"Risk Off: {forecast.get('risk_off', 0)}%\n\n"

    except Exception as e:
        print("Error forecast:", e)

    # -------------------
    # RADAR GLOBAL
    # -------------------
    print("Analizando radar global...")

    try:
        radar = radar_global()

        report += "🌎 RADAR GLOBAL\n\n"
        report += f"{radar}\n\n"

    except Exception as e:
        print("Error radar:", e)

    # -------------------
    # ROTACION SECTORIAL
    # -------------------
    print("Analizando rotación sectorial...")

    try:
        sectors = sector_rotation()

        report += "🏭 ROTACION SECTORIAL\n\n"

        if sectors:
            for s in sectors[:5]:
                report += f"{s[0]} : {s[1]}%\n"
        else:
            report += "Sin datos de rotación sectorial\n"

        report += "\n"

    except Exception as e:
        print("Error rotación:", e)

    # -------------------
    # MARKET THEME DETECTOR
    # -------------------
    print("Detectando tema dominante del mercado...")

    try:
        theme = detectar_market_theme(macro, noticias_texto, sectors)

        report += "🧠 MARKET THEME\n\n"
        report += f"Tema dominante: {theme.get('theme', 'N/D')}\n"
        report += f"Confianza: {theme.get('confidence', 0)}%\n"
        report += f"Sesgo: {theme.get('bias', 'NEUTRAL')}\n"
        report += f"Drivers: {', '.join(theme.get('drivers', [])) if theme.get('drivers') else 'Sin drivers claros'}\n"
        report += f"Favorece: {', '.join(theme.get('favored_assets', [])) if theme.get('favored_assets') else 'N/D'}\n"
        report += f"Perjudica: {', '.join(theme.get('harmed_assets', [])) if theme.get('harmed_assets') else 'N/D'}\n\n"

    except Exception as e:
        print("Error market theme detector:", e)

    # -------------------
    # SCANNER GLOBAL
    # -------------------
    print("Buscando oportunidades globales...")

    try:
        scanner = scan_assets()
        ranking = rank_opportunities(scanner)

        report += "🚀 OPORTUNIDADES GLOBALES\n\n"

        if ranking:
            for r in ranking[:10]:
                report += f"{r['ticker']} | Score {r['score']} | {r['nivel']}\n"
        else:
            report += "Sin oportunidades destacadas por ahora\n"

        report += "\n"

    except Exception as e:
        print("Error scanner:", e)

    # -------------------
    # CARTERA
    # -------------------
    print("Analizando cartera...")
    report += "📈 CARTERA\n\n"

    try:
        cartera = obtener_cartera()
    except Exception as e:
        print("Error obteniendo cartera:", e)
        cartera = []

    for ticker in cartera:
        print("Analizando", ticker)

        try:
            r = analizar_activo(ticker)

            if r:
                resultados.append(r)

                report += f"{r.get('ticker', 'N/D')}\n"
                report += f"Precio: {r.get('price', 'N/D')}\n"
                report += f"MA50: {r.get('ma50', 'N/D')}\n"
                report += f"Señal: {r.get('signal', 'N/D')}\n\n"

        except Exception as e:
            print("Error activo:", ticker, e)

    # -------------------
    # IA CARTERA
    # -------------------
    print("IA analizando cartera...")

    try:
        analisis_cartera = analizar_cartera_ia(resultados)

        report += "🧠 IA CARTERA\n"
        report += f"{analisis_cartera}\n\n"

    except Exception as e:
        print("Error IA cartera:", e)

    # -------------------
    # IA ESTRATEGIA
    # -------------------
    print("Generando estrategia IA...")

    try:
        estrategia = generar_estrategia_ia(
            macro,
            resultados,
            noticias_texto,
            theme.get("summary_es", "")
        )

        report += "📊 ESTRATEGIA IA\n"

        if estrategia and str(estrategia).strip():
            report += f"{estrategia}\n\n"
        else:
            report += "Sin cambios estratégicos destacados por el momento\n\n"

    except Exception as e:
        print("Error estrategia IA:", e)

    # -------------------
    # ALERTAS
    # -------------------
    print("Revisando alertas...")

    try:
        alertas = revisar_alertas()

        if alertas:
            report += "🚨 ALERTAS\n"
            report += f"{alertas}\n\n"

    except Exception as e:
        print("Error alertas:", e)

    # -------------------
    # INFORME FINAL
    # -------------------
    print("Generando informe final...")

    try:
        informe = generar_informe_final(
            macro=macro,
            radar=radar,
            cartera=resultados,
            risk_score=risk_score,
            crash=crash,
            noticias=noticias_texto + "\n\n" + theme.get("summary_es", "")
        )

        if informe and str(informe).strip():
            report += f"{informe}\n"

    except Exception as e:
        print("Error informe final:", e)

    enviar_telegram(report)
    print("Reporte enviado")


if __name__ == "__main__":
    while True:
        run_agent()
        print("Esperando 6 horas...")
        time.sleep(21600)