def generar_estrategia(macro, noticias):

    estrategia = ""

    if "volatilidad" in macro.lower():

        estrategia += "Mercado en fase de riesgo elevado\n"
        estrategia += "Priorizar activos defensivos\n"

    if "inflacion" in noticias.lower():

        estrategia += "Favorecer commodities y energia\n"

    if estrategia == "":
        estrategia = "Mercado estable, mantener diversificación"

    return estrategia