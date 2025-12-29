import requests
from smolagents import tool

API_URL = "https://api.coingecko.com/api/v3"


@tool
def crypto_price(symbol: str) -> str:
    """
    Returns the current price of a cryptocurrency in USD.

    Args:
        symbol (str): Cryptocurrency id or symbol (bitcoin, ethereum, etc.)

    Returns:
        str: Current price in USD.
    """
    response = requests.get(
        f"{API_URL}/simple/price",
        params={"ids": symbol.lower(), "vs_currencies": "usd"}
    )
    data = response.json()

    if symbol.lower() in data:
        return f"The current price of {symbol.upper()} is ${data[symbol.lower()]['usd']}"
    return f"Could not find price for {symbol.upper()}"


@tool
def crypto_info(symbol: str) -> str:
    """
    Returns basic information about a cryptocurrency.

    Args:
        symbol (str): Cryptocurrency id (bitcoin, ethereum, etc.)

    Returns:
        str: Short description and market data.
    """
    response = requests.get(f"{API_URL}/coins/{symbol.lower()}")
    if response.status_code != 200:
        return f"Could not find info for {symbol.upper()}"

    data = response.json()
    name = data.get("name", "Unknown")
    market_cap = data["market_data"]["market_cap"]["usd"]
    supply = data["market_data"]["circulating_supply"]

    return (
        f"{name}:\n"
        f"Market cap: ${market_cap:,}\n"
        f"Circulating supply: {supply:,}"
    )


@tool
def compare_crypto(symbol1: str, symbol2: str) -> str:
    """
    Compares prices of two cryptocurrencies.

    Args:
        symbol1 (str): First cryptocurrency id.
        symbol2 (str): Second cryptocurrency id.

    Returns:
        str: Comparison of prices.
    """
    response = requests.get(
        f"{API_URL}/simple/price",
        params={
            "ids": f"{symbol1.lower()},{symbol2.lower()}",
            "vs_currencies": "usd"
        }
    )
    data = response.json()

    if symbol1.lower() not in data or symbol2.lower() not in data:
        return "One or both cryptocurrencies could not be found."

    price1 = data[symbol1.lower()]["usd"]
    price2 = data[symbol2.lower()]["usd"]

    return (
        f"{symbol1.upper()}: ${price1}\n"
        f"{symbol2.upper()}: ${price2}"
    )


@tool
def crypto_history(symbol: str, days: int) -> str:
    """
    Returns historical price data for a cryptocurrency.

    Args:
        symbol (str): Cryptocurrency id.
        days (int): Number of past days (1, 7, 30, etc.)

    Returns:
        str: Summary of historical prices.
    """
    response = requests.get(
        f"{API_URL}/coins/{symbol.lower()}/market_chart",
        params={"vs_currency": "usd", "days": days}
    )

    if response.status_code != 200:
        return f"Could not retrieve history for {symbol.upper()}"

    prices = response.json().get("prices", [])
    if not prices:
        return "No historical data available."

    first = prices[0][1]
    last = prices[-1][1]

    return (
        f"{symbol.upper()} price {days} days ago: ${first:.2f}\n"
        f"Current price: ${last:.2f}"
    )


@tool
def crypto_risk(symbol: str) -> str:
    """
    Estimates investment risk based on market volatility.

    Args:
        symbol (str): Cryptocurrency id.

    Returns:
        str: Risk assessment.
    """
    response = requests.get(f"{API_URL}/coins/{symbol.lower()}")
    if response.status_code != 200:
        return f"Could not assess risk for {symbol.upper()}"

    data = response.json()
    change_24h = data["market_data"]["price_change_percentage_24h"]

    if change_24h > 10:
        risk = "High risk 🚨"
    elif change_24h > 3:
        risk = "Medium risk ⚠️"
    else:
        risk = "Low risk ✅"

    return (
        f"{symbol.upper()} 24h change: {change_24h:.2f}%\n"
        f"Risk level: {risk}"
    )
