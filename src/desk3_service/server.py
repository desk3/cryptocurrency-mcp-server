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
            description="Get EIP1559 gas suggestion for a given chainid (query param required)（获取 EIP1559 Gas 建议，需 chainid 查询参数）",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/exchangeRate"),
            name="Fiat Exchange Rate List",
            description="List of foreign currency exchange rates（法币汇率列表）",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/mini/24hr"),
            name="24hr Mini Ticker",
            description="24-hour currency price Mini information, supports symbol parameters: ETHUSDT（24 小时币价迷你行情，支持 symbol 参数，如 ETHUSDT）",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/price"),
            name="Token Price Info",
            description="Get real-time token price information, support symbol parameters (ETHUSDT,BTCUSDT)（获取实时代币价格，支持 symbol 参数，如 ETHUSDT、BTCUSDT）",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/fear-greed"),
            name="Crypto Fear and Greed Index",
            description="Discover our Fear and Greed Index, a powerful tool that analyzes market sentiment to help you make informed crypto investment decisions. Stay ahead of market trends with real-time and historical data available through our easy-to-use API.（贪婪与恐惧指数，分析市场情绪，助力明智投资决策，支持实时与历史数据）",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/btc/trend"),
            name="BTC Trend (3 months)",
            description="Get the BTC trend chart for the past 3 months. Format: [[date, price, active addresses, new addresses, transaction addresses]]（获取近 3 个月 BTC 趋势图表，格式：[[日期, 当日价格, 活跃地址数, 新增地址数, 发生交易地址数]]）",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/eth/trend"),
            name="ETH Trend (3 months)",
            description="Get the ETH trend chart for the past three months. Format: [[date, price, active addresses, new addresses]]（获取近 3 个月 ETH 趋势图表，格式：[[日期, 当日价格, 活跃地址数, 新增地址数]]）",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/altcoin/season"),
            name="Altcoin Season Index",
            description="Altcoin Season Index page provides real-time insights into whether the cryptocurrency market is currently in Altcoin Season, based on the performance of the top 100 altcoins relative to Bitcoin over the past 90 days, with detailed charts and metrics for tracking market trends and altcoin dominance.（山寨币季指数，基于前 100 山寨币与比特币 90 天表现，实时判断市场是否处于山寨币季，含详细图表与指标）",
            mimeType="application/json",
            size=None,
            annotations=None,
            meta=None,
        ),
        types.Resource(
            uri=AnyUrl("desk3://market/bitcoin/dominance"),
            name="Bitcoin Dominance",
            description="Bitcoin (BTC) dominance is a metric used to measure the relative market share or dominance of Bitcoin in the overall cryptocurrency sector. It represents the percentage of Bitcoin's total market capitalization compared to the total market capitalization of all cryptocurrencies combined.（比特币主导率，衡量比特币在整个加密货币市场的市值占比）",
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
        case "/gas/suggest":
            try:
                query_params = {qp[0]: qp[1] for qp in uri.query_params()}
                chainid = query_params.get("chainid")
                if not chainid:
                    raise ValueError("Missing required query param: chainid")
                data = await get_suggest_gas(chainid=chainid)
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch suggest gas data: {e}")
        case "/market/exchangeRate":
            try:
                data = await get_exchange_rate()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch exchange rate data: {e}")
        case "/market/mini/24hr":
            try:
                query_params = {qp[0]: qp[1] for qp in uri.query_params()}
                symbol = query_params.get("symbol")
                data = await get_mini_24hr(symbol=symbol)
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch mini 24hr data: {e}")
        case "/market/price":
            try:
                query_params = {qp[0]: qp[1] for qp in uri.query_params()}
                symbol = query_params.get("symbol")
                data = await get_token_price(symbol=symbol)
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch token price data: {e}")
        case "/market/fear-greed":
            try:
                data = await get_fear_greed_index()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch fear & greed index: {e}")
        case "/market/btc/trend":
            try:
                data = await get_btc_trend()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch BTC trend data: {e}")
        case "/market/eth/trend":
            try:
                data = await get_eth_trend()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch ETH trend data: {e}")
        case "/market/altcoin/season":
            try:
                data = await get_altcoin_season_index()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch Altcoin Season Index data: {e}")
        case "/market/bitcoin/dominance":
            try:
                data = await get_bitcoin_dominance()
                return json.dumps(data, indent=2)
            except Exception as e:
                raise RuntimeError(f"Failed to fetch Bitcoin dominance data: {e}")
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
            description="Get EIP1559 estimated gas info (chainid required)（获取 EIP1559 估算 Gas 信息，需要 chainid）",
            inputSchema={
                "type": "object",
                "properties": {
                    "chainid": {"type": "string"},
                },
                "required": ["chainid"],
            },
        ),
        types.Tool(
            name="get_exchange_rate",
            description="Get list of fiat currency exchange rates（获取法币汇率列表）",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_mini_24hr",
            description="Get 24-hour mini ticker info, supports symbol parameter（获取 24 小时迷你行情，支持 symbol 参数）",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name="get_token_price",
            description="Get real-time token price info, supports symbol parameter（获取实时代币价格，支持 symbol 参数）",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name="get_fear_greed_index",
            description="Discover our Fear and Greed Index, a powerful tool that analyzes market sentiment to help you make informed crypto investment decisions. Stay ahead of market trends with real-time and historical data available through our easy-to-use API.（贪婪与恐惧指数，分析市场情绪，助力明智投资决策，支持实时与历史数据）",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_btc_trend",
            description="Get BTC trend chart for the past 3 months. Format: [[date, price, active addresses, new addresses, transaction addresses]]（获取近 3 个月 BTC 趋势图表，格式：[[日期, 当日价格, 活跃地址数, 新增地址数, 发生交易地址数]]）",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_eth_trend",
            description="Get the ETH trend chart for the past three months. Format: [[date, price, active addresses, new addresses]]（获取近 3 个月 ETH 趋势图表，格式：[[日期, 当日价格, 活跃地址数, 新增地址数]]）",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_altcoin_season_index",
            description="Altcoin Season Index page provides real-time insights into whether the cryptocurrency market is currently in Altcoin Season, based on the performance of the top 100 altcoins relative to Bitcoin over the past 90 days, with detailed charts and metrics for tracking market trends and altcoin dominance.（山寨币季指数，基于前 100 山寨币与比特币 90 天表现，实时判断市场是否处于山寨币季，含详细图表与指标）",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_bitcoin_dominance",
            description="Bitcoin (BTC) dominance is a metric used to measure the relative market share or dominance of Bitcoin in the overall cryptocurrency sector. It represents the percentage of Bitcoin's total market capitalization compared to the total market capitalization of all cryptocurrencies combined.（比特币主导率，衡量比特币在整个加密货币市场的市值占比）",
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
