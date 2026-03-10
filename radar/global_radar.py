import yfinance as yf


def radar_global():

    activos = {

        "SPY": "Acciones USA",
        "EEM": "Emergentes",
        "EWZ": "Brasil",
        "GLD": "Oro",
        "SLV": "Plata",
        "XLK": "Tecnologia",
        "IBIT": "Bitcoin ETF"

    }

    resultado = ""

    for ticker in activos:

        try:

            data = yf.download(ticker, period="3mo")

            price = float(data["Close"].iloc[-1])
            ma50 = float(data["Close"].rolling(50).mean().iloc[-1])

            if price > ma50:

                estado = "Fuerte"

            else:

                estado = "Débil"

            resultado += f"{activos[ticker]}: {estado}\n"

        except:

            pass

    return resultado