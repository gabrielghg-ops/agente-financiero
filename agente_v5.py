import time
from cartera_reader import obtener_cartera
from oportunidades import analizar_activo
from macro import analizar_macro
from noticias import analizar_noticias


def run_agent():

    print("===== AGENTE FINANCIERO V5 =====")

    cartera = obtener_cartera()

    print(f"Activos detectados: {cartera}")

    for ticker in cartera:

        try:

            print(f"\nAnalizando {ticker}")

            resultado = analizar_activo(ticker)

            if resultado:
                print(f"Oportunidad detectada en {ticker}")

        except Exception as e:
            print(f"Error analizando {ticker}: {e}")

    analizar_macro()

    analizar_noticias()

    print("\nAgente finalizado")


if __name__ == "__main__":

    while True:

        run_agent()

        print("\nEsperando 6 horas...\n")

        time.sleep(21600)