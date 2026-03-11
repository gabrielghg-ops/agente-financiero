def generar_informe_final(macro, radar, cartera, risk_score, crash, noticias):

    texto = "\n\n📊 INFORME DE MERCADO\n\n"

    # entorno
    if risk_score > 70:
        entorno = "RISK OFF"
    elif risk_score > 40:
        entorno = "NEUTRAL"
    else:
        entorno = "RISK ON"

    texto += f"Entorno de mercado: {entorno}\n\n"

    texto += (
        "El mercado muestra un entorno de mayor cautela impulsado "
        "principalmente por factores macroeconómicos y geopolíticos. "
        "La volatilidad permanece elevada y el capital está rotando "
        "hacia activos defensivos.\n\n"
    )

    # estado cartera
    alcistas = sum(1 for a in cartera if a["signal"] == "alcista")
    bajistas = sum(1 for a in cartera if a["signal"] == "bajista")

    total = len(cartera)

    if total > 0:
        texto += f"En la cartera analizada {alcistas} activos muestran tendencia alcista y {bajistas} bajista.\n\n"

    # recomendaciones simples
    texto += "Rotación sugerida:\n"

    texto += (
        "- Reducir exposición en tecnología o activos de crecimiento si pierden momentum (ej: XLK, SPY).\n"
        "- Reducir exposición en cripto o ETF vinculados a bitcoin si mantienen debilidad (ej: IBIT).\n"
        "- Favorecer metales preciosos o refugios si continúan fuertes (ej: GLD, SLV).\n"
        "- Mantener atención en energía y materias primas si persiste presión inflacionaria.\n"
    )

    return texto