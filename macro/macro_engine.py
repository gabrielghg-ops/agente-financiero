import yfinance as yf

from macro.macro_risk_score import calcular_risk_score
from macro.macro_news import resumen_noticias
from macro.macro_conclusion import generar_conclusion
from macro.macro_correlation import analizar_correlaciones


def ultimo_valor(df):

    try:
        val = df["Close"].iloc[-1]

        if hasattr(val, "item"):
            val = val.item()

        return float(val)

    except:
        return 0


def analizar_macro_global():

    print("Analizando entorno macroeconómico...")

    datos = {}

    try:

        spy = yf.download("SPY", period="6mo", progress=False)
        vix = yf.download("^VIX", period="6mo", progress=False)
        dxy = yf.download("DX-Y.NYB", period="6mo", progress=False)
        gold = yf.download("GC=F", period="6mo", progress=False)
        oil = yf.download("CL=F", period="6mo", progress=False)

        datos["spy"] = ultimo_valor(spy)
        datos["vix"] = ultimo_valor(vix)
        datos["dxy"] = ultimo_valor(dxy)
        datos["gold"] = ultimo_valor(gold)
        datos["oil"] = ultimo_valor(oil)

    except Exception as e:

        print("Error macro:", e)

    score = calcular_risk_score(datos)

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