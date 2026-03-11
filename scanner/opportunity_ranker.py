def rank_opportunities(scanner_results):

    ranked = []

    for ticker, score in scanner_results:

        if score >= 8:
            label = "FUERTE"

        elif score >= 5:
            label = "INTERESANTE"

        else:
            label = "DEBIL"

        ranked.append({
            "ticker": ticker,
            "score": score,
            "nivel": label
        })

    return ranked