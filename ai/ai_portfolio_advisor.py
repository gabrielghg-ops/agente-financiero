def analizar_cartera(activos):

    if not activos:
        return "Sin datos de cartera"

    alcistas = 0
    bajistas = 0

    for a in activos:

        if a.get("signal") == "alcista":
            alcistas += 1
        else:
            bajistas += 1

    texto = f"""
Activos alcistas: {alcistas}
Activos bajistas: {bajistas}
"""

    if bajistas > alcistas:
        texto += "Reducir exposición en renta variable"

    else:
        texto += "Cartera con sesgo positivo"

    return texto