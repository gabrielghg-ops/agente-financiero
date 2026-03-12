import yfinance as yf
import pandas as pd


def _extract_close_series(data):
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


def macro_forecast():
    try:
        spy = yf.download("SPY", period="6mo", interval="1d", auto_adjust=True, progress=False, group_by="column")
        vix = yf.download("^VIX", period="3mo", interval="1d", auto_adjust=True, progress=False, group_by="column")
        dxy = yf.download("DX-Y.NYB", period="3mo", interval="1d", auto_adjust=True, progress=False, group_by="column")
        gld = yf.download("GLD", period="6mo", interval="1d", auto_adjust=True, progress=False, group_by="column")
        oil = yf.download("CL=F", period="6mo", interval="1d", auto_adjust=True, progress=False, group_by="column")

        spy_close = _extract_close_series(spy)
        vix_close = _extract_close_series(vix)
        dxy_close = _extract_close_series(dxy)
        gld_close = _extract_close_series(gld)
        oil_close = _extract_close_series(oil)

        if spy_close is None or vix_close is None:
            return {"risk_on": 33.3, "neutral": 33.3, "risk_off": 33.4}

        spy_price = _last_float(spy_close)
        spy_ma50 = _last_float(spy_close.rolling(50).mean()) if len(spy_close) >= 50 else spy_price
        spy_ret_3m = ((_last_float(spy_close.iloc[-1]) / _last_float(spy_close.iloc[-63])) - 1) if len(spy_close) >= 63 else 0

        vix_value = _last_float(vix_close)
        dxy_value = _last_float(dxy_close) if dxy_close is not None else None
        gld_value = _last_float(gld_close) if gld_close is not None else None
        gld_ma50 = _last_float(gld_close.rolling(50).mean()) if gld_close is not None and len(gld_close) >= 50 else gld_value
        oil_value = _last_float(oil_close) if oil_close is not None else None

        risk_on = 35
        neutral = 35
        risk_off = 30

        # SPY
        if spy_price is not None and spy_ma50 is not None:
            if spy_price > spy_ma50:
                risk_on += 12
            else:
                risk_off += 15

        if spy_ret_3m > 0.05:
            risk_on += 8
        elif spy_ret_3m < -0.03:
            risk_off += 10

        # VIX
        if vix_value is not None:
            if vix_value < 18:
                risk_on += 10
            elif vix_value >= 22:
                risk_off += 15
            elif vix_value >= 25:
                risk_off += 5

        # DXY
        if dxy_value is not None and dxy_value >= 103:
            risk_off += 6

        # Oro
        if gld_value is not None and gld_ma50 is not None and gld_value > gld_ma50:
            risk_off += 6

        # Petróleo
        if oil_value is not None and oil_value >= 85:
            risk_off += 6
        if oil_value is not None and oil_value >= 95:
            risk_off += 4

        total = risk_on + neutral + risk_off

        return {
            "risk_on": round(risk_on / total * 100, 1),
            "neutral": round(neutral / total * 100, 1),
            "risk_off": round(risk_off / total * 100, 1)
        }

    except Exception as e:
        print("Error macro_forecast:", e)
        return {"risk_on": 33.3, "neutral": 33.3, "risk_off": 33.4}