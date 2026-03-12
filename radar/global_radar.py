import yfinance as yf

ASSETS = {
    "SPY": "USA",
    "EEM": "Emergentes",
    "EWZ": "Brasil",
    "GLD": "Oro",
    "SLV": "Plata",
    "XLK": "Tecnologia",
    "IBIT": "Bitcoin ETF",
}


def radar_global():
    lineas = []

    for ticker, nombre in ASSETS.items():
        try:
            data = yf.download(ticker, period="6mo", interval="1d", auto_adjust=True, progress=False)

            if data is None or data.empty or len(data) < 60:
                lineas.append(f"{ticker} ({nombre}) | Sin datos suficientes")
                continue

            close = data["Close"]
            price = float(close.iloc[-1])
            ma50 = float(close.rolling(50).mean().iloc[-1])
            perf_3m = ((price / float(close.iloc[-63])) - 1) * 100 if len(close) >= 63 else 0.0

            tendencia = "alcista" if price > ma50 else "bajista"

            lineas.append(
                f"{ticker} ({nombre}) | Perf 3m: {perf_3m:.2f}% | Tendencia actual: {tendencia}"
            )

        except Exception as e:
            lineas.append(f"{ticker} ({nombre}) | Error: {str(e)}")

    return "\n".join(lineas)