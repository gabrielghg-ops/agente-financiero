import yfinance as yf

def macro_forecast():

    spy = yf.download("SPY", period="3mo")
    vix = yf.download("^VIX", period="3mo")

    spy_return = (spy["Close"].iloc[-1] / spy["Close"].iloc[0]) - 1
    vix_level = vix["Close"].iloc[-1]

    risk_on = 50
    neutral = 30
    risk_off = 20

    if spy_return > 0:
        risk_on += 20

    if vix_level > 25:
        risk_off += 20

    total = risk_on + neutral + risk_off

    return {
        "risk_on": round(risk_on / total * 100, 1),
        "neutral": round(neutral / total * 100, 1),
        "risk_off": round(risk_off / total * 100, 1)
    }