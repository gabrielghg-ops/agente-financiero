def detectar_alertas_macro(datos):

    alertas = []

    vix = datos.get("vix", 0)
    dxy = datos.get("dxy", 0)
    us10y = datos.get("us10y", 0)

    # volatilidad extrema
    if vix > 30:
        alertas.append(
            "🚨 Volatilidad extrema detectada (VIX > 30). Posible estrés en mercados."
        )

    # mercado muy complaciente
    if vix < 12:
        alertas.append(
            "⚠ Volatilidad muy baja (VIX < 12). Mercado complaciente."
        )

    # dolar fuerte
    if dxy > 105:
        alertas.append(
            "💵 Dólar muy fuerte. Presión bajista sobre activos de riesgo."
        )

    # tasas altas
    if us10y > 4.7:
        alertas.append(
            "📉 Tasas del bono 10Y elevadas. Liquidez global restringida."
        )

    return alertas