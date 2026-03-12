import yfinance as yf
import pandas as pd

ASSETS = {
    "SPY": "USA",
    "EEM": "Emergentes",
    "EWZ": "Brasil",
    "GLD": "Oro",
    "SLV": "Plata",
    "XLK": "Tecnologia",
    "IBIT": "Bitcoin ETF",
}


def _extract_close_series(data):
    """
    Extrae una serie de cierres de forma segura desde yfinance.
    """
    if data is None or data.empty:
        return None

    close = data.get("Close")

    if close is None:
        return None

    if isinstance(close, pd.DataFrame):
        if close.empty:
            return None
        close = close.iloc[:, 0]

    if isinstance(close, pd.Series):
        close = close.dropna()
        return close if not close.empty else None

    return None


def _last_float(value):
    """
    Convierte Series/DataFrame/valor al último float válido.
    """
    if value is None:
        return None

    if isinstance(value, pd.DataFrame):
        if value.empty:
            return None
        value = value.iloc[:, 0]

    if isinstance(value, pd.Series):
        value = value.dropna()
        if value.empty:
            return None
        return float(value.iloc[-1])

    try:
        return float(value)
    except Exception:
        return None


def radar_global():
    lineas = []

    for ticker, nombre in ASSETS.items():
        try:
            data = yf.download(
                ticker,
                period="6mo",
                interval="1d",
                auto_adjust=True,
                progress=False,
                group_by="column"
            )

            close = _extract_close_series(data)

            if close is None or len(close) < 60:
                lineas.append(f"{ticker} ({nombre}) | Sin datos suficientes")
                continue

            price = _last_float(close)
            ma50 = _last_float(close.rolling(50).mean())

            if price is None or ma50 is None:
                lineas.append(f"{ticker} ({nombre}) | Sin datos suficientes")
                continue

            # aprox 3 meses bursátiles = 63 ruedas
            base_idx = -63 if len(close) >= 63 else 0
            base_price = _last_float(close.iloc[base_idx])

            if base_price is None or base_price == 0:
                perf_3m = 0.0
            else:
                perf_3m = ((price / base_price) - 1) * 100

            tendencia = "alcista" if price > ma50 else "bajista"

            lineas.append(
                f"{ticker} ({nombre}) | Perf 3m: {perf_3m:.2f}% | Tendencia actual: {tendencia}"
            )

        except Exception as e:
            lineas.append(f"{ticker} ({nombre}) | Error: {str(e)}")

    return "\n".join(lineas)