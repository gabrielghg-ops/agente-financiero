from macro.macro_market import obtener_datos_macro
from macro.macro_news import resumen_noticias
from macro.macro_correlation import interpretar_macro
from macro.macro_alerts import detectar_alertas_macro


def analizar_macro_global():

    try:

        datos = obtener_datos_macro()

        interpretacion = interpretar_macro(datos)

        alertas = detectar_alertas_macro(datos)

        noticias = resumen_noticias()

        reporte = f"""
🌍 ANALISIS MACRO GLOBAL

VIX: {datos.get('vix','?'):.2f}
DXY: {datos.get('dxy','?'):.2f}
US10Y: {datos.get('us10y','?'):.2f}

Oro: {datos.get('gold','?')}
Petróleo: {datos.get('oil','?')}

Tendencia SP500: {datos.get('sp_trend','?')}
Tendencia NASDAQ: {datos.get('nasdaq_trend','?')}

Condiciones del mercado:
Riesgo: {interpretacion.get('riesgo')}
Dólar: {interpretacion.get('dolar')}
Liquidez: {interpretacion.get('liquidez')}

Sentimiento global: {interpretacion.get('sentimiento')}
"""

        if alertas:

            reporte += "\n🚨 ALERTAS MACRO:\n"

            for alerta in alertas:

                reporte += f"- {alerta}\n"

        reporte += f"\n{noticias}"

        return reporte

    except Exception as e:

        return f"Error en análisis macro: {e}"