import yfinance as yf

def analizar_macro():

    try:
        spy = yf.download("SPY", period="3mo")["Close"]
        gld = yf.download("GLD", period="3mo")["Close"]

        spy_change = spy.pct_change().mean()
        gold_change = gld.pct_change().mean()

        if spy_change > 0 and gold_change < 0:
            return "📈 Mercado en modo RISK ON"

        if spy_change < 0 and gold_change > 0:
            return "⚠ Mercado en modo RISK OFF"

        return "➖ Mercado lateral"

    except:
        return "No se pudo analizar macro"