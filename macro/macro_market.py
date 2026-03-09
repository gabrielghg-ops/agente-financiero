import yfinance as yf

def obtener_datos_macro():

    vix = yf.Ticker("^VIX").history(period="1d")["Close"].iloc[-1]
    dxy = yf.Ticker("DX-Y.NYB").history(period="1d")["Close"].iloc[-1]
    sp500 = yf.Ticker("^GSPC").history(period="5d")["Close"]
    nasdaq = yf.Ticker("^IXIC").history(period="5d")["Close"]
    gold = yf.Ticker("GC=F").history(period="1d")["Close"].iloc[-1]
    oil = yf.Ticker("CL=F").history(period="1d")["Close"].iloc[-1]
    us10y = yf.Ticker("^TNX").history(period="1d")["Close"].iloc[-1]

    tendencia_sp = "alcista" if sp500.iloc[-1] > sp500.mean() else "bajista"
    tendencia_nasdaq = "alcista" if nasdaq.iloc[-1] > nasdaq.mean() else "bajista"

    return {
        "vix": vix,
        "dxy": dxy,
        "us10y": us10y,
        "gold": gold,
        "oil": oil,
        "sp_trend": tendencia_sp,
        "nasdaq_trend": tendencia_nasdaq
    }