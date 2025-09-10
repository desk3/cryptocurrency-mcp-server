# Desk3 MCP Server

A fully compatible [MCP (Model Context Protocol)](https://github.com/mcp-protocol/spec) server for Desk3 crypto data, supporting Dify, Claude, Notion MCP, and other clients.

<a href="https://glama.ai/mcp/servers/@desk3/cryptocurrency-mcp-server">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@desk3/cryptocurrency-mcp-server/badge" />
</a>

## Key Features

- Implements all Desk3 crypto data endpoints as MCP resources and tools
- Supports HTTP, SSE, and JSON-RPC 2.0 interfaces
- One-click start with `uv run desk3_service`
- Docker support

## Resources

The server exposes the following resources:

- `desk3://gas/suggest`  
  EIP1559 Gas Suggestion (获取 EIP1559 Gas 建议，需 chainid 查询参数)
- `desk3://market/exchangeRate`  
  Fiat Exchange Rate List（法币汇率列表）
- `desk3://market/mini/24hr`  
  24hr Mini Ticker（24 小时币价迷你行情，支持 symbol 参数，如 ETHUSDT）
- `desk3://market/price`  
  Token Price Info（获取实时代币价格，支持 symbol 参数，如 ETHUSDT、BTCUSDT）
- `desk3://market/circulating`  
  Token Circulating Supply and Total Supply（获取代币流通量与供应量，symbol 参数必传，格式 BTC -> BTCUSDT, ETH -> ETHUSDT）
- `desk3://market/fear-greed`  
  Crypto Fear and Greed Index（贪婪与恐惧指数，分析市场情绪，助力明智投资决策，支持实时与历史数据）
- `desk3://market/btc/trend`  
  BTC Trend (3 months)（获取近 3 个月 BTC 趋势图表，格式：[[日期, 当日价格, 活跃地址数, 新增地址数, 发生交易地址数]]）
- `desk3://market/eth/trend`  
  ETH Trend (3 months)（获取近 3 个月 ETH 趋势图表，格式：[[日期, 当日价格, 活跃地址数, 新增地址数]]）
- `desk3://market/altcoin/season`  
  Altcoin Season Index（山寨币季指数，基于前 100 山寨币与比特币 90 天表现，实时判断市场是否处于山寨币季，含详细图表与指标）
- `desk3://market/bitcoin/dominance`  
  Bitcoin Dominance（比特币主导率，衡量比特币在整个加密货币市场的市值占比）
- `desk3://market/cycle/indicators`  
  Crypto Market Cycle Top Indicators（加密货币市场周期顶部指标，返回字段：指标/当前/24小时%/参考价格/已触发）
- `desk3://market/pi-cycle-top`  
  BTC Pi Cycle Top Indicator（BTC Pi 周期顶部指标，使用 111DMA 和 2x350DMA 识别比特币市场顶部）
- `desk3://market/rainbow`  
  Bitcoin Rainbow Price Chart（比特币彩虹价格图，使用对数增长曲线和色带说明市场情绪，识别潜在买入或卖出区域）
- `desk3://market/puell-multiple`  
  Puell Multiple（皮勒乘数计算，通过每日发行量除以其365天平均值评估比特币矿工收入，反映市场挖矿压力）
- `desk3://market/cycles`  
  Simple indicators: Puell Multiple Status/Pi Cycle Top Status/Crypto Market Cycle Top Indicator（简易指标：Puell 多重状态/Pi 周期顶部状态/加密货币市场周期顶部指标）

## Tools

- `get_suggest_gas`  
  Get EIP1559 estimated gas info (chainid required)（获取 EIP1559 估算 Gas 信息，需要 chainid）
  - **chainid**: Chain ID for the blockchain network (e.g., 1 for Ethereum mainnet, 137 for Polygon)
- `get_exchange_rate`  
  Get list of fiat currency exchange rates（获取法币汇率列表）
- `get_mini_24hr`  
  Get 24-hour mini ticker info, supports symbol parameter（获取 24 小时迷你行情，支持 symbol 参数）
  - **symbol**: Trading pair symbol in format like BTCUSDT, ETHUSDT, etc. Leave empty to get all symbols
- `get_token_price`  
  Get real-time token price info, supports symbol parameter（获取实时代币价格，支持 symbol 参数）
  - **symbol**: Trading pair symbol in format like BTCUSDT, ETHUSDT, etc. Leave empty to get all symbols
- `get_token_circulating_supply`  
  Get token circulating supply and total supply information（获取代币流通量与供应量信息）
  - **symbol**: Trading pair symbol (required), format BTC -> BTCUSDT, ETH -> ETHUSDT
- `get_fear_greed_index`  
  Discover our Fear and Greed Index...（贪婪与恐惧指数，分析市场情绪，助力明智投资决策，支持实时与历史数据）
- `get_btc_trend`  
  Get BTC trend chart for the past 3 months...（获取近 3 个月 BTC 趋势图表...）
- `get_eth_trend`  
  Get the ETH trend chart for the past three months...（获取近 3 个月 ETH 趋势图表...）
- `get_altcoin_season_index`  
  Altcoin Season Index page provides real-time insights...（山寨币季指数...）
- `get_bitcoin_dominance`  
  Bitcoin (BTC) dominance is a metric...（比特币主导率...）
- `get_cycle_indicators`  
  Get crypto market cycle top indicators with fields (Indicator/Current/24h%/ReferencePrice/Triggered)（加密货币市场周期顶部指标，返回字段：指标/当前/24小时%/参考价格/已触发）
- `get_pi_cycle_top`  
  The Pi Cycle Top indicator uses the 111DMA and 2x350DMA to identify Bitcoin market tops（Pi 周期顶部指标使用 111DMA 和 2x350DMA 识别比特币市场顶部）
- `get_rainbow_chart`  
  The Bitcoin Rainbow Chart uses a logarithmic growth curve with a color band to illustrate market sentiment and highlight potential buy or sell areas（比特币彩虹图使用带有色带的对数增长曲线来说明市场情绪，并突出显示潜在的买入或卖出区域）
- `get_puell_multiple`  
  The Puell Multiple assesses Bitcoin miners' revenue by dividing daily issuance (in USD) by its 365-day average（Puell Multiple 通过将每日发行量（美元）除以其 365 天的平均值来评估比特币矿工的收入）
- `get_cycles`  
  Does the Bitcoin Four-Year Cycle Exist? Discover the cryptocurrency market cycle indicator that helps you identify the top of the cryptocurrency bull market（比特币四年周期是否存在？发现加密货币市场周期指标，帮助您识别加密货币牛市的顶峰）

## Configuration

~~- Requires a valid `DESK3_API_KEY` (set in your environment or `.env` file).~~

## Quickstart

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

### Install and Run

```bash
uv sync
uv run desk3_service
```

### Docker

```bash
docker build -t desk3-service .
docker run -e -p 8100:8100 desk3-service
```

## Startup Modes

This project supports two startup modes:

### 1. HTTP/SSE Server (Recommended)

Launches a Starlette HTTP/SSE server on 0.0.0.0:8100/sse (http://127.0.0.1:8100/sse) for use with Dify, Claude, Notion MCP, etc.

```bash
# Recommended: run directly with Python
PYTHONPATH=src python -m desk3_service.http_server
# Or run the Starlette MCP server variant
PYTHONPATH=src python -m desk3_service.starlette_mcp_server
```

Or, if you want to use uv/pyproject.toml script, add a script entry for http_server or starlette_mcp_server.

### 2. MCP Stdio Server (Advanced)

Launches a pure MCP stdio server for CLI or advanced integration (not HTTP/SSE):

```bash
uv run desk3_service
```

This mode is only needed if you want to use MCP over stdin/stdout (not recommended for most users).

## Troubleshooting

- Make sure `uv` is installed and in your PATH.
~~- Ensure your `DESK3_API_KEY` is valid.~~
~~- If using Docker, set the API key with `-e DESK3_API_KEY=...`.~~



