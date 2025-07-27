# Desk3 MCP 服务端

一个完全兼容 [MCP (Model Context Protocol)](https://github.com/mcp-protocol/spec) 的 Desk3 加密货币数据服务端，支持 Dify、Claude、Notion MCP 等客户端。

## 主要特性

- 实现了所有 Desk3 加密货币数据接口，作为 MCP 资源和工具暴露
- 支持 HTTP、SSE、JSON-RPC 2.0
- 一键启动：`uv run desk3_service`
- 支持 Docker 部署

## 资源列表

- `desk3://gas/suggest`  
  EIP1559 Gas 建议（需 chainid 查询参数）
- `desk3://market/exchangeRate`  
  法币汇率列表
- `desk3://market/mini/24hr`  
  24 小时币价迷你行情（支持 symbol 参数，如 ETHUSDT）
- `desk3://market/price`  
  实时代币价格（支持 symbol 参数，如 ETHUSDT、BTCUSDT）
- `desk3://market/fear-greed`  
  贪婪与恐惧指数（分析市场情绪，助力明智投资决策，支持实时与历史数据）
- `desk3://market/btc/trend`  
  BTC 近 3 个月趋势图表（[[日期, 当日价格, 活跃地址数, 新增地址数, 发生交易地址数]]）
- `desk3://market/eth/trend`  
  ETH 近 3 个月趋势图表（[[日期, 当日价格, 活跃地址数, 新增地址数]]）
- `desk3://market/altcoin/season`  
  山寨币季指数（基于前 100 山寨币与比特币 90 天表现，含详细图表与指标）
- `desk3://market/bitcoin/dominance`  
  比特币主导率（衡量比特币在整个加密货币市场的市值占比）
- `desk3://market/cycle/indicators`  
  加密货币市场周期顶部指标（返回字段：指标/当前/24小时%/参考价格/已触发）
- `desk3://market/pi-cycle-top`  
  BTC Pi 周期顶部指标（使用 111DMA 和 2x350DMA 识别比特币市场顶部）
- `desk3://market/rainbow`  
  比特币彩虹价格图（使用对数增长曲线和色带说明市场情绪，识别潜在买入或卖出区域）
- `desk3://market/puell-multiple`  
  皮勒乘数计算（通过每日发行量除以其365天平均值评估比特币矿工收入，反映市场挖矿压力）
- `desk3://market/cycles`  
  简易指标：Puell 多重状态/Pi 周期顶部状态/加密货币市场周期顶部指标

## 工具列表

- `get_suggest_gas`  
  获取 EIP1559 估算 Gas 信息（需要 chainid）
  - **chainid**: 区块链网络链ID（如 1 表示以太坊主网，137 表示 Polygon）
- `get_exchange_rate`  
  获取法币汇率列表
- `get_mini_24hr`  
  获取 24 小时迷你行情（支持 symbol 参数）
  - **symbol**: 交易对符号，格式如 BTCUSDT、ETHUSDT 等。留空获取所有符号
- `get_token_price`  
  获取实时代币价格（支持 symbol 参数）
  - **symbol**: 交易对符号，格式如 BTCUSDT、ETHUSDT 等。留空获取所有符号
- `get_fear_greed_index`  
  贪婪与恐惧指数，分析市场情绪，助力明智投资决策，支持实时与历史数据
- `get_btc_trend`  
  获取近 3 个月 BTC 趋势图表
- `get_eth_trend`  
  获取近 3 个月 ETH 趋势图表
- `get_altcoin_season_index`  
  山寨币季指数，实时判断市场是否处于山寨币季，含详细图表与指标
- `get_bitcoin_dominance`  
  比特币主导率，衡量比特币在整个加密货币市场的市值占比
- `get_cycle_indicators`  
  获取加密货币市场周期顶部指标，返回字段（指标/当前/24小时%/参考价格/已触发）
- `get_pi_cycle_top`  
  Pi 周期顶部指标使用 111DMA 和 2x350DMA 识别比特币市场顶部
- `get_rainbow_chart`  
  比特币彩虹图使用带有色带的对数增长曲线来说明市场情绪，并突出显示潜在的买入或卖出区域
- `get_puell_multiple`  
  Puell Multiple 通过将每日发行量（美元）除以其 365 天的平均值来评估比特币矿工的收入
- `get_cycles`  
  比特币四年周期是否存在？发现加密货币市场周期指标，帮助您识别加密货币牛市的顶峰

## 配置

- 需要有效的 `DESK3_API_KEY`（可在环境变量或 `.env` 文件中设置）

## 快速开始

### 依赖

- Python 3.12 及以上
- [uv](https://docs.astral.sh/uv/getting-started/installation/) 包管理器

### 安装与运行

```bash
uv sync
uv run desk3_service
```

### Docker

```bash
docker build -t desk3-service .
docker run -e DESK3_API_KEY=..密钥.. -p 8100:8100 desk3-service
```

- 启动容器时请务必加上 `-p 8100:8100`，以便外部访问 HTTP/SSE 服务。

## 启动方式

本项目支持两种启动方式：

### 1. HTTP/SSE 服务端（推荐）

在 0.0.0.0:8100 启动 Starlette HTTP/SSE 服务，适用于 Dify、Claude、Notion MCP 等客户端。

```bash
# 推荐：直接用 Python 启动
PYTHONPATH=src python -m desk3_service.http_server
# 或启动 Starlette MCP 变体
PYTHONPATH=src python -m desk3_service.starlette_mcp_server
```

如需用 uv/pyproject.toml script 启动，也可为 http_server 或 starlette_mcp_server 添加 script。

### 2. MCP 标准输入输出模式（高级用法）

以纯 MCP stdio server 方式启动，适合 CLI 或高级集成（不提供 HTTP/SSE）：

```bash
uv run desk3_service
```

此模式仅当您想通过 stdin/stdout 使用 MCP 时才需要（不推荐大多数用户使用）。

## 故障排除

- 确保 `uv` 已安装并包含在您的 PATH 中。
- 确保您的 `DESK3_API_KEY` 有效。
- 如果使用 Docker，请使用 `-e DESK3_API_KEY=...` 设置 API 密钥。