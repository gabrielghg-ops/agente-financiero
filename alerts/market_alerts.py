import yfinance as yf


def revisar_alertas():

    alertas = ""

    try:

        spy = yf.download("SPY", period="2d")
        vix = yf.download("^VIX", period="2d")
        btc = yf.download("BTC-USD", period="2d")

        # SPY
        spy_hoy = float(spy["Close"].iloc[-1].item())
        spy_ayer = float(spy["Close"].iloc[-2].item())

        spy_cambio = (spy_hoy - spy_ayer) / spy_ayer * 100

        if spy_cambio < -3:
            alertas += "⚠ SPY cayó más de 3% hoy\n"

        # VIX
        vix_actual = float(vix["Close"].iloc[-1].item())

        if vix_actual > 30:
            alertas += "⚠ VIX indica volatilidad extrema\n"

        # BTC
        btc_hoy = float(btc["Close"].iloc[-1].item())
        btc_ayer = float(btc["Close"].iloc[-2].item())

        btc_cambio = (btc_hoy - btc_ayer) / btc_ayer * 100

        if btc_cambio < -8:
            alertas += "⚠ BTC caída fuerte (>8%)\n"

    except Exception as e:

        print("Error en alertas:", e)

    return alertas