def generar_estrategia(macro, noticias):

    estrategia = ""

    if "RISK_ON" in macro:

        estrategia += """
📈 Estrategia sugerida

Mercado en modo RISK ON.

Sugerencias:
- Priorizar acciones de crecimiento
- Tecnología y semiconductores
- Reducir exposición a oro
"""

    elif "RISK_OFF" in macro:

        estrategia += """
⚠ Estrategia defensiva

Mercado en modo RISK OFF.

Sugerencias:
- Aumentar liquidez
- Considerar oro
- Reducir exposición a acciones cíclicas
"""

    else:

        estrategia += """
📊 Estrategia neutral

Mercado sin dirección clara.

Sugerencias:
- Mantener cartera diversificada
- Esperar confirmaciones de tendencia
"""

    if "inflation" in str(noticias).lower():

        estrategia += "\n⚠ Riesgo inflacionario detectado en noticias."

    if "war" in str(noticias).lower():

        estrategia += "\n⚠ Riesgo geopolítico detectado."

    return estrategia