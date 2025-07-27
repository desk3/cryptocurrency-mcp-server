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

The server implements comprehensive parameter hints using JSON Schema features:

- **Parameter Descriptions**: Each parameter includes detailed descriptions in both English and Chinese
- **Examples**: Common parameter values are provided as examples (e.g., BTCUSDT, ETHUSDT for symbols)
- **Pattern Validation**: Regular expressions ensure proper parameter format (e.g., ^[A-Z0-9]+$ for symbols)
- **Required Fields**: Clearly marked required vs optional parameters

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

- **Tools**:
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
  - `get_cycle_indicators`  
    Get crypto market cycle top indicators with fields (Indicator/Current/24h%/ReferencePrice/Triggered). Provides comprehensive market cycle analysis including Bitcoin Ahr999 Index, Pi Cycle Top Indicator, Puell Multiple, Bitcoin Rainbow Chart, and more.（加密货币市场周期顶部指标，返回字段：指标/当前/24小时%/参考价格/已触发。提供全面的市场周期分析，包括比特币Ahr999指数、Pi周期顶部指标、Puell倍数、比特币彩虹图等）
  - `get_pi_cycle_top`  
    The Pi Cycle Top indicator uses the 111DMA and 2x350DMA to identify Bitcoin market tops. When the 111DMA crosses above the 2x350DMA, it historically typically signals a cycle peak within about 3 days, reflecting Bitcoin's long-term cyclical behavior.（Pi 周期顶部指标使用 111DMA 和 2x350DMA 来识别比特币市场顶部。当 111DMA 上穿 2x350DMA 时，历史上通常在约 3 天内预示周期峰值，反映了比特币的长期周期行为。）
  - `get_rainbow_chart`  
    The Bitcoin Rainbow Chart uses a logarithmic growth curve with a color band to illustrate market sentiment and highlight potential buy or sell areas. It is not suitable for short-term predictions, but helps to identify overvaluation or undervaluation from history.（比特币彩虹图使用带有色带的对数增长曲线来说明市场情绪，并突出显示潜在的买入或卖出区域。它不适用于短期预测，但有助于从历史上识别高估或低估的情况。）
  - `get_puell_multiple`  
    The Puell Multiple assesses Bitcoin miners' revenue by dividing daily issuance (in USD) by its 365-day average. This reflects the mining pressure in the market. Low values (green areas) indicate undervaluation and strong historical buy areas, while high values (red areas) indicate overvaluation and potential sell opportunities. It provides insight into market cycles from the perspective of miners.（Puell Multiple 通过将每日发行量（美元）除以其 365 天的平均值来评估比特币矿工的收入。这反映了市场上的挖矿压力。低值（绿色区域）表示低估和强劲的历史买入区域，而高值（红色区域）表示高估和潜在的卖出机会。它从矿工的角度洞察市场周期。）
  - `get_cycles`  
    Does the Bitcoin Four-Year Cycle Exist? Discover the cryptocurrency market cycle indicator that helps you identify the top of the cryptocurrency bull market. This is a collection of publicly available signals including Pi Cycle and Puell Multiple data.（比特币四年周期是否存在？发现加密货币市场周期指标，帮助您识别加密货币牛市的顶峰。这是一个公开可用的信号集合，包括 Pi 循环和 Puell Multiple 数据。） Return fields: (puellMultiple Puell: multiple status / piCycleTop: Pi cycle top status / likelihood: cryptocurrency market cycle top indicator) 返回字段：（puellMultiple Puell：多重状态 / piCycleTop：Pi 周期顶部状态 / likelihood: 加密货币市场周期顶部指标）