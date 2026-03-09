from macro.macro_market import obtener_datos_macro
from macro.macro_news import resumen_noticias
from macro.macro_correlation import interpretar_macro
from macro.macro_alerts import detectar_alertas_macro
from macro.macro_risk_score import calcular_risk_score
from macro.macro_conclusion import generar_conclusion


def analizar_macro_global():

    try:

        datos = obtener_datos_macro()

        interpretacion = interpretar_macro(datos)

        alertas = detectar_alertas_macro(datos)

        noticias = resumen_noticias()

        risk_score, risk_mode = calcular_risk_score(datos)

        conclusion = generar_conclusion(
            datos,
            interpretacion,
            risk_score,
            risk_mode
        )

        vix = datos.get("vix", 0)
        dxy = datos.get("dxy", 0)
        us10y = datos.get("us10y", 0)
        gold = datos.get("gold", "?")
        oil = datos.get("oil", "?")

        sp_trend = datos.get("sp_trend", "?")
        nasdaq_trend = datos.get("nasdaq_trend", "?")

        reporte = f"""
🌍 ANALISIS MACRO GLOBAL

VIX: {vix:.2f}
DXY: {dxy:.2f}
US10Y: {us10y:.2f}

Oro: {gold}
Petróleo: {oil}

Tendencia SP500: {sp_trend}
Tendencia NASDAQ: {nasdaq_trend}

Condiciones del mercado:
Riesgo: {interpretacion.get('riesgo')}
Dólar: {interpretacion.get('dolar')}
Liquidez: {interpretacion.get('liquidez')}

Sentimiento global: {interpretacion.get('sentimiento')}

🌐 GLOBAL RISK SCORE: {risk_score}/100
Modo mercado: {risk_mode}
"""

        if alertas:

            reporte += "\n🚨 ALERTAS MACRO:\n"

            for alerta in alertas:

                reporte += f"- {alerta}\n"

        reporte += f"\n{noticias}"

        reporte += conclusion

        return reporte

    except Exception as e:

        return f"Error en análisis macro: {e}"