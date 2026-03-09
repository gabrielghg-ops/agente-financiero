import yfinance as yf

def analizar_macro():

    try:

        vix = yf.Ticker("^VIX").history(period="1d")["Close"].iloc[-1]
        dxy = yf.Ticker("DX-Y.NYB").history(period="1d")["Close"].iloc[-1]
        sp500 = yf.Ticker("^GSPC").history(period="5d")["Close"]
        us10y = yf.Ticker("^TNX").history(period="1d")["Close"].iloc[-1]
        gold = yf.Ticker("GC=F").history(period="1d")["Close"].iloc[-1]

        # tendencia SP500
        if sp500.iloc[-1] > sp500.mean():
            sp_trend = "alcista"
        else:
            sp_trend = "bajista"

        # riesgo segun VIX
        if vix < 15:
            riesgo = "bajo"
        elif vix < 25:
            riesgo = "moderado"
        else:
            riesgo = "alto"

        # interpretación del dólar
        if dxy > 104:
            dolar = "fuerte (presión bajista en activos)"
        else:
            dolar = "débil o neutral"

        macro = f"""
ANÁLISIS MACRO GLOBAL

Volatilidad (VIX): {vix:.2f} → Riesgo {riesgo}

Dólar (DXY): {dxy:.2f} → {dolar}

Bonos USA 10Y: {us10y:.2f}%

Oro: {gold:.0f}

Tendencia S&P500: {sp_trend}

Interpretación:
- Liquidez global condicionada por tasas.
- Sentimiento del mercado: {riesgo}.
- Contexto para trading: mercado {sp_trend}.
"""

        return macro

    except Exception as e:
        return f"Error obteniendo datos macro: {e}"