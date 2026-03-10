import yfinance as yf

from macro.macro_risk_score import calcular_risk_score
from macro.macro_news import resumen_noticias
from macro.macro_conclusion import generar_conclusion
from macro.macro_correlation import analizar_correlaciones


def analizar_macro_global():

    print("Analizando entorno macroeconómico...")

    datos = {}

    try:

        spy = yf.download("SPY", period="6mo", progress=False)
        vix = yf.download("^VIX", period="6mo", progress=False)
        dxy = yf.download("DX-Y.NYB", period="6mo", progress=False)
        gold = yf.download("GC=F", period="6mo", progress=False)
        oil = yf.download("CL=F", period="6mo", progress=False)

        datos["spy"] = spy["Close"].iloc[-1]
        datos["vix"] = vix["Close"].iloc[-1]
        datos["dxy"] = dxy["Close"].iloc[-1]
        datos["gold"] = gold["Close"].iloc[-1]
        datos["oil"] = oil["Close"].iloc[-1]

    except Exception as e:

        print("Error macro:", e)

    score = calcular_risk_score()

    noticias = resumen_noticias()

    correlaciones = analizar_correlaciones(datos)

    conclusion = generar_conclusion(datos, score, noticias)

    reporte = f"""
🌍 MACRO GLOBAL

SPY: {round(datos.get("spy",0),2)}
VIX: {round(datos.get("vix",0),2)}
DXY: {round(datos.get("dxy",0),2)}
ORO: {round(datos.get("gold",0),2)}
PETROLEO: {round(datos.get("oil",0),2)}

Risk Score: {score}/100

🔗 Correlaciones:
{correlaciones}

📰 Contexto global:
{noticias}

📊 Conclusión:
{conclusion}
"""

    return reporte