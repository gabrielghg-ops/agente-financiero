import yfinance as yf


def get_last_price(ticker):

    try:

        df = yf.download(ticker, period="5d", progress=False)

        if df is None or df.empty:
            return None

        return float(df["Close"].iloc[-1])

    except:
        return None


def analizar_macro():

    print("Analizando entorno macroeconómico...")

    vix = get_last_price("^VIX")
    tnx = get_last_price("^TNX")
    dxy = get_last_price("DX-Y.NYB")
    spy = get_last_price("SPY")

    macro_text = "🌎 ANALISIS MACRO\n\n"

    score = 0

    # VIX
    if vix:

        if vix < 18:
            macro_text += f"VIX: {round(vix,2)} (riesgo bajo)\n"
            score += 1

        elif vix < 25:
            macro_text += f"VIX: {round(vix,2)} (riesgo moderado)\n"

        else:
            macro_text += f"VIX: {round(vix,2)} (riesgo alto)\n"
            score -= 1

    # Tasas
    if tnx:

        if tnx < 3.5:
            macro_text += f"Tasas 10Y: {round(tnx,2)}% (estímulo)\n"
            score += 1

        elif tnx > 4.5:
            macro_text += f"Tasas 10Y: {round(tnx,2)}% (presión sobre acciones)\n"
            score -= 1

        else:
            macro_text += f"Tasas 10Y: {round(tnx,2)}% (neutral)\n"

    # Dólar
    if dxy:

        if dxy > 105:
            macro_text += f"Dólar fuerte: {round(dxy,2)}\n"
            score -= 1

        elif dxy < 100:
            macro_text += f"Dólar débil: {round(dxy,2)}\n"
            score += 1

        else:
            macro_text += f"Dólar neutral: {round(dxy,2)}\n"

    # SPY
    if spy:

        macro_text += f"SPY referencia: {round(spy,2)}\n"

    macro_text += "\n"

    # Conclusión macro
    if score >= 2:

        macro_text += "🟢 Entorno RISK ON (favorable para acciones)"

    elif score <= -2:

        macro_text += "🔴 Entorno RISK OFF (mercado defensivo)"

    else:

        macro_text += "🟡 Entorno NEUTRAL"

    print("Macro OK")

    return macro_text