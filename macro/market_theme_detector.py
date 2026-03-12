def detectar_market_theme(macro, noticias_texto, sectors):
    """
    Detecta el tema dominante del mercado a partir de:
    - datos macro
    - noticias
    - rotación sectorial

    Devuelve un dict listo para integrar al reporte y a la IA.
    """

    macro = macro or {}
    noticias = (noticias_texto or "").lower()
    sectors = sectors or []

    # -------------------------
    # Helpers
    # -------------------------
    def safe_float(value, default=0):
        try:
            if isinstance(value, str):
                value = value.replace("%", "").replace(",", "").strip()
            return float(value)
        except:
            return default

    def contains_any(text, words):
        return any(w in text for w in words)

    # -------------------------
    # Datos macro base
    # -------------------------
    spy = safe_float(macro.get("SPY", 0))
    vix = safe_float(macro.get("VIX", 0))
    dxy = safe_float(macro.get("DXY", 0))
    oro = safe_float(macro.get("ORO", 0))
    petroleo = safe_float(macro.get("PETROLEO", 0))

    # -------------------------
    # Ranking sectorial
    # sectors esperado:
    # [("Tecnologia", 3.2), ("Energia", 1.8), ...]
    # -------------------------
    top_sector = sectors[0][0] if len(sectors) > 0 else ""
    top_perf = safe_float(sectors[0][1], 0) if len(sectors) > 0 else 0

    second_sector = sectors[1][0] if len(sectors) > 1 else ""
    second_perf = safe_float(sectors[1][1], 0) if len(sectors) > 1 else 0

    weak_sector = sectors[-1][0] if len(sectors) > 0 else ""
    weak_perf = safe_float(sectors[-1][1], 0) if len(sectors) > 0 else 0

    # -------------------------
    # Scores temáticos
    # -------------------------
    scores = {
        "inflacion_persistente": 0,
        "risk_off_macro": 0,
        "risk_on_growth": 0,
        "boom_energia_materias_primas": 0,
        "flight_to_safety": 0,
        "debilidad_emergentes_dolar_fuerte": 0,
        "liderazgo_tecnologico_ai": 0,
    }

    drivers_map = {k: [] for k in scores.keys()}

    # -------------------------
    # Reglas macro
    # -------------------------

    # Inflación persistente
    if petroleo > 80:
        scores["inflacion_persistente"] += 20
        drivers_map["inflacion_persistente"].append("Petróleo elevado")

    if oro > 0:
        scores["inflacion_persistente"] += 5
        drivers_map["inflacion_persistente"].append("Oro con soporte")

    if contains_any(noticias, [
        "inflation", "inflación", "cpi", "ppi", "fed hawkish",
        "hawkish", "rates higher", "higher for longer", "tipos altos"
    ]):
        scores["inflacion_persistente"] += 35
        drivers_map["inflacion_persistente"].append("Narrativa de inflación / Fed hawkish")

    if top_sector.lower() in ["energia", "materials", "materiales"]:
        scores["inflacion_persistente"] += 15
        drivers_map["inflacion_persistente"].append(f"Liderazgo sectorial en {top_sector}")

    # Risk off macro
    if vix >= 22:
        scores["risk_off_macro"] += 25
        drivers_map["risk_off_macro"].append("VIX elevado")

    if dxy >= 103:
        scores["risk_off_macro"] += 20
        drivers_map["risk_off_macro"].append("Dólar fuerte")

    if contains_any(noticias, [
        "recession", "recesión", "slowdown", "hard landing",
        "geopolitical", "war", "conflict", "crisis", "default"
    ]):
        scores["risk_off_macro"] += 30
        drivers_map["risk_off_macro"].append("Noticias macro defensivas")

    if weak_sector.lower() in ["tecnologia", "consumo", "consumo discrecional"]:
        scores["risk_off_macro"] += 10
        drivers_map["risk_off_macro"].append(f"Debilidad en {weak_sector}")

    # Risk on growth
    if vix < 18:
        scores["risk_on_growth"] += 20
        drivers_map["risk_on_growth"].append("Volatilidad controlada")

    if dxy < 102:
        scores["risk_on_growth"] += 15
        drivers_map["risk_on_growth"].append("Dólar no presiona el mercado")

    if top_sector.lower() in ["tecnologia", "consumo", "industria"]:
        scores["risk_on_growth"] += 20
        drivers_map["risk_on_growth"].append(f"Liderazgo en {top_sector}")

    if contains_any(noticias, [
        "soft landing", "growth", "growth stocks", "bull market",
        "risk on", "liquidity", "rate cuts", "recorte de tasas"
    ]):
        scores["risk_on_growth"] += 30
        drivers_map["risk_on_growth"].append("Narrativa favorable para activos de riesgo")

    # Boom energía / materias primas
    if petroleo > 85:
        scores["boom_energia_materias_primas"] += 30
        drivers_map["boom_energia_materias_primas"].append("Petróleo muy fuerte")

    if top_sector.lower() in ["energia", "materiales"]:
        scores["boom_energia_materias_primas"] += 25
        drivers_map["boom_energia_materias_primas"].append(f"Liderazgo en {top_sector}")

    if contains_any(noticias, [
        "oil", "crude", "commodities", "uranium", "copper",
        "metals", "energy shock", "supply shock"
    ]):
        scores["boom_energia_materias_primas"] += 25
        drivers_map["boom_energia_materias_primas"].append("Noticias favorables para commodities")

    # Flight to safety
    if vix >= 25:
        scores["flight_to_safety"] += 25
        drivers_map["flight_to_safety"].append("VIX muy alto")

    if dxy >= 104:
        scores["flight_to_safety"] += 20
        drivers_map["flight_to_safety"].append("Flujo hacia dólar")

    if oro > 0:
        scores["flight_to_safety"] += 10
        drivers_map["flight_to_safety"].append("Oro como refugio")

    if contains_any(noticias, [
        "fear", "panic", "safe haven", "flight to safety",
        "stress", "banking crisis", "liquidity stress"
    ]):
        scores["flight_to_safety"] += 35
        drivers_map["flight_to_safety"].append("Narrativa de refugio / estrés financiero")

    # Debilidad emergentes / dólar fuerte
    if dxy >= 104:
        scores["debilidad_emergentes_dolar_fuerte"] += 30
        drivers_map["debilidad_emergentes_dolar_fuerte"].append("Dólar global fuerte")

    if contains_any(noticias, [
        "china slowdown", "emerging markets", "capital outflows",
        "yuan", "fx pressure", "dólar fuerte"
    ]):
        scores["debilidad_emergentes_dolar_fuerte"] += 25
        drivers_map["debilidad_emergentes_dolar_fuerte"].append("Presión sobre emergentes")

    # Liderazgo tecnológico / AI
    if top_sector.lower() == "tecnologia":
        scores["liderazgo_tecnologico_ai"] += 30
        drivers_map["liderazgo_tecnologico_ai"].append("Tecnología lidera la rotación")

    if second_sector.lower() == "tecnologia":
        scores["liderazgo_tecnologico_ai"] += 10
        drivers_map["liderazgo_tecnologico_ai"].append("Tecnología sigue fuerte en ranking")

    if contains_any(noticias, [
        "ai", "artificial intelligence", "semiconductors",
        "chips", "nvidia", "cloud", "big tech"
    ]):
        scores["liderazgo_tecnologico_ai"] += 35
        drivers_map["liderazgo_tecnologico_ai"].append("Narrativa AI / semiconductores")

    if vix < 20:
        scores["liderazgo_tecnologico_ai"] += 10
        drivers_map["liderazgo_tecnologico_ai"].append("Entorno de volatilidad moderada")

    # -------------------------
    # Selección del tema dominante
    # -------------------------
    theme_key = max(scores, key=scores.get)
    raw_score = scores[theme_key]

    theme_names = {
        "inflacion_persistente": "Inflación persistente",
        "risk_off_macro": "Risk Off Macro",
        "risk_on_growth": "Risk On / Growth",
        "boom_energia_materias_primas": "Boom de energía y materias primas",
        "flight_to_safety": "Flight to Safety",
        "debilidad_emergentes_dolar_fuerte": "Debilidad de emergentes por dólar fuerte",
        "liderazgo_tecnologico_ai": "Liderazgo tecnológico / AI",
    }

    bias_map = {
        "inflacion_persistente": "NEUTRAL-RISK OFF",
        "risk_off_macro": "RISK OFF",
        "risk_on_growth": "RISK ON",
        "boom_energia_materias_primas": "NEUTRAL",
        "flight_to_safety": "RISK OFF",
        "debilidad_emergentes_dolar_fuerte": "RISK OFF",
        "liderazgo_tecnologico_ai": "RISK ON",
    }

    favored_assets_map = {
        "inflacion_persistente": ["GLD", "XLE", "DBC", "SLV"],
        "risk_off_macro": ["GLD", "IEF", "UUP"],
        "risk_on_growth": ["QQQ", "XLK", "SPY", "IBIT"],
        "boom_energia_materias_primas": ["XLE", "COPX", "URA", "GLD"],
        "flight_to_safety": ["GLD", "UUP", "SHY"],
        "debilidad_emergentes_dolar_fuerte": ["UUP", "GLD"],
        "liderazgo_tecnologico_ai": ["QQQ", "XLK", "SMH", "IBIT"],
    }

    harmed_assets_map = {
        "inflacion_persistente": ["QQQ", "XLK", "TLT"],
        "risk_off_macro": ["QQQ", "EEM", "IBIT"],
        "risk_on_growth": ["UUP", "GLD"],
        "boom_energia_materias_primas": ["XLY", "TLT"],
        "flight_to_safety": ["SPY", "QQQ", "IBIT"],
        "debilidad_emergentes_dolar_fuerte": ["EEM", "EWZ", "FXI"],
        "liderazgo_tecnologico_ai": ["XLE", "XLP"],
    }

    confidence = min(max(raw_score, 15), 95)

    drivers = drivers_map.get(theme_key, [])
    if not drivers:
        drivers = ["Sin drivers dominantes claros"]

    theme_name = theme_names[theme_key]
    bias = bias_map[theme_key]
    favored = favored_assets_map[theme_key]
    harmed = harmed_assets_map[theme_key]

    summary_es = (
        f"El mercado muestra un tema dominante de {theme_name.lower()} "
        f"con sesgo {bias}. Drivers principales: {', '.join(drivers[:3])}."
    )

    return {
        "theme": theme_name,
        "confidence": confidence,
        "bias": bias,
        "drivers": drivers[:5],
        "favored_assets": favored,
        "harmed_assets": harmed,
        "summary_es": summary_es,
        "all_scores": scores
    }