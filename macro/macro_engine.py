from macro.macro_news import resumen_noticias
from macro.macro_risk_score import calcular_risk_score
from macro.macro_conclusion import generar_conclusion


def analizar_macro_global():

    print("Analizando entorno macroeconómico...")

    report = ""

    score = calcular_risk_score()

    report += f"Risk Score Global: {score}/100\n\n"

    noticias = resumen_noticias()

    report += "Noticias Macro:\n"
    report += noticias
    report += "\n\n"

    conclusion = generar_conclusion(score)

    report += conclusion

    return report