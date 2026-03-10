import yfinance as yf

from macro.macro_news import analizar_noticias


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

        spy = yf.download("SPY", period="5d")
        vix = yf.download("^VIX", period="5d")
        dxy = yf.download("DX-Y.NYB", period="5d")
        gold = yf.download("GC=F", period="5d")
        oil = yf.download("CL=F", period="5d")

        spy_val = float(spy["Close"].iloc[-1].item())
        vix_val = float(vix["Close"].iloc[-1].item())
        dxy_val = float(dxy["Close"].iloc[-1].item())
        gold_val = float(gold["Close"].iloc[-1].item())
        oil_val = float(oil["Close"].iloc[-1].item())

    except Exception as e:

        print("Error obteniendo datos macro:", e)

        return "Error obteniendo datos macro\n"

    # -------------------------
    # SCORE BASE DE MERCADO
    # -------------------------

    score = 50

    # SPY fuerte
    if spy_val > spy["Close"].mean():
        score += 10
    else:
        score -= 10

    # volatilidad
    if vix_val < 20:
        score += 10
    elif vix_val > 30:
        score -= 15

    # dolar fuerte
    if dxy_val > dxy["Close"].mean():
        score -= 5

    # oro refugio
    if gold_val > gold["Close"].mean():
        score -= 5

    # petróleo alto = inflación
    if oil_val > oil["Close"].mean():
        score -= 5

    # -------------------------
    # ANALISIS DE NOTICIAS
    # -------------------------

    print("Analizando noticias macro...")

    noticias, riesgo_noticias = analizar_noticias()

    # -------------------------
    # SCORE FINAL
    # -------------------------

    score_total = score - riesgo_noticias

    if score_total < 0:
        score_total = 0

    if score_total > 100:
        score_total = 100

    risk_mode = determinar_risk_mode(score_total)

    # -------------------------
    # CORRELACION SIMPLE
    # -------------------------

    correlacion = ""

    if gold_val > gold["Close"].mean() and vix_val > 25:
        correlacion = "Flujo hacia activos refugio"

    elif spy_val > spy["Close"].mean() and vix_val < 20:
        correlacion = "Flujo hacia activos de riesgo"

    else:
        correlacion = "Mercado mixto"

    # -------------------------
    # CONCLUSION
    # -------------------------

    conclusion = ""

    if risk_mode == "RISK ON":

        conclusion = (
            "El entorno macro muestra condiciones favorables para activos de riesgo.\n\n"
            "Recomendación:\n"
            "- Mayor exposición a acciones\n"
            "- Favorecer índices\n"
            "- Crypto favorecida\n"
            "- Menor necesidad de refugio en oro\n"
        )

    elif risk_mode == "NEUTRAL":

        conclusion = (
            "El mercado se encuentra en fase de incertidumbre.\n\n"
            "Recomendación:\n"
            "- Mantener posiciones equilibradas\n"
            "- Reducir apalancamiento\n"
            "- Vigilar noticias macro\n"
        )

    else:

        conclusion = (
            "El mercado muestra señales de aversión al riesgo.\n\n"
            "Recomendación:\n"
            "- Reducir exposición a acciones\n"
            "- Aumentar activos defensivos\n"
            "- Considerar oro o cash\n"
        )

    # -------------------------
    # TEXTO FINAL
    # -------------------------

    texto = f"""
🌍 MACRO GLOBAL

SPY: {round(spy_val,2)}
VIX: {round(vix_val,2)}
DXY: {round(dxy_val,2)}
ORO: {round(gold_val,2)}
PETROLEO: {round(oil_val,2)}

Risk Score Mercado: {score}
Impacto Noticias: -{riesgo_noticias}

Global Risk Score: {score_total}/100
Modo de mercado: {risk_mode}

🔗 Correlaciones:
{correlacion}

📰 Contexto global:
{noticias}

📊 Conclusión estratégica:

{conclusion}
"""

    return texto