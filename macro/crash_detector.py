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
        value = value.dropna()
        if value.empty:
            return None
        return float(value.iloc[-1])

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
        close = close.dropna()
        return close if not close.empty else None

    return None


def detect_crash_risk():
    try:
        spy_close = _download_close("SPY", period="8mo")
        vix_close = _download_close("^VIX", period="3mo")
        dxy_close = _download_close("DX-Y.NYB", period="3mo")
        gld_close = _download_close("GLD", period="6mo")
        oil_close = _download_close("CL=F", period="6mo")

        if spy_close is None or vix_close is None:
            return {"crash_score": 0, "crash_risk": "SIN DATOS"}

        spy_price = _to_float_last(spy_close)
        spy_ma50 = _to_float_last(spy_close.rolling(50).mean()) if len(spy_close) >= 50 else spy_price
        spy_ma200 = _to_float_last(spy_close.rolling(200).mean()) if len(spy_close) >= 200 else spy_ma50

        vix_value = _to_float_last(vix_close)
        dxy_value = _to_float_last(dxy_close) if dxy_close is not None else 0
        gld_value = _to_float_last(gld_close) if gld_close is not None else 0
        gld_ma50 = _to_float_last(gld_close.rolling(50).mean()) if gld_close is not None and len(gld_close) >= 50 else gld_value
        oil_value = _to_float_last(oil_close) if oil_close is not None else 0

        score = 0

        # Estructura técnica del SPY
        if spy_price is not None and spy_ma50 is not None and spy_price < spy_ma50:
            score += 20

        if spy_price is not None and spy_ma200 is not None and spy_price < spy_ma200:
            score += 25

        if (
            spy_price is not None
            and spy_ma50 is not None
            and spy_ma200 is not None
            and spy_price < spy_ma50
            and spy_ma50 < spy_ma200
        ):
            score += 10

        # Volatilidad
        if vix_value is not None and vix_value >= 22:
            score += 15
        if vix_value is not None and vix_value >= 25:
            score += 10
        if vix_value is not None and vix_value >= 30:
            score += 10

        # Dólar fuerte
        if dxy_value is not None and dxy_value >= 103:
            score += 5
        if dxy_value is not None and dxy_value >= 105:
            score += 5

        # Oro como refugio
        if (
            gld_value is not None
            and gld_ma50 is not None
            and gld_value > gld_ma50
        ):
            score += 5

        # Petróleo / shock geopolítico-inflacionario
        if oil_value is not None and oil_value >= 85:
            score += 8
        if oil_value is not None and oil_value >= 95:
            score += 7

        # Combinaciones de estrés
        if (
            spy_price is not None
            and spy_ma50 is not None
            and vix_value is not None
            and spy_price < spy_ma50
            and vix_value >= 22
        ):
            score += 8

        if (
            spy_price is not None
            and spy_ma50 is not None
            and oil_value is not None
            and spy_price < spy_ma50
            and oil_value >= 90
        ):
            score += 5

        if (
            vix_value is not None
            and oil_value is not None
            and vix_value >= 25
            and oil_value >= 90
        ):
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