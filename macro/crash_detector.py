import yfinance as yf


def detect_crash_risk():
    try:
        spy = yf.download("SPY", period="8mo", interval="1d", auto_adjust=True, progress=False)
        vix = yf.download("^VIX", period="3mo", interval="1d", auto_adjust=True, progress=False)
        dxy = yf.download("DX-Y.NYB", period="3mo", interval="1d", auto_adjust=True, progress=False)
        gld = yf.download("GLD", period="6mo", interval="1d", auto_adjust=True, progress=False)
        oil = yf.download("CL=F", period="6mo", interval="1d", auto_adjust=True, progress=False)

        if spy.empty or vix.empty:
            return {"crash_score": 0, "crash_risk": "SIN DATOS"}

        spy_close = spy["Close"]
        spy_price = float(spy_close.iloc[-1])
        spy_ma50 = float(spy_close.rolling(50).mean().iloc[-1]) if len(spy_close) >= 50 else spy_price
        spy_ma200 = float(spy_close.rolling(200).mean().iloc[-1]) if len(spy_close) >= 200 else spy_ma50

        vix_value = float(vix["Close"].iloc[-1])

        dxy_value = float(dxy["Close"].iloc[-1]) if not dxy.empty else 0
        gld_close = gld["Close"]
        gld_value = float(gld_close.iloc[-1]) if not gld.empty else 0
        gld_ma50 = float(gld_close.rolling(50).mean().iloc[-1]) if len(gld_close) >= 50 else gld_value
        oil_value = float(oil["Close"].iloc[-1]) if not oil.empty else 0

        score = 0

        # SPY estructura técnica
        if spy_price < spy_ma50:
            score += 20

        if spy_price < spy_ma200:
            score += 25

        if spy_price < spy_ma50 and spy_ma50 < spy_ma200:
            score += 10

        # Volatilidad
        if vix_value >= 22:
            score += 15
        if vix_value >= 25:
            score += 10
        if vix_value >= 30:
            score += 10

        # Dólar fuerte
        if dxy_value >= 103:
            score += 5
        if dxy_value >= 105:
            score += 5

        # Oro refugio
        if gld_value > gld_ma50:
            score += 5

        # Petróleo / shock inflacionario-geopolítico
        if oil_value >= 85:
            score += 8
        if oil_value >= 95:
            score += 7

        # Bonus por combinación de estrés
        if spy_price < spy_ma50 and vix_value >= 22:
            score += 8

        if spy_price < spy_ma50 and oil_value >= 90:
            score += 5

        if vix_value >= 25 and oil_value >= 90:
            score += 7

        score = min(score, 100)

        if score < 25:
            level = "BAJO"
        elif score < 50:
            level = "MEDIO"
        elif score < 75:
            level = "ALTO"
        else:
            level = "EXTREMO"

        return {
            "crash_score": score,
            "crash_risk": level
        }

    except Exception as e:
        print("Error detect_crash_risk:", e)
        return {
            "crash_score": 0,
            "crash_risk": "SIN DATOS"
        }