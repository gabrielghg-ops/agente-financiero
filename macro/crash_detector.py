import yfinance as yf
import pandas as pd


def _to_float_last(value):
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
        spy_close = _download_close("SPY", period="10mo")
        vix_close = _download_close("^VIX", period="4mo")
        dxy_close = _download_close("DX-Y.NYB", period="4mo")
        gld_close = _download_close("GLD", period="6mo")
        oil_close = _download_close("CL=F", period="6mo")

        if spy_close is None or vix_close is None:
            return {"crash_score": 0, "crash_risk": "SIN DATOS"}

        spy_price = _to_float_last(spy_close)
        spy_ma50 = _to_float_last(spy_close.rolling(50).mean()) if len(spy_close) >= 50 else spy_price
        spy_ma200 = _to_float_last(spy_close.rolling(200).mean()) if len(spy_close) >= 200 else spy_ma50

        vix_value = _to_float_last(vix_close)
        dxy_value = _to_float_last(dxy_close) if dxy_close is not None else None
        gld_value = _to_float_last(gld_close) if gld_close is not None else None
        gld_ma50 = _to_float_last(gld_close.rolling(50).mean()) if gld_close is not None and len(gld_close) >= 50 else gld_value
        oil_value = _to_float_last(oil_close) if oil_close is not None else None

        score = 0

        # SPY
        if spy_price is not None and spy_ma50 is not None and spy_price < spy_ma50:
            score += 16

        if spy_price is not None and spy_ma200 is not None and spy_price < spy_ma200:
            score += 20

        if (
            spy_price is not None and spy_ma50 is not None and spy_ma200 is not None
            and spy_price < spy_ma50 and spy_ma50 < spy_ma200
        ):
            score += 8

        # VIX
        if vix_value is not None and vix_value >= 22:
            score += 10
        if vix_value is not None and vix_value >= 25:
            score += 8
        if vix_value is not None and vix_value >= 30:
            score += 10

        # DXY
        if dxy_value is not None and dxy_value >= 103:
            score += 4
        if dxy_value is not None and dxy_value >= 105:
            score += 4

        # Oro
        if gld_value is not None and gld_ma50 is not None and gld_value > gld_ma50:
            score += 4

        # Petróleo
        if oil_value is not None and oil_value >= 85:
            score += 5
        if oil_value is not None and oil_value >= 95:
            score += 5

        # Combinaciones
        if (
            spy_price is not None and spy_ma50 is not None and vix_value is not None
            and spy_price < spy_ma50 and vix_value >= 22
        ):
            score += 6

        if (
            spy_price is not None and spy_ma50 is not None and oil_value is not None
            and spy_price < spy_ma50 and oil_value >= 90
        ):
            score += 4

        if (
            vix_value is not None and oil_value is not None
            and vix_value >= 25 and oil_value >= 90
        ):
            score += 5

        score = min(score, 100)

        if score < 25:
            level = "BAJO"
        elif score < 45:
            level = "MEDIO"
        elif score < 70:
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