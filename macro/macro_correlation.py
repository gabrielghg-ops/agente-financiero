def interpretar_macro(datos):

    vix = datos.get("vix", 0)
    dxy = datos.get("dxy", 0)
    us10y = datos.get("us10y", 0)

    # Sentimiento de mercado segun volatilidad

    if vix < 15:
        riesgo = "bajo"
    elif vix < 25:
        riesgo = "moderado"
    else:
        riesgo = "alto"

    # Fuerza del dolar

    if dxy > 104:
        dolar = "fuerte"
    elif dxy < 100:
        dolar = "debil"
    else:
        dolar = "neutral"

    # Condiciones de liquidez segun tasas

    if us10y > 4.5:
        liquidez = "restrictiva"
    elif us10y < 3.5:
        liquidez = "expansiva"
    else:
        liquidez = "normal"

    # Sesgo general de mercado

    if riesgo == "bajo" and dolar != "fuerte":
        sentimiento = "RISK ON"

    elif riesgo == "alto":
        sentimiento = "RISK OFF"

    else:
        sentimiento = "NEUTRAL"

    return {
        "riesgo": riesgo,
        "dolar": dolar,
        "liquidez": liquidez,
        "sentimiento": sentimiento
    }