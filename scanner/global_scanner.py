import yfinance as yf

ASSETS = [
    "NVDA","MSFT","AAPL","AMD","META",
    "GLD","SLV","COPX","URA",
    "XLE","XLK","EEM","EWZ","IBIT"
]

def scan_assets():

    results = []

    for ticker in ASSETS:

        try:

            data = yf.download(ticker, period="6mo")

            ma50 = data["Close"].rolling(50).mean().iloc[-1]
            ma200 = data["Close"].rolling(200).mean().iloc[-1]
            price = data["Close"].iloc[-1]

            score = 0

            if price > ma50:
                score += 3

            if ma50 > ma200:
                score += 3

            momentum = (price / data["Close"].iloc[0]) - 1

            if momentum > 0:
                score += 4

            results.append((ticker, score))

        except:
            pass

    ranking = sorted(results, key=lambda x: x[1], reverse=True)

    return ranking[:10]