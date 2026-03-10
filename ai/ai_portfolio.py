def analizar_cartera_ia(resultados):

    if not resultados:

        return "No hay datos de cartera"

    alcistas = 0
    bajistas = 0

    precios = []

    for r in resultados:

        precios.append(r["price"])

        if r["signal"] == "alcista":
            alcistas += 1
        else:
            bajistas += 1

    texto = ""

    texto += f"Activos analizados: {len(resultados)}\n"
    texto += f"Alcistas: {alcistas}\n"
    texto += f"Bajistas: {bajistas}\n"

    if alcistas > bajistas:

        texto += "\nTendencia general positiva\n"

    else:

        texto += "\nTendencia general débil\n"

    return texto