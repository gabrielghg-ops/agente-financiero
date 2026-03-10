def generar_estrategia_ia(macro, resultados, noticias):

    texto = ""

    if "RISK ON" in macro:

        texto += "Mercado favorable para riesgo\n"
        texto += "Aumentar exposición a acciones\n"

    if "RISK OFF" in macro:

        texto += "Mercado defensivo\n"
        texto += "Reducir exposición a acciones\n"

    if "inflación" in noticias.lower():

        texto += "Inflación relevante en noticias\n"

    return texto