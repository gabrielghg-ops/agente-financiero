def calcular_risk_score(datos):

    score = 50

    vix = datos.get("vix", 0)
    dxy = datos.get("dxy", 0)
    us10y = datos.get("us10y", 0)

    # volatilidad

    if vix < 15:
        score += 15
    elif vix > 25:
        score -= 15

    # dolar

    if dxy > 105:
        score -= 10
    elif dxy < 100:
        score += 10

    # tasas

    if us10y > 4.5:
        score -= 10
    elif us10y < 3.5:
        score += 10

    if score > 100:
        score = 100

    if score < 0:
        score = 0

    if score >= 65:
        modo = "RISK ON"

    elif score <= 35:
        modo = "RISK OFF"

    else:
        modo = "NEUTRAL"

    return score, modo