from macro.macro_market import obtener_datos_macro
from macro.macro_news import resumen_noticias
from macro.macro_correlation import interpretar_macro


def analizar_macro_global():

    datos = obtener_datos_macro()

    interpretacion = interpretar_macro(datos)

    noticias = resumen_noticias()

    reporte = f"""
ANALISIS MACRO GLOBAL

VIX: {datos['vix']:.2f}
DXY: {datos['dxy']:.2f}
US10Y: {datos['us10y']:.2f}

Tendencia SP500: {datos['sp_trend']}
Tendencia NASDAQ: {datos['nasdaq_trend']}

Sentimiento: {interpretacion['sentimiento']}
Liquidez: {interpretacion['liquidez']}

{noticias}
"""

    return reporte