from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def analizar_noticias():

    prompt = """
    Resume las noticias financieras globales del momento
    y explica el impacto probable en los mercados.
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text