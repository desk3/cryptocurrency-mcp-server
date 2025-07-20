# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Desk3 MCP (Model Context Protocol) server that provides cryptocurrency data from the Desk3 API. The server implements the MCP specification, allowing AI assistants to access cryptocurrency lists and quotes as well as various interfaces related to cryptocurrency data.

## Architecture

- **MCP Server**: Built using the `mcp` Python library, communicates via stdin/stdout
- **API Integration**: Interfaces with Desk3 API for cryptocurrency data
- **Resource System**: Exposes cryptocurrency data as resources with `desk3://` URI scheme
- **Tool System**: Provides two tools for getting listings and quotes

### Key Components

- `src/desk3_service/server.py`:  
  Main MCP server implementation.  
  - Registers all MCP resources and tools (handlers, schemas, business logic).
  - Implements all API integrations and business logic for Desk3 crypto data.
  - Single source of truth for all MCP interfaces.

- `src/desk3_service/http_server.py`:  
  Starlette-based HTTP + SSE adapter.  
  - Exposes HTTP and SSE endpoints for MCP clients (e.g., Dify, Claude, Notion).
  - Imports the `server` instance from `server.py` and does not register handlers itself.

- `src/desk3_service/starlette_mcp_server.py`:  
  Starlette-based SSE + POST MCP server adapter.  
  - Provides SSE and POST endpoints for MCP protocol.
  - Imports the `server` instance from `server.py` and does not register handlers itself.

- `src/desk3_service/__init__.py`:  
  Package entry point (optional).  
  - Can be used to run the MCP server as a module.

- `pyproject.toml`, `.env`, `uv.lock`:  
  Dependency management and environment configuration.

## Development Commands

### Setup and Installation

```bash
# Install dependencies
uv sync

# Run the server (directly via uv, thanks to the script entry in pyproject.toml)
uv run desk3_service
```

### Docker
```bash
# Build Docker image
docker build -t desk3-service .

# Run with Docker
docker run -e DESK3_API_KEY=your_api_key_here desk3-service
```

### Linting
```bash
# Run ruff linter
uv run ruff check
uv run ruff format
```

## Configuration

- Requires `DESK3_API_KEY` environment variable
- Uses `.env` file support via python-dotenv
- Configuration for Claude Desktop requires absolute path to repository

## MCP Server Details

The server implements:

- **Resources**:
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

- **Tools**:
  - `get_suggest_gas`  
    Get EIP1559 estimated gas info (chainid required)（获取 EIP1559 估算 Gas 信息，需要 chainid）
  - `get_exchange_rate`  
    Get list of fiat currency exchange rates（获取法币汇率列表）
  - `get_mini_24hr`  
    Get 24-hour mini ticker info, supports symbol parameter（获取 24 小时迷你行情，支持 symbol 参数）
  - `get_token_price`  
    Get real-time token price info, supports symbol parameter（获取实时代币价格，支持 symbol 参数）
  - `get_fear_greed_index`  
    Discover our Fear and Greed Index, a powerful tool that analyzes market sentiment to help you make informed crypto investment decisions. Stay ahead of market trends with real-time and historical data available through our easy-to-use API.（贪婪与恐惧指数，分析市场情绪，助力明智投资决策，支持实时与历史数据）
  - `get_btc_trend`  
    Get BTC trend chart for the past 3 months. Format: [[date, price, active addresses, new addresses, transaction addresses]]（获取近 3 个月 BTC 趋势图表，格式：[[日期, 当日价格, 活跃地址数, 新增地址数, 发生交易地址数]]）
  - `get_eth_trend`  
    Get the ETH trend chart for the past three months. Format: [[date, price, active addresses, new addresses]]（获取近 3 个月 ETH 趋势图表，格式：[[日期, 当日价格, 活跃地址数, 新增地址数]]）
  - `get_altcoin_season_index`  
    Altcoin Season Index page provides real-time insights into whether the cryptocurrency market is currently in Altcoin Season, based on the performance of the top 100 altcoins relative to Bitcoin over the past 90 days, with detailed charts and metrics for tracking market trends and altcoin dominance.（山寨币季指数，基于前 100 山寨币与比特币 90 天表现，实时判断市场是否处于山寨币季，含详细图表与指标）
  - `get_bitcoin_dominance`  
    Bitcoin (BTC) dominance is a metric used to measure the relative market share or dominance of Bitcoin in the overall cryptocurrency sector. It represents the percentage of Bitcoin's total market capitalization compared to the total market capitalization of all cryptocurrencies combined.（比特币主导率，衡量比特币在整个加密货币市场的市值占比）