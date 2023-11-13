import requests
from keys import CMC_PRO_API_KEY


API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
API_KEY = CMC_PRO_API_KEY


def crypto_price(user_input):
    symbol = user_input.upper()
    params = {
        "symbol": symbol,
        "convert": "USD",
        "CMC_PRO_API_KEY": API_KEY
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        price = data["data"][symbol]["quote"]["USD"]["price"]
        market_cap = data["data"][symbol]["quote"]["USD"]["market_cap"]
        return f"\n{symbol}\n\nPrice: ${price:.2f}\nMarket Cap: ${market_cap:.2f}"
    else:
        return f"\nCould not get price and market capitalization for {symbol}."
