import yfinance as yf
import pandas as pd


def _get_close_series(data):
    if data is None or data.empty:
        return pd.Series(dtype="float64")

    close = data["Close"]

    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    return pd.to_numeric(close, errors="coerce").dropna()


def detect_crash_risk():
    spy = yf.download("SPY", period="12mo", interval="1d", progress=False)
    vix = yf.download("^VIX", period="12mo", interval="1d", progress=False)

    spy_close = _get_close_series(spy)
    vix_close = _get_close_series(vix)

    if len(spy_close) < 50 or len(vix_close) == 0:
        return {
            "crash_score": 0,
            "crash_risk": "SIN DATOS"
        }

    spy_price = float(spy_close.iloc[-1])
    ma50 = spy_close.rolling(50).mean().iloc[-1]

    score = 0

    if pd.notna(ma50) and spy_price < float(ma50):
        score += 40

    vix_value = float(vix_close.iloc[-1])

    if vix_value > 30:
        score += 35
    elif vix_value > 25:
        score += 20

    if len(spy_close) >= 20:
        ret_20d = (spy_price / float(spy_close.iloc[-20])) - 1
        if ret_20d < -0.08:
            score += 25
        elif ret_20d < -0.05:
            score += 15

    score = min(score, 100)

    if score < 30:
        level = "BAJO"
    elif score < 60:
        level = "MEDIO"
    else:
        level = "ALTO"

    return {
        "crash_score": score,
        "crash_risk": level
    }