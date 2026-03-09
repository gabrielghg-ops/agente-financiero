import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def generar_informe_ia(macro_texto, cartera_texto):

    try:

        prompt = f"""
Eres un estratega macro financiero profesional.

Analiza el siguiente contexto de mercado y cartera.

CONTEXTO MACRO:
{macro_texto}

CARTERA:
{cartera_texto}

Genera un informe claro que incluya:

1) Diagnóstico de la situación macro global
2) Riesgos principales del mercado
3) Oportunidades potenciales
4) Recomendaciones estratégicas
5) Posibles rotaciones de activos
6) Si conviene aumentar o reducir exposición al riesgo

Sé claro y conciso.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un estratega macro financiero."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error generando informe IA: {e}"