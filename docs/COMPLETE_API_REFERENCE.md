# RustChain REST API 完整参考文档

> **RustChain v1.0.0** — 完整 API 端点参考，含中文说明、请求/响应示例和 Python SDK 调用方法。
> 
> **基础地址**: `https://rustchain.org`
> **认证方式**: X-API-Key (Header) 或 Bearer JWT

---

## 目录

1. [系统端点](#1-系统端点)
2. [区块链端点](#2-区块链端点)
3. [钱包端点](#3-钱包端点)
4. [挖矿端点](#4-挖矿端点)
5. [认证端点](#5-认证端点)
6. [SophiaCore 智能审查](#6-sophiacore-智能审查)

---

## 1. 系统端点

### 1.1 健康检查

**`GET /health`**

检查 RustChain 节点的健康状态。

#### 请求

```bash
curl https://rustchain.org/health
```

#### 响应

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": 1640000000
}
```

#### Python SDK

```python
from rustchain_sdk import RustChainClient

client = RustChainClient(base_url="https://rustchain.org")
health = client.health_check()
print(f"状态: {health['status']}, 版本: {health['version']}")
```

#### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| status | string | 节点状态：healthy / degraded / offline |
| version | string | 当前运行的软件版本 |
| timestamp | integer | 服务器 Unix 时间戳 |

---

## 2. 区块链端点

### 2.1 获取当前 Epoch

**`GET /epoch`**

返回当前 Epoch（周期）信息。

#### 请求

```bash
curl https://rustchain.org/epoch
```

#### 响应

```json
{
  "epoch": 123,
  "block_height": 456789,
  "timestamp": 1640000000
}
```

#### Python SDK

```python
epoch_info = client.get_epoch()
print(f"Epoch: {epoch_info['epoch']}, 区块高度: {epoch_info['block_height']}")
```

#### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| epoch | integer | 当前周期编号 |
| block_height | integer | 当前区块高度 |
| timestamp | integer | 当前时间戳 |

### 2.2 获取区块信息

**`GET /block/{block_number}`**

根据区块号获取区块详细信息。

#### 请求

```bash
curl https://rustchain.org/block/12345
```

#### 响应

```json
{
  "number": 12345,
  "hash": "0xabc123def456...",
  "parent_hash": "0x789ghi012...",
  "timestamp": 1640000000,
  "transactions": ["0xtx1...", "0xtx2..."],
  "miner": "0xminer123...",
  "difficulty": "1000000",
  "total_difficulty": "500000000"
}
```

#### Python SDK

```python
block = client.get_block(12345)
print(f"区块 #{block['number']}, 哈希: {block['hash'][:16]}...")
print(f"矿工: {block['miner']}")
print(f"包含交易: {len(block['transactions'])} 笔")
```

#### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| number | integer | 区块号 |
| hash | string | 区块哈希 |
| parent_hash | string | 父区块哈希 |
| timestamp | integer | 区块时间戳 |
| transactions | array | 交易哈希列表 |
| miner | string | 出块矿工地址 |
| difficulty | string | 当前难度 |
| total_difficulty | string | 累计难度 |

---

## 3. 钱包端点

### 3.1 查询余额

**`GET /wallet/balance?address=<钱包地址>`**

查询指定钱包地址的 RTC 余额。

#### 请求

```bash
curl "https://rustchain.org/wallet/balance?address=0x742d35Cc6634C0532925a3b844Bc9e7595f..."
```

#### 响应

```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f...",
  "balance": "1.2345",
  "balance_wei": "1234500000000000000"
}
```

#### Python SDK

```python
balance = client.get_balance("0x742d35Cc6634C0532925a3b844Bc9e7595f...")
print(f"余额: {balance['balance']} RTC")
print(f"余额 (wei): {balance['balance_wei']}")
```

#### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| address | string | 查询的钱包地址 |
| balance | string | 余额（RTC 单位，18 位小数） |
| balance_wei | string | 余额（最小单位 wei） |

### 3.2 查询交易列表

**`GET /transactions?address=<地址>&limit=20`**

获取指定地址的交易记录。

#### 请求

```bash
curl "https://rustchain.org/transactions?address=0x742d35Cc...&limit=10"
```

#### 响应

```json
{
  "transactions": [
    {
      "hash": "0xabc123...",
      "from": "0xsender...",
      "to": "0xreceiver...",
      "value": "1.5",
      "timestamp": 1640000000
    }
  ]
}
```

#### Python SDK

```python
txs = client.get_transactions("0x742d35Cc...", limit=10)
for tx in txs['transactions']:
    print(f"{tx['hash'][:10]}... | {tx['from'][:8]}... -> {tx['to'][:8]}... | {tx['value']} RTC")
```

---

## 4. 挖矿端点

### 4.1 获取矿工列表

**`GET /api/miners?limit=20&offset=0`**

获取网络上的活跃矿工列表。

#### 请求

```bash
curl "https://rustchain.org/api/miners?limit=10&offset=0"
```

#### 响应

```json
{
  "miners": [
    {
      "address": "0xminer1...",
      "hashrate": "1500 H/s",
      "blocks": 42
    }
  ],
  "total": 1523
}
```

#### Python SDK

```python
miners = client.get_miners(limit=10, offset=0)
for miner in miners['miners']:
    print(f"矿工: {miner['address'][:10]}... | 算力: {miner['hashrate']} | 出块: {miner['blocks']}")
print(f"总算工数: {miners['total']}")
```

---

## 5. 认证端点

### 5.1 提交认证 (Attestation)

**`POST /attest/submit`**

向网络提交硬件认证证明。这是 RustChain PoA（硬件证明共识）的核心端点。

#### 请求

```bash
curl -X POST https://rustchain.org/attest/submit \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "hardware_fingerprint": "abc123...",
      "timestamp": 1640000000,
      "nonce": 42
    },
    "signature": "0xsignature..."
  }'
```

#### 响应

```json
{
  "tx_hash": "0xabc123...",
  "status": "submitted"
}
```

#### Python SDK

```python
result = client.submit_attestation(
    data={
        "hardware_fingerprint": "abc123...",
        "timestamp": 1640000000,
        "nonce": 42
    },
    signature="0xsignature..."
)
print(f"交易哈希: {result['tx_hash']}")
print(f"状态: {result['status']}")
```

#### 注意事项

- `data` 字段必须包含完整的硬件指纹信息
- `signature` 是使用矿工私钥对 data 字段的 Ed25519 签名
- 认证成功后，矿工将被注册到网络并获得挖矿资格

---

## 6. SophiaCore 智能审查

> **RIP-306**: Sophia Elya 是 RustChain 的 AI 驱动的硬件验证系统，通过分析矿工指纹来检测 Sybil 攻击和欺诈行为。

### 6.1 检查矿工指纹

**`POST /sophia/inspect`**

提交指纹包进行 Sophia Elya 语义分析，返回审查结果。

#### 请求

```bash
curl -X POST https://rustchain.org/sophia/inspect \
  -H "Content-Type: application/json" \
  -d '{
    "miner_id": "miner_001",
    "fingerprint": {
      "cpu_id": "Intel-XYZ-123",
      "gpu_id": "NVIDIA-ABC-456",
      "mac_address": "AA:BB:CC:DD:EE:FF"
    },
    "hardware": {
      "cpu_cores": 8,
      "gpu_model": "RTX 3080"
    },
    "epoch": 123
  }'
```

#### 响应

```json
{
  "miner_id": "miner_001",
  "verdict": "APPROVED",
  "confidence": 0.95,
  "reasoning": "Hardware fingerprint matches expected patterns for claimed configuration",
  "flags": [],
  "emoji": "✅",
  "phase": "advisory",
  "effective_verdict": "APPROVED",
  "created_at": "2024-01-15T12:00:00Z"
}
```

#### 审查结果说明

| 判定 | 含义 |
|------|------|
| APPROVED ✅ | 硬件指纹正常，可以信任 |
| CAUTIOUS ⚠️ | 存在轻微异常，需要观察 |
| SUSPICIOUS 🚨 | 发现明显异常，可能为 Sybil 攻击 |
| REJECTED ❌ | 确认欺诈，禁止挖矿 |

#### Python SDK

```python
result = client.sophia_inspect(
    miner_id="miner_001",
    fingerprint={
        "cpu_id": "Intel-XYZ-123",
        "gpu_id": "NVIDIA-ABC-456",
        "mac_address": "AA:BB:CC:DD:EE:FF"
    },
    hardware={"cpu_cores": 8, "gpu_model": "RTX 3080"},
    epoch=123
)
print(f"判定: {result['verdict']} (置信度: {result['confidence']})")
print(f"原因: {result['reasoning']}")
```

### 6.2 查询矿工最新审查状态

**`GET /sophia/status/{miner_id}`**

#### 请求

```bash
curl https://rustchain.org/sophia/status/miner_001
```

#### 响应

```json
{
  "miner_id": "miner_001",
  "verdict": "APPROVED",
  "confidence": 0.95,
  "reasoning": "...",
  "flags": [],
  "emoji": "✅",
  "phase": "advisory"
}
```

#### 404 响应

```json
{
  "error": "No inspections found for miner_001"
}
```

### 6.3 查询矿工审查历史

**`GET /sophia/history/{miner_id}?limit=50`**

#### 请求

```bash
curl "https://rustchain.org/sophia/history/miner_001?limit=10"
```

#### 响应

```json
{
  "miner_id": "miner_001",
  "count": 10,
  "inspections": [
    {
      "verdict": "APPROVED",
      "confidence": 0.95,
      "created_at": "2024-01-15T12:00:00Z"
    },
    {
      "verdict": "CAUTIOUS",
      "confidence": 0.60,
      "created_at": "2024-01-14T12:00:00Z"
    }
  ]
}
```

### 6.4 获取审查统计

**`GET /sophia/stats`**

#### 响应

```json
{
  "total_inspections": 15230,
  "by_verdict": {
    "APPROVED": 14500,
    "CAUTIOUS": 500,
    "SUSPICIOUS": 180,
    "REJECTED": 50
  },
  "avg_confidence": 0.92,
  "pending_reviews": 23
}
```

### 6.5 获取待人工审查列表

**`GET /sophia/pending`**

获取需要人工复核的审查结果。

#### 响应

```json
{
  "count": 23,
  "reviews": [
    {
      "miner_id": "miner_042",
      "verdict": "CAUTIOUS",
      "confidence": 0.45,
      "reasoning": "Unusual GPU memory pattern detected",
      "flags": ["gpu_memory_mismatch"]
    }
  ]
}
```

### 6.6 管理员覆盖判定

**`POST /sophia/override`**

管理员可以覆盖 Sophia 的自动判定。需要 HTTP Basic Auth。

#### 请求

```bash
curl -X POST https://rustchain.org/sophia/override \
  -u admin:password \
  -H "Content-Type: application/json" \
  -d '{
    "inspection_id": 1234,
    "verdict": "REJECTED",
    "reason": "Confirmed Sybil attack via manual investigation"
  }'
```

#### 响应

```
200 OK
```

### 6.7 批量查询最新判定

**`POST /sophia/batch-status`**

批量查询最多 100 个矿工的最新判定结果。

#### 请求

```bash
curl -X POST https://rustchain.org/sophia/batch-status \
  -H "Content-Type: application/json" \
  -d '{
    "miner_ids": ["miner_001", "miner_002", "miner_003"]
  }'
```

#### 响应

```json
{
  "results": {
    "miner_001": {"verdict": "APPROVED", "confidence": 0.95},
    "miner_002": {"verdict": "CAUTIOUS", "confidence": 0.60},
    "miner_003": {"verdict": "APPROVED", "confidence": 0.88}
  }
}
```

### 6.8 触发即时审查

**`POST /sophia/trigger/{miner_id}`**

由 Sybil 风险评分器调用，触发对指定矿工的即时审查。需要 Bearer Token 认证。

#### 请求

```bash
curl -X POST https://rustchain.org/sophia/trigger/miner_001 \
  -H "Authorization: Bearer <trigger_secret>"
```

### 6.9 SophiaCore 服务健康

**`GET /sophia/health`**

检查 SophiaCore 服务健康状态，包括 Ollama 主机状态。

### 6.10 Prometheus 指标

**`GET /sophia/metrics`**

返回 Prometheus 格式的指标数据。

### 6.11 管理员审查面板

**`GET /sophia/dashboard`**

返回管理员随机审查的 HTML 仪表板页面。

---

## 错误码参考

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 认证失败 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

### 错误响应格式

```json
{
  "code": 400,
  "message": "Invalid address format",
  "details": {
    "expected": "0x followed by 40 hex characters",
    "received": "invalid_address"
  }
}
```

---

*文档版本: 1.0 | 最后更新: 2026-05-19*
