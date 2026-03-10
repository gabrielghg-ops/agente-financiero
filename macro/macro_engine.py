import yfinance as yf

from macro.macro_news import resumen_noticias
from macro.macro_risk_score import calcular_risk_score
from macro.macro_conclusion import generar_conclusion


def analizar_macro_global():

    print("Analizando entorno macroeconómico...")

    datos = {}

    try:

        # SPY (mercado USA)
        spy = yf.download("SPY", period="6mo", progress=False)

        if not spy.empty:

            price = spy["Close"].iloc[-1]
            ma200 = spy["Close"].rolling(200).mean().iloc[-1]

            datos["SPY"] = {
                "precio": round(float(price), 2),
                "ma200": round(float(ma200), 2),
                "tendencia": "alcista" if price > ma200 else "bajista"
            }

    except Exception as e:

        print("Error analizando SPY:", e)

    try:

        # VIX (riesgo)
        vix = yf.download("^VIX", period="6mo", progress=False)

        if not vix.empty:

            datos["VIX"] = round(float(vix["Close"].iloc[-1]), 2)

    except Exception as e:

        print("Error analizando VIX:", e)

    try:

        # Dólar
        dxy = yf.download("DX-Y.NYB", period="6mo", progress=False)

        if not dxy.empty:

            datos["DXY"] = round(float(dxy["Close"].iloc[-1]), 2)

    except Exception as e:

        print("Error analizando DXY:", e)

    try:

        # Petróleo
        oil = yf.download("CL=F", period="6mo", progress=False)

        if not oil.empty:

            datos["OIL"] = round(float(oil["Close"].iloc[-1]), 2)

    except Exception as e:

        print("Error analizando Oil:", e)

    try:

        # Oro
        gold = yf.download("GC=F", period="6mo", progress=False)

        if not gold.empty:

            datos["GOLD"] = round(float(gold["Close"].iloc[-1]), 2)

    except Exception as e:

        print("Error analizando Gold:", e)

    # score de riesgo
    score = calcular_risk_score()

    datos["risk_score"] = score

    # noticias
    noticias = resumen_noticias()

    # conclusión macro
    conclusion = generar_conclusion(datos, noticias)

    reporte = f"""
🌍 MACRO GLOBAL

SPY tendencia: {datos.get("SPY",{}).get("tendencia","?")}
VIX: {datos.get("VIX","?")}
DXY: {datos.get("DXY","?")}
Oro: {datos.get("GOLD","?")}
Petróleo: {datos.get("OIL","?")}

Risk Score: {score}/100

📰 Contexto noticias:
{noticias}

🧠 Conclusión estratégica:
{conclusion}
"""

    return reporte