import yfinance as yf


def calcular_risk_score():

    try:

        print("Calculando risk score global...")

        spy = yf.download("SPY", period="3mo", progress=False)
        vix = yf.download("^VIX", period="3mo", progress=False)

        if spy.empty or vix.empty:
            return 50

        spy_price = spy["Close"].iloc[-1]
        spy_avg = spy["Close"].mean()

        vix_level = vix["Close"].iloc[-1]

        score = 50

        # tendencia mercado
        if spy_price > spy_avg:
            score += 20
        else:
            score -= 20

        # volatilidad
        if vix_level < 20:
            score += 20
        else:
            score -= 20

        score = max(0, min(100, score))

        return score

    except Exception as e:

        print("Error calculando risk score:", e)

        return 50