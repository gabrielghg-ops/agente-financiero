import yfinance as yf


def calcular_risk_score(noticias_riesgo):

    try:

        spy = yf.download("SPY", period="3mo")
        vix = yf.download("^VIX", period="1mo")
        gold = yf.download("GC=F", period="3mo")
        oil = yf.download("CL=F", period="1mo")

        spy_price = float(spy["Close"].iloc[-1])
        spy_ma50 = float(spy["Close"].rolling(50).mean().iloc[-1])

        vix_val = float(vix["Close"].iloc[-1])
        gold_val = float(gold["Close"].iloc[-1])
        oil_val = float(oil["Close"].iloc[-1])

        score = 0

        # tendencia mercado
        if spy_price < spy_ma50:
            score += 25

        # volatilidad
        if vix_val > 25:
            score += 20

        # petróleo shock
        if oil_val > 95:
            score += 15

        # oro refugio
        if gold_val > gold["Close"].rolling(50).mean().iloc[-1]:
            score += 10

        # noticias
        score += noticias_riesgo

        if score > 100:
            score = 100

        return score

    except Exception as e:

        print("Error risk model:", e)

        return 50