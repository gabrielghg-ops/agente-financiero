import requests
import yfinance as yf
from openai import OpenAI

# ==============================
# CONFIGURACIÓN
# ==============================

TELEGRAM_TOKEN = "8618097270:AAEEO0LqKcucsQgcVMMbLkmF76Uuvoh81zU"
CHAT_ID = "7703343025"
OPENAI_API_KEY = "OPENAI_API_KEY"

client = OpenAI(api_key=OPENAI_API_KEY)

# ETFs a analizar
tickers = ["SPY", "QQQ", "DIA", "XLK", "SLV"]

# ==============================
# FUNCIONES
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
    Actúa como un analista financiero profesional.
    Analiza estos ETFs y da un resumen claro, profesional y breve.
    Incluye interpretación del mercado y posibles implicancias.

    Datos:
    {datos}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un analista financiero experto."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }

    requests.post(url, data=payload)


# ==============================
# EJECUCIÓN
# ==============================

if __name__ == "__main__":
    datos = obtener_datos()
    analisis = analizar_con_ia(datos)
    enviar_telegram(analisis)
    
    print("Mensaje enviado correctamente 🚀")