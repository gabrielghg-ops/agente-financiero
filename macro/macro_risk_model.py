import yfinance as yf
import pandas as pd


def _get_close_series(data):
    """
    Convierte la columna Close en una serie limpia.
    Evita errores de Series/DataFrame de yfinance.
    """

    if data is None or data.empty:
        return pd.Series(dtype="float64")

    close = data["Close"]

    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    return pd.to_numeric(close, errors="coerce").dropna()


def calcular_risk_score(riesgo_noticias):

    score = 0

    try:
        spy = yf.download("SPY", period="6mo", interval="1d", progress=False)
        vix = yf.download("^VIX", period="6mo", interval="1d", progress=False)
        dxy = yf.download("DX-Y.NYB", period="6mo", interval="1d", progress=False)
        gold = yf.download("GLD", period="6mo", interval="1d", progress=False)

        spy_close = _get_close_series(spy)
        vix_close = _get_close_series(vix)
        dxy_close = _get_close_series(dxy)
        gold_close = _get_close_series(gold)

        if len(spy_close) < 50:
            return 50

        spy_price = float(spy_close.iloc[-1])
        spy_ma50 = spy_close.rolling(50).mean().iloc[-1]

        if spy_price < spy_ma50:
            score += 25

        if len(vix_close) > 0:
            vix_value = float(vix_close.iloc[-1])

            if vix_value > 25:
                score += 20

        if len(dxy_close) >= 2:
            dxy_return = (float(dxy_close.iloc[-1]) / float(dxy_close.iloc[0])) - 1

            if dxy_return > 0.03:
                score += 15

        if len(gold_close) >= 50:
            gold_price = float(gold_close.iloc[-1])
            gold_ma50 = gold_close.rolling(50).mean().iloc[-1]

            if gold_price > gold_ma50:
                score += 10

        score += riesgo_noticias

        score = min(score, 100)

        return score

    except Exception as e:

        print("Error calculando risk score:", e)

        return 50