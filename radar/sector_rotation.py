import yfinance as yf

SECTORS = {
    "Tecnologia": "XLK",
    "Finanzas": "XLF",
    "Energia": "XLE",
    "Salud": "XLV",
    "Industria": "XLI",
    "Consumo": "XLY",
    "Defensivo": "XLP"
}

def sector_rotation():

    results = {}

    for sector, ticker in SECTORS.items():

        data = yf.download(ticker, period="3mo")

        perf = (data["Close"].iloc[-1] / data["Close"].iloc[0]) - 1

        results[sector] = round(perf * 100, 2)

    sorted_sectors = sorted(results.items(), key=lambda x: x[1], reverse=True)

    return sorted_sectors