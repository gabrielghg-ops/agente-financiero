import yfinance as yf
import pandas as pd


def _to_float_last(value):
    """
    Convierte de forma segura un valor/Series/DataFrame al último float disponible.
    """
    if value is None:
        return None

    if isinstance(value, pd.DataFrame):
        if value.empty:
            return None
        value = value.iloc[:, 0]

    if isinstance(value, pd.Series):
        if value.empty:
            return None
        return float(value.dropna().iloc[-1])

    try:
        return float(value)
    except Exception:
        return None


def _download_close(ticker, period="6mo", interval="1d"):
    data = yf.download(
        ticker,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False,
        group_by="column"
    )

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
        return close.dropna()

    return None


def analizar_macro_global():
    spy_close = _download_close("SPY")
    vix_close = _download_close("^VIX")
    dxy_close = _download_close("DX-Y.NYB")
    gold_close = _download_close("GLD")
    oil_close = _download_close("CL=F")

    spy_price = _to_float_last(spy_close)
    vix_value = _to_float_last(vix_close)
    dxy_value = _to_float_last(dxy_close)
    gold_value = _to_float_last(gold_close)
    oil_value = _to_float_last(oil_close)

    spy_ma50 = _to_float_last(spy_close.rolling(50).mean()) if spy_close is not None and len(spy_close) >= 50 else None
    gold_ma50 = _to_float_last(gold_close.rolling(50).mean()) if gold_close is not None and len(gold_close) >= 50 else None

    correlaciones = []

    if vix_value is not None:
        if vix_value > 22:
            correlaciones.append("Mercado sensible al riesgo (VIX inverso)")
        else:
            correlaciones.append("Volatilidad controlada")

    if spy_price is not None and spy_ma50 is not None:
        if spy_price > spy_ma50:
            correlaciones.append("SPY sobre MA50")
        else:
            correlaciones.append("SPY bajo MA50")

    if gold_value is not None and gold_ma50 is not None:
        if gold_value > gold_ma50:
            correlaciones.append("Oro fuerte sobre MA50")
        else:
            correlaciones.append("Oro sin liderazgo claro")

    return {
        "SPY": round(spy_price, 2) if spy_price is not None else "N/D",
        "VIX": round(vix_value, 2) if vix_value is not None else "N/D",
        "DXY": round(dxy_value, 2) if dxy_value is not None else "N/D",
        "ORO": round(gold_value, 2) if gold_value is not None else "N/D",
        "PETROLEO": round(oil_value, 2) if oil_value is not None else "N/D",
        "correlaciones": " | ".join(correlaciones) if correlaciones else "Sin correlaciones relevantes"
    }