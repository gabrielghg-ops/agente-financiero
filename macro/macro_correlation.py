import yfinance as yf
import pandas as pd


def analizar_correlaciones():

    try:

        spy = yf.download("SPY", period="3mo")
        gold = yf.download("GC=F", period="3mo")
        vix = yf.download("^VIX", period="3mo")

        # Verificar datos
        if spy.empty or gold.empty or vix.empty:
            return "Datos insuficientes para calcular correlaciones"

        # Retornos
        spy_ret = spy["Close"].pct_change()
        gold_ret = gold["Close"].pct_change()
        vix_ret = vix["Close"].pct_change()

        # Unir series para evitar desalineaciones
        df = pd.concat([spy_ret, gold_ret, vix_ret], axis=1)
        df.columns = ["spy", "gold", "vix"]
        df = df.dropna()

        if df.empty:
            return "Datos insuficientes para correlaciones"

        corr_gold = float(df["spy"].corr(df["gold"]))
        corr_vix = float(df["spy"].corr(df["vix"]))

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