import yfinance as yf
import pandas as pd
import requests
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

tickers = [
"SPY","MELI","GOOGL","GLD","SLV","IBIT",
"EWZ","EEM","PAMP","YPF"
]

def rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100/(1+rs))

def analizar_tecnico(ticker):

    df = yf.download(ticker, period="3mo")

    df["RSI"] = rsi(df["Close"])

    last = df.iloc[-1]

    if last["RSI"] < 35:
        signal="COMPRA"
    elif last["RSI"] > 70:
        signal="VENTA"
    else:
        signal="MANTENER"

    return {
        "ticker":ticker,
        "price":round(last["Close"],2),
        "rsi":round(last["RSI"],1),
        "signal":signal
    }

def analizar_noticias():

    prompt="""
    Resume las noticias financieras globales
    y su impacto probable en los mercados.
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text

report="📊 REPORTE FINANCIERO DIARIO\n\n"

for t in tickers:

    r=analizar_tecnico(t)

    report+=f"""
{r['ticker']}
Precio: {r['price']}
RSI: {r['rsi']}
Señal: {r['signal']}

"""

news=analizar_noticias()

report+="\nNoticias y macro:\n"
report+=news

url=f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

requests.post(url,data={
"chat_id":CHAT_ID,
"text":report
})