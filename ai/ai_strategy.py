def generar_estrategia_ia(macro, resultados, noticias):

    texto = ""

    noticias_lower = noticias.lower()

    if "war" in noticias_lower or "conflict" in noticias_lower or "attack" in noticias_lower:

        texto += "⚠ Riesgo geopolítico detectado en noticias\n"
        texto += "Mercados pueden volverse volátiles\n"
        texto += "Reducir exposición a riesgo\n\n"

    if "inflation" in noticias_lower:

        texto += "Inflación relevante en noticias\n\n"

    if "RISK ON" in macro:

        texto += "Mercado favorable para riesgo\n"

    if "RISK OFF" in macro:

        texto += "Mercado defensivo\n"

    return texto