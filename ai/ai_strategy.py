import os

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


def generar_estrategia_ia(macro, resultados, noticias, theme_summary=None):
    """
    Genera una estrategia de mercado usando:
    - datos macro
    - análisis de cartera
    - noticias
    - tema dominante de mercado (opcional)

    Devuelve texto listo para agregar al reporte.
    """

    macro = macro or {}
    resultados = resultados or []
    noticias = noticias or "Sin noticias relevantes"
    theme_summary = theme_summary or ""

    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key or OpenAI is None:
        return estrategia_fallback(macro, resultados, noticias, theme_summary)

    resumen_cartera = construir_resumen_cartera(resultados)

    system_prompt = (
        "Eres un analista macro-financiero institucional. "
        "Tu tarea es generar una estrategia clara, breve y accionable en español. "
        "Debes priorizar gestión de riesgo, contexto macro, rotación sectorial y protección de capital. "
        "No inventes datos. Usa solamente la información proporcionada. "
        "El tono debe ser profesional, directo y útil para un reporte automatizado."
    )

    user_prompt = f"""
Analiza la siguiente información y genera una estrategia de mercado en español.

DATOS MACRO:
{macro}

NOTICIAS:
{noticias}

TEMA DOMINANTE DEL MERCADO:
{theme_summary if theme_summary else "No disponible"}

CARTERA ANALIZADA:
{resumen_cartera}

Quiero que respondas con este formato:

1. SESGO GENERAL
- Una conclusión breve del entorno actual

2. QUÉ FAVORECER
- Tipos de activos, sectores o estilos que conviene priorizar

3. QUÉ EVITAR O REDUCIR
- Riesgos, sectores o activos que conviene evitar

4. ACCIÓN PRÁCTICA
- Qué haría un gestor prudente en este contexto

Sé concreto. No uses relleno. Máximo 220 palabras.
"""

    try:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
            max_tokens=350,
        )

        content = response.choices[0].message.content

        if content and str(content).strip():
            return content.strip()

        return estrategia_fallback(macro, resultados, noticias, theme_summary)

    except Exception as e:
        print("Error OpenAI en estrategia IA:", e)
        return estrategia_fallback(macro, resultados, noticias, theme_summary)


def construir_resumen_cartera(resultados):
    """
    Convierte la cartera analizada en un resumen simple para el prompt.
    """
    if not resultados:
        return "No hay activos analizados en cartera."

    lineas = []

    for r in resultados:
        ticker = r.get("ticker", "N/D")
        price = r.get("price", "N/D")
        ma50 = r.get("ma50", "N/D")
        signal = r.get("signal", "N/D")

        lineas.append(
            f"- {ticker} | Precio: {price} | MA50: {ma50} | Señal: {signal}"
        )

    return "\n".join(lineas)


def estrategia_fallback(macro, resultados, noticias, theme_summary=""):
    """
    Estrategia simple de respaldo si OpenAI falla o no está configurado.
    """
    theme_text = (theme_summary or "").lower()

    alcistas = 0
    bajistas = 0

    for r in resultados or []:
        signal = str(r.get("signal", "")).lower()

        if "alc" in signal or "bull" in signal:
            alcistas += 1
        elif "baj" in signal or "bear" in signal:
            bajistas += 1

    vix = extraer_numero(macro.get("VIX", 0))
    dxy = extraer_numero(macro.get("DXY", 0))
    oro = extraer_numero(macro.get("ORO", 0))
    petroleo = extraer_numero(macro.get("PETROLEO", 0))

    bias = "NEUTRAL"
    favorecer = []
    evitar = []
    accion = []

    if "risk off" in theme_text or vix >= 22 or "flight to safety" in theme_text:
        bias = "Defensivo / Risk Off"
        favorecer.extend(["liquidez", "oro", "exposición defensiva", "gestión de riesgo"])
        evitar.extend(["tecnología agresiva", "activos muy volátiles", "sobreexposición a beta alta"])
        accion.append("Reducir exposición táctica en activos de alto riesgo.")
        accion.append("Priorizar preservación de capital y entradas selectivas.")

    elif "inflación" in theme_text or petroleo > 80:
        bias = "Inflacionario / Selectivo"
        favorecer.extend(["energía", "commodities", "metales", "activos reales"])
        evitar.extend(["bonos largos", "crecimiento muy sensible a tasas"])
        accion.append("Favorecer sectores vinculados a materias primas.")
        accion.append("Evitar sobrecargar posiciones sensibles a tasas largas.")

    elif "tecnológico" in theme_text or "ai" in theme_text:
        bias = "Risk On con liderazgo tecnológico"
        favorecer.extend(["tecnología", "semiconductores", "crecimiento líder"])
        evitar.extend(["sectores rezagados sin momentum"])
        accion.append("Mantener exposición selectiva en liderazgo tecnológico.")
        accion.append("Evitar perseguir activos extendidos sin confirmación.")

    else:
        bias = "Neutral / Mixto"
        favorecer.extend(["selectividad", "diversificación", "seguimiento de tendencia"])
        evitar.extend(["concentración excesiva", "operaciones impulsivas"])
        accion.append("Esperar confirmación antes de aumentar riesgo.")
        accion.append("Mantener cartera balanceada y revisar fortaleza relativa.")

    if bajistas > alcistas:
        accion.append("La cartera muestra más debilidad que fortaleza; conviene revisar posiciones débiles.")
    elif alcistas > bajistas:
        accion.append("La cartera mantiene mejor tono interno; se puede sostener exposición con control de riesgo.")

    if dxy >= 104:
        evitar.append("emergentes débiles frente a dólar fuerte")

    if oro and oro > 0 and ("risk off" in theme_text or "inflación" in theme_text):
        if "oro" not in favorecer:
            favorecer.append("oro")

    favorecer = unique_keep_order(favorecer)
    evitar = unique_keep_order(evitar)
    accion = unique_keep_order(accion)

    texto = []
    texto.append("1. SESGO GENERAL")
    texto.append(f"- {bias}. El contexto combina macro, cartera y narrativa de mercado.")
    texto.append("")
    texto.append("2. QUÉ FAVORECER")
    texto.append(f"- {', '.join(favorecer) if favorecer else 'Selectividad y gestión activa.'}")
    texto.append("")
    texto.append("3. QUÉ EVITAR O REDUCIR")
    texto.append(f"- {', '.join(evitar) if evitar else 'Exposición excesiva sin confirmación macro.'}")
    texto.append("")
    texto.append("4. ACCIÓN PRÁCTICA")
    for a in accion[:3]:
        texto.append(f"- {a}")

    return "\n".join(texto)


def extraer_numero(value, default=0.0):
    try:
        if isinstance(value, str):
            value = value.replace("%", "").replace(",", "").strip()
        return float(value)
    except Exception:
        return default


def unique_keep_order(items):
    seen = set()
    result = []

    for item in items:
        key = str(item).strip().lower()
        if key and key not in seen:
            seen.add(key)
            result.append(item)

    return result