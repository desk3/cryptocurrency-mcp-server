import os

from dotenv import load_dotenv
from typing import Any
import requests
import json
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

import logging

load_dotenv()
API_KEY = '123'; # os.getenv("DESK3_API_KEY")  # Use os.getenv("DESK3_API_KEY") in production
if not API_KEY:
    raise ValueError("Missing DESK3_API_KEY environment variable")

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def request_api(method: str, url: str, params: dict = None, data: dict = None) -> any:
    headers = {
        'Accepts': 'application/json',
        'X-DESK3_PRO_API_KEY': API_KEY,
    }
    try:
        logging.info(f"Requesting {method.upper()} {url} params={params} data={data}")
        if method.lower() == 'get':
            response = requests.get(url, headers=headers, params=params)
        elif method.lower() == 'post':
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        response.raise_for_status()
        logging.info(f"Response {response.status_code} for {url}")
        return json.loads(response.text)
    except Exception as e:
        logging.error(f"Error during {method.upper()} {url}: {e}")
        raise

async def get_suggest_gas(chainid: str) -> dict[str, Any]:
    """
    Get EIP1559 estimated gas information.
    :param chainid: Chain ID, required
    :return: Gas suggestion and trend information
    """
    url = 'https://mcp.desk3.io/v1/price/getSuggestGas'
    params = {'chainid': chainid}
    try:
        return request_api('get', url, params=params)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch suggest gas data: {e}")

async def get_exchange_rate() -> dict[str, Any]:
    """
    Get list of fiat currency exchange rates.
    :return: Exchange rate data
    """
    url = 'https://mcp.desk3.io/v1/market/exchangeRate'
    try:
        return request_api('get', url)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch exchange rate data: {e}")

async def get_mini_24hr(symbol: str | None = None) -> list[dict[str, Any]]:
    """
    Get 24-hour mini ticker information.
    :param symbol: Trading pair, comma separated for multiple, return all if not provided
    :return: Mini ticker info array
    """
    url = 'https://mcp.desk3.io/v1/market/mini/24hr'
    params = {}
    if symbol:
        params['symbol'] = symbol
    try:
        return request_api('get', url, params=params)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch mini 24hr data: {e}")

async def get_token_price(symbol: str | None = None) -> dict[str, Any]:
    """
    Get real-time token price information.
    :param symbol: Trading pair, comma separated for multiple, return all if not provided
    :return: Token price information
    """
    url = 'https://mcp.desk3.io/v1/market/price'
    params = {}
    if symbol:
        params['symbol'] = symbol
    try:
        return request_api('get', url, params=params)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch token price data: {e}")

async def get_fear_greed_index() -> dict[str, Any]:
    """
    Get crypto fear and greed index。
    :return: index
    """
    url = 'https://mcp.desk3.io/v1/market/fear-greed'
    try:
        return request_api('get', url)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch fear & greed index: {e}")

async def get_btc_trend() -> list[list]:
    """
    Get BTC trend chart for the past 3 months.
    :return: List of [date, price, active addresses, new addresses, transaction addresses]
    """
    url = 'https://mcp.desk3.io/v1/market/btc/trend'
    try:
        return request_api('get', url)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch BTC trend data: {e}")

async def get_eth_trend() -> list[list]:
    """
    Get the ETH trend chart for the past three months.
    :return: List of [date, price, active addresses, new addresses]
    """
    url = 'https://mcp.desk3.io/v1/market/eth/trend'
    try:
        return request_api('get', url)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch ETH trend data: {e}")

async def get_altcoin_season_index() -> dict:
    """
    Get the Altcoin Season Index.
    :return: Altcoin season index data
    """
    url = 'https://mcp.desk3.io/v1/market/altcoin/season'
    try:
        return request_api('get', url)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch Altcoin Season Index data: {e}")

async def get_bitcoin_dominance() -> dict:
    """
    Get Bitcoin (BTC) dominance metric.
    :return: Bitcoin dominance data
    """
    url = 'https://mcp.desk3.io/v1/market/bitcoin/dominance'
    try:
        return request_api('get', url)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch Bitcoin dominance data: {e}")

async def get_cycle_indicators() -> dict[str, Any]:
    """
    Get crypto market cycle top indicators.
    :return: Market cycle indicators data with fields (Indicator/Current/24h%/ReferencePrice/Triggered)
    """
    url = 'https://mcp.desk3.io/v1/market/cycleIndicators'
    try:
        return request_api('get', url)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch cycle indicators data: {e}")

async def get_pi_cycle_top() -> dict[str, Any]:
    """
    Get BTC Pi Cycle Top indicator data.
    :return: Pi Cycle Top indicator data using 111DMA and 2x350DMA to identify Bitcoin market tops
    """
    url = 'https://mcp.desk3.io/v1/market/pi-cycle-top'
    try:
        return request_api('get', url)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch Pi Cycle Top indicator data: {e}")

async def get_rainbow_chart() -> dict[str, Any]:
    """
    Get Bitcoin Rainbow Price Chart data.
    :return: Bitcoin Rainbow Chart data using logarithmic growth curve with color bands to illustrate market sentiment
    """
    url = 'https://mcp.desk3.io/v1/market/rainbow'
    try:
        return request_api('get', url)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch Bitcoin Rainbow Chart data: {e}")

async def get_puell_multiple() -> dict[str, Any]:
    """
    Get Puell Multiple data.
    :return: Puell Multiple data assessing Bitcoin miners' revenue by dividing daily issuance by its 365-day average
    """
    url = 'https://mcp.desk3.io/v1/market/puell-multiple'
    try:
        return request_api('get', url)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch Puell Multiple data: {e}")


async def get_cycles() -> dict[str, Any]:
    """
    Get Simple indicators data including Puell Multiple Status, Pi Cycle Top Status, and Crypto Market Cycle Top Indicator.
    :return: Simple indicators data with puellMultiple, piCycleTop, and likelihood fields
    """
    url = 'https://mcp.desk3.io/v1/market/cycles'
    try:
        return request_api('get', url)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch cycles data: {e}")

server = Server("desk3_service")

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    List available desk3 resources.
    """
    resources = [
        types.Resource(
            uri=AnyUrl("desk3://gas/suggest"),
            name="EIP1559 Gas Suggestion",
            description="Get EIP1559 gas suggestion for a given chainid. Use ?chainid=1 for Ethereum mainnet, ?chainid=137 for Polygon",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/exchangeRate"),
            name="Fiat Exchange Rate List",
            description="List of foreign currency exchange rates",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/mini/24hr"),
            name="24hr Mini Ticker",
            description="24-hour currency price Mini information, supports symbol parameters like BTCUSDT, ETHUSDT. Use ?symbol=BTCUSDT to get specific symbol data",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/price"),
            name="Token Price Info",
            description="Get real-time token price information, support symbol parameters like BTCUSDT, ETHUSDT. Use ?symbol=BTCUSDT to get specific symbol data",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/fear-greed"),
            name="Crypto Fear and Greed Index",
            description="Discover our Fear and Greed Index, a powerful tool that analyzes market sentiment to help you make informed crypto investment decisions. Stay ahead of market trends with real-time and historical data available through our easy-to-use API",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/btc/trend"),
            name="BTC Trend (3 months)",
            description="Get the BTC trend chart for the past 3 months. Format: [[date, price, active addresses, new addresses, transaction addresses]]",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/eth/trend"),
            name="ETH Trend (3 months)",
            description="Get the ETH trend chart for the past three months. Format: [[date, price, active addresses, new addresses]]",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/altcoin/season"),
            name="Altcoin Season Index",
            description="Altcoin Season Index page provides real-time insights into whether the cryptocurrency market is currently in Altcoin Season, based on the performance of the top 100 altcoins relative to Bitcoin over the past 90 days, with detailed charts and metrics for tracking market trends and altcoin dominance",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/bitcoin/dominance"),
            name="Bitcoin Dominance",
            description="Bitcoin (BTC) dominance is a metric used to measure the relative market share or dominance of Bitcoin in the overall cryptocurrency sector. It represents the percentage of Bitcoin's total market capitalization compared to the total market capitalization of all cryptocurrencies combined",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/cycle/indicators"),
            name="Crypto Market Cycle Top Indicators",
            description="Get crypto market cycle top indicators with fields (Indicator/Current/24h%/ReferencePrice/Triggered). Provides comprehensive market cycle analysis including Bitcoin Ahr999 Index, Pi Cycle Top Indicator, Puell Multiple, and more",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/pi-cycle-top"),
            name="BTC Pi Cycle Top Indicator",
            description="The Pi Cycle Top indicator uses the 111DMA and 2x350DMA to identify Bitcoin market tops. When the 111DMA crosses above the 2x350DMA, it historically typically signals a cycle peak within about 3 days, reflecting Bitcoin's long-term cyclical behavior",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/rainbow"),
            name="Bitcoin Rainbow Price Chart",
            description="The Bitcoin Rainbow Chart uses a logarithmic growth curve with a color band to illustrate market sentiment and highlight potential buy or sell areas. It is not suitable for short-term predictions, but helps to identify overvaluation or undervaluation from history",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/puell-multiple"),
            name="Puell Multiple",
            description="The Puell Multiple assesses Bitcoin miners' revenue by dividing daily issuance (in USD) by its 365-day average. This reflects the mining pressure in the market. Low values (green areas) indicate undervaluation and strong historical buy areas, while high values (red areas) indicate overvaluation and potential sell opportunities. It provides insight into market cycles from the perspective of miners",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/cycles"),
            name="Simple indicators: Puell Multiple Status/Pi Cycle Top Status/Crypto Market Cycle Top Indicator",
            description="Does the Bitcoin Four-Year Cycle Exist? Discover the cryptocurrency market cycle indicator that helps you identify the top of the cryptocurrency bull market. This is a collection of publicly available signals including Pi Cycle and Puell Multiple data. Return fields: (puellMultiple Puell: multiple status / piCycleTop: Pi cycle top status / likelihood: cryptocurrency market cycle top indicator) ",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        )
    ]
    return resources

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    if uri.scheme != "desk3":
        raise ValueError(f"Unsupported scheme: {uri.scheme}")

    match uri.path:
        case "/suggest":
            try:
                query_params = {qp[0]: qp[1] for qp in uri.query_params()}
                chainid = query_params.get("chainid")
                if not chainid:
                    raise ValueError("Missing required query param: chainid")
                data = await get_suggest_gas(chainid=chainid)
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch suggest gas data: {e}")
        case "/exchangeRate":
            try:
                data = await get_exchange_rate()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch exchange rate data: {e}")
        case "/mini/24hr":
            try:
                query_params = {qp[0]: qp[1] for qp in uri.query_params()}
                symbol = query_params.get("symbol")
                data = await get_mini_24hr(symbol=symbol)
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch mini 24hr data: {e}")
        case "/price":
            try:
                query_params = {qp[0]: qp[1] for qp in uri.query_params()}
                symbol = query_params.get("symbol")
                data = await get_token_price(symbol=symbol)
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch token price data: {e}")
        case "/fear-greed":
            try:
                data = await get_fear_greed_index()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch fear & greed index: {e}")
        case "/btc/trend":
            try:
                data = await get_btc_trend()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch BTC trend data: {e}")
        case "/eth/trend":
            try:
                data = await get_eth_trend()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch ETH trend data: {e}")
        case "/altcoin/season":
            try:
                data = await get_altcoin_season_index()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch Altcoin Season Index data: {e}")
        case "/bitcoin/dominance":
            try:
                data = await get_bitcoin_dominance()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch Bitcoin dominance data: {e}")
        case "/cycle/indicators":
            try:
                data = await get_cycle_indicators()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch cycle indicators data: {e}")
        case "/pi-cycle-top":
            try:
                data = await get_pi_cycle_top()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch Pi Cycle Top indicator data: {e}")
        case "/rainbow":
            try:
                data = await get_rainbow_chart()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch Bitcoin Rainbow Chart data: {e}")
        case "/puell-multiple":
            try:
                data = await get_puell_multiple()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch Puell Multiple data: {e}")
        case "/cycles":
            try:
                data = await get_cycles()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch cycles data: {e}")
        case _:
            raise ValueError(f"Unsupported path: {uri.path}")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    tools = [
        types.Tool(
            name="get_suggest_gas",
            description="Get EIP1559 estimated gas info (chainid required)",
            inputSchema={
                "type": "object",
                "properties": {
                    "chainid": {
                        "type": "string",
                        "description": "Chain ID for the blockchain network (e.g., 1 for Ethereum mainnet, 137 for Polygon)",
                        "examples": ["1", "137", "56", "42161"],
                        "pattern": "^[0-9]+$"
                    },
                },
                "required": ["chainid"],
            },
        ),
        types.Tool(
            name="get_exchange_rate",
            description="Get list of fiat currency exchange rates",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_mini_24hr",
            description="Get 24-hour mini ticker info, supports symbol parameter",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol in format like BTCUSDT, ETHUSDT, etc. Leave empty to get all symbols.",
                        "examples": ["BTCUSDT", "ETHUSDT", "BNBUSDT"],
                        "pattern": "^[A-Z0-9]+$"
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="get_token_price",
            description="Get real-time token price info, supports symbol parameter",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol in format like BTCUSDT, ETHUSDT, etc. Leave empty to get all symbols",
                        "examples": ["BTCUSDT", "ETHUSDT", "BNBUSDT"],
                        "pattern": "^[A-Z0-9]+$"
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="get_fear_greed_index",
            description="Discover our Fear and Greed Index, a powerful tool that analyzes market sentiment to help you make informed crypto investment decisions. Stay ahead of market trends with real-time and historical data available through our easy-to-use API",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_btc_trend",
            description="Get BTC trend chart for the past 3 months. Format: [[date, price, active addresses, new addresses, transaction addresses]]",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_eth_trend",
            description="Get the ETH trend chart for the past three months. Format: [[date, price, active addresses, new addresses]]",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_altcoin_season_index",
            description="Altcoin Season Index page provides real-time insights into whether the cryptocurrency market is currently in Altcoin Season, based on the performance of the top 100 altcoins relative to Bitcoin over the past 90 days, with detailed charts and metrics for tracking market trends and altcoin dominance",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_bitcoin_dominance",
            description="Bitcoin (BTC) dominance is a metric used to measure the relative market share or dominance of Bitcoin in the overall cryptocurrency sector. It represents the percentage of Bitcoin's total market capitalization compared to the total market capitalization of all cryptocurrencies combined",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_cycle_indicators",
            description="Get crypto market cycle top indicators with fields (Indicator/Current/24h%/ReferencePrice/Triggered). Provides comprehensive market cycle analysis including Bitcoin Ahr999 Index, Pi Cycle Top Indicator, Puell Multiple, Bitcoin Rainbow Chart, and more",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_pi_cycle_top",
            description="The Pi Cycle Top indicator uses the 111DMA and 2x350DMA to identify Bitcoin market tops. When the 111DMA crosses above the 2x350DMA, it historically typically signals a cycle peak within about 3 days, reflecting Bitcoin's long-term cyclical behavior",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_rainbow_chart",
            description="The Bitcoin Rainbow Chart uses a logarithmic growth curve with a color band to illustrate market sentiment and highlight potential buy or sell areas. It is not suitable for short-term predictions, but helps to identify overvaluation or undervaluation from history",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_puell_multiple",
            description="The Puell Multiple assesses Bitcoin miners' revenue by dividing daily issuance (in USD) by its 365-day average. This reflects the mining pressure in the market. Low values (green areas) indicate undervaluation and strong historical buy areas, while high values (red areas) indicate overvaluation and potential sell opportunities. It provides insight into market cycles from the perspective of miners",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_cycles",
            description="Does the Bitcoin Four-Year Cycle Exist? Discover the cryptocurrency market cycle indicator that helps you identify the top of the cryptocurrency bull market. This is a collection of publicly available signals including Pi Cycle and Puell Multiple data. Return fields: (puellMultiple Puell: multiple status / piCycleTop: Pi cycle top status / likelihood: cryptocurrency market cycle top indicator) ",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        )
    ]
    return tools

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """

    match name:
        case "get_suggest_gas":
            if not arguments or "chainid" not in arguments:
                raise ValueError("Missing required argument: chainid")
            chainid = arguments["chainid"]
            try:
                data = await get_suggest_gas(chainid=chainid)
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps(data, indent=2),
                    )
                ]
            except Exception as e:
                raise RuntimeError(f"Failed to fetch suggest gas data: {e}")
        case "get_exchange_rate":
            try:
                data = await get_exchange_rate()
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps(data, indent=2),
                    )
                ]
            except Exception as e:
                raise RuntimeError(f"Failed to fetch exchange rate data: {e}")
        case "get_mini_24hr":
            symbol = arguments.get("symbol") if arguments else None
            try:
                data = await get_mini_24hr(symbol=symbol)
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps(data, indent=2),
                    )
                ]
            except Exception as e:
                raise RuntimeError(f"Failed to fetch mini 24hr data: {e}")
        case "get_token_price":
            symbol = arguments.get("symbol") if arguments else None
            try:
                data = await get_token_price(symbol=symbol)
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps(data, indent=2),
                    )
                ]
            except Exception as e:
                raise RuntimeError(f"Failed to fetch token price data: {e}")
        case "get_fear_greed_index":
            try:
                data = await get_fear_greed_index()
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps(data, indent=2),
                    )
                ]
            except Exception as e:
                raise RuntimeError(f"Failed to fetch fear & greed index: {e}")
        case "get_btc_trend":
            try:
                data = await get_btc_trend()
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps(data, indent=2),
                    )
                ]
            except Exception as e:
                raise RuntimeError(f"Failed to fetch BTC trend data: {e}")
        case "get_eth_trend":
            try:
                data = await get_eth_trend()
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps(data, indent=2),
                    )
                ]
            except Exception as e:
                raise RuntimeError(f"Failed to fetch ETH trend data: {e}")
        case "get_altcoin_season_index":
            try:
                data = await get_altcoin_season_index()
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps(data, indent=2),
                    )
                ]
            except Exception as e:
                raise RuntimeError(f"Failed to fetch Altcoin Season Index data: {e}")
        case "get_bitcoin_dominance":
            try:
                data = await get_bitcoin_dominance()
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps(data, indent=2),
                    )
                ]
            except Exception as e:
                raise RuntimeError(f"Failed to fetch Bitcoin dominance data: {e}")
        case "get_cycle_indicators":
            try:
                data = await get_cycle_indicators()
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps(data, indent=2),
                    )
                ]
            except Exception as e:
                raise RuntimeError(f"Failed to fetch cycle indicators data: {e}")
        case "get_pi_cycle_top":
            try:
                data = await get_pi_cycle_top()
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps(data, indent=2),
                    )
                ]
            except Exception as e:
                raise RuntimeError(f"Failed to fetch Pi Cycle Top indicator data: {e}")
        case "get_rainbow_chart":
            try:
                data = await get_rainbow_chart()
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps(data, indent=2),
                    )
                ]
            except Exception as e:
                raise RuntimeError(f"Failed to fetch Bitcoin Rainbow Chart data: {e}")
        case "get_puell_multiple":
            try:
                data = await get_puell_multiple()
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps(data, indent=2),
                    )
                ]
            except Exception as e:
                raise RuntimeError(f"Failed to fetch Puell Multiple data: {e}")
        case "get_cycles":
            try:
                data = await get_cycles()
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps(data, indent=2),
                    )
                ]
            except Exception as e:
                raise RuntimeError(f"Failed to fetch cycles data: {e}")
        case _:
            raise ValueError(f"Unsupported tool: {name}")


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="desk3_service",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
