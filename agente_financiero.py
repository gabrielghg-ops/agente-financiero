import requests
import yfinance as yf
import os
from openai import OpenAI

# ==============================
# VARIABLES DE ENTORNO
# ==============================

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

tickers = ["SPY", "QQQ", "DIA", "XLK", "SLV"]

# ==============================

def obtener_datos():
    datos = {}

    for ticker in tickers:
        activo = yf.Ticker(ticker)
        hist = activo.history(period="1d")

        if not hist.empty:
            precio = hist["Close"].iloc[-1]
            apertura = hist["Open"].iloc[-1]
            variacion = ((precio - apertura) / apertura) * 100

            datos[ticker] = {
                "precio": round(precio, 2),
                "variacion": round(variacion, 2)
            }

    return datos


def analizar_con_ia(datos):

    prompt = f"""
Analiza estos ETFs y resume la situación del mercado:

{datos}

Explica brevemente tendencias y riesgos.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un analista financiero experto."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def enviar_telegram(mensaje):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje
    }

    requests.post(url, data=payload)


# ==============================

if __name__ == "__main__":

    datos = obtener_datos()
    analisis = analizar_con_ia(datos)

    enviar_telegram(analisis)

    print("Mensaje enviado correctamente 🚀")