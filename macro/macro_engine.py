import yfinance as yf


def analizar_macro_global():

    spy = yf.download("SPY", period="6mo")
    vix = yf.download("^VIX", period="6mo")
    dxy = yf.download("DX-Y.NYB", period="6mo")
    gold = yf.download("GLD", period="6mo")
    oil = yf.download("CL=F", period="6mo")

    spy_price = float(spy["Close"].iloc[-1])
    vix_value = float(vix["Close"].iloc[-1])
    dxy_value = float(dxy["Close"].iloc[-1])
    gold_value = float(gold["Close"].iloc[-1])
    oil_value = float(oil["Close"].iloc[-1])

    spy_ma50 = float(spy["Close"].rolling(50).mean().iloc[-1])
    gold_ma50 = float(gold["Close"].rolling(50).mean().iloc[-1])

    correlaciones = []

    if vix_value > 22:
        correlaciones.append("Mercado sensible al riesgo (VIX inverso)")
    else:
        correlaciones.append("Volatilidad controlada")

    if spy_price > spy_ma50:
        correlaciones.append("SPY sobre MA50")
    else:
        correlaciones.append("SPY bajo MA50")

    if gold_value > gold_ma50:
        correlaciones.append("Oro fuerte sobre MA50")

    return {
        "SPY": round(spy_price, 2),
        "VIX": round(vix_value, 2),
        "DXY": round(dxy_value, 2),
        "ORO": round(gold_value, 2),
        "PETROLEO": round(oil_value, 2),
        "correlaciones": " | ".join(correlaciones)
    }