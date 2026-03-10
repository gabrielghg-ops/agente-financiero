def analizar_correlaciones(datos):

    texto = ""

    try:

        if datos["vix"] > 25:
            texto += "Alta volatilidad en mercado\n"

        if datos["dxy"] > 105:
            texto += "Dolar fuerte presiona emergentes\n"

        if datos["gold"] > 2300:
            texto += "Flujo hacia activos refugio\n"

        if datos["oil"] > 90:
            texto += "Riesgo inflacionario por energia\n"

    except:
        texto = "Sin datos suficientes"

    return texto