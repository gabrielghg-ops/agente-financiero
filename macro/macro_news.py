import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_telegram(mensaje):

    if TELEGRAM_TOKEN is None or TELEGRAM_CHAT_ID is None:
        print("Telegram no configurado")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    limite = 4000

    partes = [mensaje[i:i+limite] for i in range(0, len(mensaje), limite)]

    for parte in partes:

        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": parte
        }

        try:
            r = requests.post(url, json=data)

            if r.status_code != 200:
                print("Error enviando telegram:", r.text)

        except Exception as e:
            print("Error telegram:", e)