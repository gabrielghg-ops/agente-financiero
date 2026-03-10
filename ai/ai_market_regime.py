def detectar_regimen(risk_score):

    if risk_score < 30:

        return "RISK ON"

    elif risk_score < 60:

        return "NEUTRAL"

    else:

        return "RISK OFF"