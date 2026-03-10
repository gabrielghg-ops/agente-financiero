def generar_conclusion(datos, interpretacion, risk_score, risk_mode):

    vix = datos.get("vix", 0)
    us10y = datos.get("us10y", 0)

    conclusion = "\n📈 CONCLUSION ESTRATEGICA\n"

    conclusion += f"\nGlobal Risk Score: {risk_score}/100"
    conclusion += f"\nModo de mercado: {risk_mode}\n"

    if risk_mode == "RISK ON":

        conclusion += """
El entorno macro muestra condiciones favorables para activos de riesgo.

Recomendación:
- Mayor exposición a acciones
- Favorecer índices
- Crypto favorecida
- Menor necesidad de refugio en oro
"""

    elif risk_mode == "RISK OFF":

        conclusion += """
El entorno macro muestra señales defensivas.

Recomendación:
- Reducir exposición a acciones
- Favorecer activos refugio
- Mayor cautela en crypto
- Priorizar liquidez
"""

    else:

        conclusion += """
El entorno macro es mixto o incierto.

Recomendación:
- Mantener exposición moderada
- Seleccionar activos con tendencia clara
- Evitar sobreexposición
"""

    if vix > 30:
        conclusion += "\n⚠ Volatilidad elevada detectada."

    if us10y > 4.7:
        conclusion += "\n⚠ Tasas elevadas pueden presionar activos de riesgo."

    return conclusion