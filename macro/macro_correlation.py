import yfinance as yf


def analizar_correlaciones():

    try:

        spy = yf.download("SPY", period="3mo")
        gold = yf.download("GC=F", period="3mo")
        vix = yf.download("^VIX", period="3mo")

        if spy.empty or gold.empty or vix.empty:
            return "No hay suficientes datos para correlaciones"

        spy_ret = spy["Close"].pct_change().dropna()
        gold_ret = gold["Close"].pct_change().dropna()
        vix_ret = vix["Close"].pct_change().dropna()

        corr_gold = float(spy_ret.corr(gold_ret))
        corr_vix = float(spy_ret.corr(vix_ret))

        texto = ""

        if corr_gold < -0.2:
            texto += "Flujo hacia activos refugio (oro)\n"

        if corr_vix < -0.2:
            texto += "Mercado sensible al riesgo (VIX inverso)\n"

        if texto == "":
            texto = "Correlaciones normales de mercado"

        return texto

    except Exception as e:

        print("Error correlaciones:", e)

        return "No se pudieron calcular correlaciones"