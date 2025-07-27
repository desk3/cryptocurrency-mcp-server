# Desk3 MCP Server

A fully compatible [MCP (Model Context Protocol)](https://github.com/mcp-protocol/spec) server for Desk3 crypto data, supporting Dify, Claude, Notion MCP, and other clients.

Desk3 MCP Server

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

## Tools

- `get_suggest_gas`  
  Get EIP1559 estimated gas info (chainid required)（获取 EIP1559 估算 Gas 信息，需要 chainid）
- `get_exchange_rate`  
  Get list of fiat currency exchange rates（获取法币汇率列表）
- `get_mini_24hr`  
  Get 24-hour mini ticker info, supports symbol parameter（获取 24 小时迷你行情，支持 symbol 参数）
- `get_token_price`  
  Get real-time token price info, supports symbol parameter（获取实时代币价格，支持 symbol 参数）
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

## Configuration

- Requires a valid `DESK3_API_KEY` (set in your environment or `.env` file).

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
docker run -e DESK3_API_KEY=your_api_key_here -p 8100:8100 desk3-service
```

## Startup Modes

This project supports two startup modes:

### 1. HTTP/SSE Server (Recommended)

Launches a Starlette HTTP/SSE server on 0.0.0.0:8100 for use with Dify, Claude, Notion MCP, etc.

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
- Ensure your `DESK3_API_KEY` is valid.
- If using Docker, set the API key with `-e DESK3_API_KEY=...`.


