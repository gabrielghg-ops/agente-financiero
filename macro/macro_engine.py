import yfinance as yf
import pandas as pd

from macro.macro_correlation import analizar_correlaciones


def _get_close_series(data):
    if data is None or data.empty:
        return pd.Series(dtype="float64")

    close = data["Close"]

    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    return pd.to_numeric(close, errors="coerce").dropna()


def analizar_macro_global():

    print("Analizando entorno macroeconómico...")

    try:
        spy = yf.download("SPY", period="6mo", interval="1d", progress=False)
        vix = yf.download("^VIX", period="6mo", interval="1d", progress=False)
        dxy = yf.download("DX-Y.NYB", period="6mo", interval="1d", progress=False)
        gold = yf.download("GC=F", period="6mo", interval="1d", progress=False)
        oil = yf.download("CL=F", period="6mo", interval="1d", progress=False)

        spy_close = _get_close_series(spy)
        vix_close = _get_close_series(vix)
        dxy_close = _get_close_series(dxy)
        gold_close = _get_close_series(gold)
        oil_close = _get_close_series(oil)

        if (
            len(spy_close) == 0
            or len(vix_close) == 0
            or len(dxy_close) == 0
            or len(gold_close) == 0
            or len(oil_close) == 0
        ):
            return None

        spy_val = round(float(spy_close.iloc[-1]), 2)
        vix_val = round(float(vix_close.iloc[-1]), 2)
        dxy_val = round(float(dxy_close.iloc[-1]), 2)
        gold_val = round(float(gold_close.iloc[-1]), 2)
        oil_val = round(float(oil_close.iloc[-1]), 2)

        try:
            correlaciones = analizar_correlaciones()
        except Exception as e:
            print("Error correlaciones:", e)
            correlaciones = "No disponibles"

        return {
            "SPY": spy_val,
            "VIX": vix_val,
            "DXY": dxy_val,
            "ORO": gold_val,
            "PETROLEO": oil_val,
            "correlaciones": correlaciones
        }

    except Exception as e:
        print("Error macro:", e)
        return None