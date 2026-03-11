def generar_estrategia_ia(macro, cartera, noticias):

    texto = ""

    if "iran" in noticias.lower() or "war" in noticias.lower():

        texto += "⚠ Riesgo geopolítico detectado en noticias\n"
        texto += "Mercados pueden volverse volátiles\n"
        texto += "Reducir exposición a riesgo\n\n"

    if "inflation" in noticias.lower():

        texto += "Inflación relevante en noticias\n\n"

    bajistas = 0
    alcistas = 0

    for a in cartera:

        if a["signal"] == "alcista":
            alcistas += 1

        if a["signal"] == "bajista":
            bajistas += 1

    if bajistas > alcistas:

        texto += "Mercado defensivo\n"
        texto += "Priorizar liquidez y activos refugio\n"

    else:

        texto += "Mercado con momentum positivo\n"
        texto += "Se pueden buscar oportunidades\n"

    return texto