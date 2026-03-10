import yfinance as yf

from macro.macro_news import analizar_noticias
from macro.macro_correlation import analizar_correlaciones
from macro.macro_conclusion import generar_conclusion


def determinar_risk_mode(score):

    if score >= 70:
        return "RISK ON"

    elif score >= 40:
        return "NEUTRAL"

    else:
        return "RISK OFF"


def analizar_macro_global():

    print("Analizando entorno macroeconómico...")

    try:

        spy = yf.download("SPY", period="6mo")
        vix = yf.download("^VIX", period="6mo")
        dxy = yf.download("DX-Y.NYB", period="6mo")
        gold = yf.download("GC=F", period="6mo")
        oil = yf.download("CL=F", period="6mo")

        # Convertir correctamente a float
        spy_val = float(spy["Close"].iloc[-1].item())
        vix_val = float(vix["Close"].iloc[-1].item())
        dxy_val = float(dxy["Close"].iloc[-1].item())
        gold_val = float(gold["Close"].iloc[-1].item())
        oil_val = float(oil["Close"].iloc[-1].item())

        spy_mean = float(spy["Close"].mean().item())
        vix_mean = float(vix["Close"].mean().item())

    except Exception as e:

        print("Error macro:", e)

        return "Error obteniendo datos macro"


    score = 50

    if spy_val > spy_mean:
        score += 10
    else:
        score -= 10

    if vix_val < vix_mean:
        score += 10
    else:
        score -= 10

    if dxy_val < 105:
        score += 5
    else:
        score -= 5

    if gold_val > 2000:
        score -= 5

    if oil_val > 95:
        score -= 5


    # NOTICIAS
    noticias_texto, riesgo_noticias = analizar_noticias()

    score = score - riesgo_noticias

    score = max(0, min(100, score))

    risk_mode = determinar_risk_mode(score)

    correlaciones = analizar_correlaciones()

    conclusion = generar_conclusion(
        {
            "SPY": spy_val,
            "VIX": vix_val,
            "DXY": dxy_val,
            "GOLD": gold_val,
            "OIL": oil_val
        },
        score,
        noticias_texto,
        risk_mode
    )

    report = f"""
🌍 MACRO GLOBAL

SPY: {spy_val}
VIX: {vix_val}
DXY: {dxy_val}
ORO: {gold_val}
PETROLEO: {oil_val}

Risk Score: {score}/100
Modo de mercado: {risk_mode}

🔗 Correlaciones:
{correlaciones}

📰 Contexto global:
{noticias_texto}

📊 Conclusión estratégica:
{conclusion}
"""

    return report