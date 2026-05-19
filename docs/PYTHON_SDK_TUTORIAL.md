# RustChain Python SDK 入门教程

> **目标读者**：想通过 Python 与 RustChain 区块链进行交互的开发者  
> **前置知识**：Python 3.8+、异步编程基础（async/await）  
> **SDK 版本**：1.0.0  
> **官方节点**：`https://50.28.86.131`（自签名证书，生产环境请配置证书）

---

## 目录

1. [安装与环境准备](#1-安装与环境准备)
2. [快速开始：连接节点查询数据](#2-快速开始连接节点查询数据)
3. [钱包模块：创建与管理](#3-钱包模块创建与管理)
4. [转账交易：从签名到上链](#4-转账交易从签名到上链)
5. [硬件证明（Attestation）](#5-硬件证明attestation)
6. [治理功能：提案与投票](#6-治理功能提案与投票)
7. [区块链浏览器接口](#7-区块链浏览器接口)
8. [Epoch 与奖励查询](#8-epoch-与奖励查询)
9. [异常处理](#9-异常处理)
10. [CLI 命令行工具](#10-cli-命令行工具)
11. [完整实战案例：批量监控矿工余额](#11-完整实战案例批量监控矿工余额)

---

## 1. 安装与环境准备

### 1.1 通过 pip 安装（推荐）

```bash
pip install rustchain
```

### 1.2 开发模式安装（参与 SDK 开发时使用）

```bash
git clone https://github.com/Scottcjn/rustchain-bounties.git
cd rustchain-bounties/sdk/python
pip install -e ".[dev]"
```

### 1.3 依赖说明

| 依赖包 | 版本要求 | 用途 |
|--------|----------|------|
| `httpx` | ≥ 0.25.0 | 异步 HTTP 客户端（核心依赖） |
| `click` | ≥ 8.0.0 | CLI 命令行工具 |
| `cryptography` | ≥ 41.0.0 | 可选，启用真实 Ed25519 签名 |

> ⚠️ **SSL 证书说明**：官方节点 `50.28.86.131` 使用自签名证书。`RustChainClient` 会自动检查 `~/.rustchain/node_cert.pem` 是否存在——若存在则使用该证书，否则使用系统 CA 证书。

```bash
# 若遇到 SSL 验证错误，可临时跳过（仅用于开发）
# 生产环境请从节点获取并安装正式证书
export SSL_CERT_FILE=/path/to/cert.pem
```

### 1.4 验证安装

```python
import rustchain_sdk
print(rustchain_sdk.__version__)  # 输出: 1.0.0
```

---

## 2. 快速开始：连接节点查询数据

### 2.1 初始化客户端

```python
import asyncio
from rustchain_sdk import RustChainClient

async def main():
    # 使用默认节点地址（推荐）
    client = RustChainClient()

    # 也可以指定自定义节点
    # client = RustChainClient(base_url="https://your-custom-node.example.com")
    # client = RustChainClient(base_url="https://50.28.86.131", timeout=60.0)

    async with client:
        # 在此上下文中使用 client，结束时自动关闭连接
        pass

asyncio.run(main())
```

`RustChainClient` 支持**异步上下文管理器**（`async with`），离开上下文时自动关闭 HTTP 连接。建议始终使用此写法。

### 2.2 健康检查

```python
async def check_health():
    async with RustChainClient() as client:
        health = await client.health()
        print(health)
```

返回示例：

```json
{
    "ok": true,
    "uptime_s": 31284,
    "version": "2.2.1-rip200",
    "backup_age_hours": 8.2,
    "db_rw": true,
    "tip_age_slots": 0
}
```

各字段含义：

| 字段 | 类型 | 说明 |
|------|------|------|
| `ok` | bool | 节点是否正常运行 |
| `uptime_s` | float | 运行时间（秒） |
| `version` | string | 节点软件版本 |
| `backup_age_hours` | float | 最新备份距今小时数 |
| `db_rw` | bool | 数据库读写状态 |
| `tip_age_slots` | int | 链头区块距当前槽位差 |

### 2.3 获取当前 Epoch 信息

```python
async def get_current_epoch():
    async with RustChainClient() as client:
        epoch_info = await client.get_epoch()
        print(f"当前 Epoch: {epoch_info['epoch']}")
        print(f"Epoch 奖励池: {epoch_info['epoch_pot']} RTC")
        print(f"已注册矿工数: {epoch_info['enrolled_miners']}")
        print(f"每 Epoch 区块数: {epoch_info['blocks_per_epoch']}")
```

返回示例：

```json
{
    "epoch": 104,
    "epoch_pot": 1.5,
    "enrolled_miners": 30,
    "blocks_per_epoch": 144,
    "slot": 15066,
    "total_supply_rtc": 8388608
}
```

### 2.4 获取链头信息

```python
async def get_chain_tip():
    async with RustChainClient() as client:
        tip = await client.get_headers_tip()
        print(f"当前链头高度: {tip.get('height')}")
        print(f"链头哈希: {tip.get('hash')}")
        print(f"时间戳: {tip.get('timestamp')}")
```

### 2.5 获取活跃矿工列表

```python
async def list_miners():
    async with RustChainClient() as client:
        miners = await client.get_miners()
        print(f"活跃矿工总数: {len(miners)}")
        for miner in miners[:5]:
            print(f"  地址: {miner.get('address')}, 算力: {miner.get('hashrate')}")
```

---

## 3. 钱包模块：创建与管理

`RustChainWallet` 提供 BIP39 助记词钱包的完整实现，包括私钥推导、地址生成、Ed25519 签名和导入/导出。

### 3.1 创建新钱包

**方式一：从零创建（推荐）**

```python
from rustchain_sdk import RustChainWallet

# 创建 12 词钱包（128 位熵）
wallet = RustChainWallet.create()

# 创建 24 词钱包（256 位熵，更高安全性）
# wallet = RustChainWallet.create(strength=256)

print("钱包地址:", wallet.address)        # 例: RTCa1b2c3d4e5f6...
print("公钥(HEX):", wallet.public_key_hex)
print("助记词:", " ".join(wallet.seed_phrase))
```

> ⚠️ **安全警告**：助记词是恢复钱包的唯一凭证！请务必安全备份，切勿在代码中硬编码或提交到 Git 仓库。

**方式二：从助记词恢复**

```python
# 从 12 词或 24 词助记词恢复钱包
words = ["abandon", "ability", "able", "about", "above", "absent",
         "absorb", "abstract", "absurd", "abuse", "access", "accident"]
wallet = RustChainWallet.from_seed_phrase(words)

print(wallet.address)
```

### 3.2 钱包属性一览

```python
wallet = RustChainWallet.create()

print(wallet.address)        # RTC 格式地址 (RTC...)
print(wallet.public_key_hex) # 公钥十六进制字符串
print(wallet.seed_phrase)    # BIP39 助记词列表
print(wallet.private_key_hex) # 私钥十六进制（仅展示，实际应保密）
```

### 3.3 钱包的导入与导出

**导出（生成可存储的 JSON）**

```python
# 导出的数据包含助记词，存储时务必加密
exported = wallet.export()
print(exported)
# {
#   "version": 1,
#   "address": "RTcab...",
#   "seed_phrase": ["abandon", "ability", ...],
#   "derivation_path": "m/44'/9000'/0'/0/0"
# }

# 将导出数据保存到文件（实际应用中应加密存储）
import json
with open("wallet_backup.json", "w") as f:
    json.dump(exported, f)
```

**导入（从备份恢复）**

```python
with open("wallet_backup.json") as f:
    data = json.load(f)

restored_wallet = RustChainWallet.import_(data)
print(restored_wallet.address)  # 与原钱包地址一致
```

### 3.4 地址前缀说明

RustChain 使用 `RTC` 作为地址前缀，后接 40 位十六进制字符（取自公钥 SHA256d 哈希的前 20 字节）。与以太坊的 `0x` 前缀和比特币的 `1/` 前缀类似，用于区分不同链上的地址格式。

---

## 4. 转账交易：从签名到上链

完整的转账流程分为三步：① 查询余额 → ② 签名交易 → ③ 提交上链。

### 4.1 查询余额

```python
async def check_balance(wallet_address: str):
    async with RustChainClient() as client:
        balance_info = await client.get_balance(wallet_address)
        print(f"地址: {balance_info.get('address')}")
        print(f"余额: {balance_info.get('balance')} RTC")
        print(f"余额(wei): {balance_info.get('balance_wei')}")
```

**返回示例**

```json
{
    "address": "RTC1a2b3c4d5e6f...",
    "balance": "12.345",
    "balance_wei": "12345000000000000000"
}
```

> **注意**：RustChain 中金额可以以小数 RTC 表示，`balance_wei` 字段提供以最小单位（类似以太坊的 wei）表示的精确整数值。转账时的 `amount` 参数使用最小单位。

### 4.2 构建并签名转账

```python
from rustchain_sdk import RustChainWallet

wallet = RustChainWallet.create()
print(f"发款方地址: {wallet.address}")

# 构建签名转账
# amount: 最小单位（1 RTC = 10^18 最小单位）
# fee: 手续费，最小单位（建议 0 以降低成本）
transfer = wallet.sign_transfer(
    to_address="RTCrecipient_address_here",
    amount=1_000_000_000_000,  # 0.001 RTC（以最小单位）
    fee=0
)

print(f"发款方: {transfer['from']}")
print(f"收款方: {transfer['to']}")
print(f"金额: {transfer['amount']} 最小单位")
print(f"手续费: {transfer['fee']}")
print(f"时间戳: {transfer['timestamp']}")
print(f"签名: {transfer['signature'][:32]}...")
```

`sign_transfer()` 的内部逻辑：

```
payload = f"{from_address}:{to_address}:{amount}:{fee}:{timestamp}"
signature = Ed25519_sign(private_key, payload.encode())
```

这意味着签名覆盖了完整的转账语义，包括时间戳——可以防止重放攻击（Replay Attack）。

### 4.3 提交转账到链上

```python
async def send_transaction(wallet, to_address: str, amount: int):
    async with RustChainClient() as client:
        result = await client.wallet_transfer_with_wallet(
            wallet=wallet,
            to_address=to_address,
            amount=amount,
            fee=0,
        )
        print(f"交易哈希: {result.get('tx_hash')}")
        print(f"状态: {result.get('status')}")
        return result
```

`wallet_transfer_with_wallet()` 是最简洁的写法——它内部自动完成签名并提交两步操作。如果你想分开处理，也可以手动调用：

```python
async def send_transaction_manual(wallet, to_address: str, amount: int):
    async with RustChainClient() as client:
        # 第一步：本地签名
        transfer = wallet.sign_transfer(to_address, amount, fee=0)

        # 第二步：提交签名交易
        result = await client.transfer_signed(
            from_address=transfer["from"],
            to_address=transfer["to"],
            amount=transfer["amount"],
            fee=transfer["fee"],
            signature=transfer["signature"],
            timestamp=transfer["timestamp"],
        )
        print(f"交易哈希: {result.get('tx_hash')}")
```

### 4.4 查询交易历史

```python
async def get_wallet_history(wallet_address: str):
    async with RustChainClient() as client:
        history = await client.get_wallet_history(wallet_address, limit=20)
        print(f"交易总数: {len(history.get('transactions', []))}")
        for tx in history.get("transactions", [])[:5]:
            print(f"  [{tx.get('type')}] {tx.get('from')} -> {tx.get('to')}, "
                  f"金额: {tx.get('amount')}, 状态: {tx.get('status')}")
```

### 4.5 完整转账示例

```python
import asyncio
from rustchain_sdk import RustChainClient, RustChainWallet

async def full_transfer_demo():
    # 场景：创建新钱包，查询余额，构造并提交转账

    # 1. 创建钱包
    sender = RustChainWallet.create()
    print(f"发款钱包地址: {sender.address}")
    print(f"助记词: {' '.join(sender.seed_phrase)}")

    # 2. 查询余额
    async with RustChainClient() as client:
        balance = await client.get_balance(sender.address)
        print(f"当前余额: {balance.get('balance')} RTC")

    # 3. 假设收款方地址（请替换为真实地址）
    recipient_address = "RTCabcd1234..."

    # 4. 构建并提交转账（此例中余额不足，实际会失败）
    # amount = 1000 最小单位 = 0.000000000001 RTC
    async with RustChainClient() as client:
        try:
            result = await client.wallet_transfer_with_wallet(
                wallet=sender,
                to_address=recipient_address,
                amount=1000,
                fee=0,
            )
            print(f"✅ 转账成功！交易哈希: {result.get('tx_hash')}")
        except Exception as e:
            print(f"❌ 转账失败: {e}")

asyncio.run(full_transfer_demo())
```

---

## 5. 硬件证明（Attestation）

RustChain 是一个 Proof-of-Antiquity（古董证明）区块链，矿工通过**硬件证明**机制证明其使用的是真实古董硬件。Attestation 是矿工参与挖矿奖励的核心步骤。

### 5.1 获取证明状态

```python
async def get_attestation_status(miner_public_key: str):
    async with RustChainClient() as client:
        status = await client.get_attestation_status(miner_public_key)
        print(f"矿工公钥: {status.get('miner_public_key')}")
        print(f"证明状态: {status.get('status')}")
        print(f"古董等级: {status.get('antique_level')}")
        print(f"奖励倍数: {status.get('reward_multiplier')}")
```

### 5.2 获取证明挑战

第一步：向节点请求一个**随机挑战值**（与当前 Epoch 绑定）：

```python
async def request_attestation_challenge(miner_public_key: str):
    async with RustChainClient() as client:
        challenge_data = await client.attest_challenge(miner_public_key)
        print(f"挑战值: {challenge_data.get('challenge')}")
        print(f"过期时间: {challenge_data.get('expires_at')}")
        return challenge_data
```

### 5.3 提交证明

第二步：使用挑战值和私钥签名，提交证明：

```python
from rustchain_sdk import RustChainWallet

async def submit_attestation(
    miner_public_key: str,
    wallet: RustChainWallet
):
    async with RustChainClient() as client:
        # 获取挑战
        challenge_data = await client.attest_challenge(miner_public_key)
        challenge = challenge_data["challenge"]

        # 用钱包私钥对挑战进行签名
        signature_bytes = wallet.sign(challenge.encode())
        challenge_response = signature_bytes.hex()

        # 提交证明
        result = await client.attest_submit(
            miner_public_key=miner_public_key,
            challenge_response=challenge_response,
            signature=wallet.public_key_hex,  # 矿工公钥作为签名
        )
        print(f"✅ 证明提交成功: {result}")
        return result
```

**Attestation 完整流程图**

```
矿工                        节点                        链上
 │                           │                          │
 │  ── attest_challenge() ──►│                          │
 │◄── challenge (epoch-bound)──│                          │
 │                           │                          │
 │  sign(challenge)          │                          │
 │                           │                          │
 │──── attest_submit() ──────►│                          │
 │                           │── verify & store ───────►│
 │◄── result ────────────────│                          │
 │                           │                          │
```

### 5.4 查询奖励倍数

古董硬件等级越高，奖励倍数越大：

```python
async def get_reward_multiplier():
    async with RustChainClient() as client:
        multiplier_info = await client.get_bounty_multiplier()
        print(f"当前奖励倍数: {multiplier_info.get('multiplier')}")
        print(f"古董等级: {multiplier_info.get('antique_level')}")
        print(f"生效中: {multiplier_info.get('active')}")
```

---

## 6. 治理功能：提案与投票

RustChain 的链上治理允许代币持有者提交参数变更提案，并对提案进行投票。

### 6.1 查看所有提案

```python
async def list_proposals(status: str = None):
    """
    列出治理提案
    status 可选值: "active", "passed", "rejected", "executed"
    """
    async with RustChainClient() as client:
        proposals = await client.list_governance_proposals(status=status)
        for p in proposals:
            print(f"[#{p['proposal_id']}] {p['title']} - 状态: {p['status']}")
            print(f"  类型: {p['proposal_type']}")
            print(f"  赞成票: {p.get('yes_votes', 0)}, 反对票: {p.get('no_votes', 0)}")
```

### 6.2 提交新提案

```python
async def create_proposal(
    proposer_wallet: RustChainWallet,
    proposal_type: str,
    description: str,
    payload: dict
):
    """
    提交一个新的治理提案

    Args:
        proposer_wallet: 提案人的钱包
        proposal_type:  提案类型，如 "param_change", "treasury", "upgrade"
        description:    人类可读的提案描述
        payload:         提案携带的具体参数（如参数名和新值）
    """
    async with RustChainClient() as client:
        result = await client.governance_propose(
            proposer=proposer_wallet.address,
            proposal_type=proposal_type,
            description=description,
            payload=payload,
        )
        print(f"✅ 提案已提交！提案ID: {result.get('proposal_id')}")
        return result
```

**使用示例：提交参数变更提案**

```python
import asyncio
from rustchain_sdk import RustChainClient, RustChainWallet

async def main():
    wallet = RustChainWallet.create()

    async with RustChainClient() as client:
        result = await client.governance_propose(
            proposer=wallet.address,
            proposal_type="param_change",
            description="将每 Epoch 区块奖励从 1.5 RTC 提高到 2.0 RTC",
            payload={
                "parameter": "blocks_per_epoch_reward",
                "current_value": 1.5,
                "proposed_value": 2.0,
                "reason": "提高矿工收益，增强网络安全",
            },
        )
        print(f"提案ID: {result['proposal_id']}")

asyncio.run(main())
```

### 6.3 投票

```python
async def vote_on_proposal(
    voter_wallet: RustChainWallet,
    proposal_id: int,
    vote: str  # "yes", "no", 或 "abstain"
):
    """
    对提案进行投票

    Args:
        voter_wallet: 投票人钱包
        proposal_id:   提案ID
        vote:          投票选项: "yes"（赞成）, "no"（反对）, "abstain"（弃权）
    """
    # 对投票内容签名
    vote_payload = f"{voter_wallet.address}:{proposal_id}:{vote}".encode()
    signature = voter_wallet.sign(vote_payload).hex()

    async with RustChainClient() as client:
        result = await client.governance_vote(
            voter=voter_wallet.address,
            proposal_id=proposal_id,
            vote=vote,
            signature=signature,
        )
        print(f"✅ 投票成功: {result.get('tx_hash')}")
        return result
```

---

## 7. 区块链浏览器接口

SDK 提供了封装好的浏览器数据查询接口，方便获取链上公开数据。

### 7.1 查询最新区块

```python
async def get_recent_blocks(limit: int = 20):
    async with RustChainClient() as client:
        blocks = await client.explorer_blocks(limit=limit)
        for block in blocks:
            print(f"区块 #{block['height']} | "
                  f"哈希: {block['hash'][:16]}... | "
                  f"时间: {block['timestamp']} | "
                  f"交易数: {block['tx_count']}")
```

**返回字段说明**

| 字段 | 说明 |
|------|------|
| `height` | 区块高度 |
| `hash` | 区块哈希值 |
| `timestamp` | 区块时间戳（Unix 秒） |
| `tx_count` | 区块内交易数量 |
| `miner` | 挖出该区块的矿工地址 |
| `reward` | 区块奖励金额 |

### 7.2 查询交易列表

```python
async def get_transactions(address: str = None, limit: int = 50):
    """
    获取交易列表，可按地址过滤

    Args:
        address: 可选，筛选特定地址的所有交易
        limit:   返回数量上限
    """
    async with RustChainClient() as client:
        txs = await client.explorer_transactions(address=address, limit=limit)
        for tx in txs:
            print(f"[{tx['type']}] {tx['from'][:12]}... -> {tx['to'][:12]}... | "
                  f"金额: {tx['amount']} | 状态: {tx['status']}")
```

---

## 8. Epoch 与奖励查询

### 8.1 查询特定 Epoch 的奖励分配

```python
async def get_epoch_reward_distribution(epoch_number: int):
    async with RustChainClient() as client:
        rewards = await client.get_epoch_rewards(epoch_number)
        print(f"Epoch {epoch_number} 奖励分配：")
        print(f"  总奖励池: {rewards.get('total_pot')} RTC")
        print(f"  参与矿工数: {rewards.get('participating_miners')}")
        for entry in rewards.get("allocations", [])[:5]:
            print(f"  矿工 {entry['miner'][:12]}... 获得 {entry['reward']} RTC")
```

---

## 9. 异常处理

SDK 定义了结构化的异常体系，便于精确定位错误来源：

```
RustChainError (基类)
├── ConnectionError      — 节点连接失败
├── APIError             — API 返回非 2xx 状态码
│   └── 属性: status_code, response_body
├── AuthenticationError  — 认证/授权失败
├── ValidationError      — 输入参数校验失败
├── WalletError          — 钱包操作错误（创建/签名/导入）
├── AttestationError     — 硬件证明流程错误
├── GovernanceError      — 治理操作错误
├── HealthError          — 节点健康检查失败
├── EpochError           — Epoch 操作错误
├── TransferError        — 转账交易失败
└── RPCError             — 通用 RPC 调用错误
```

### 9.1 完整异常处理示例

```python
import asyncio
from rustchain_sdk import (
    RustChainClient,
    RustChainWallet,
    RustChainError,
    ConnectionError as RCConnectionError,
    APIError,
    ValidationError,
)

async def robust_transfer():
    wallet = RustChainWallet.create()
    to_address = "RTCrecipient..."

    try:
        async with RustChainClient() as client:
            # 检查连接
            health = await client.health()
            if not health.get("ok"):
                raise ConnectionError("节点健康检查失败")

            # 检查余额
            balance = await client.get_balance(wallet.address)
            balance_rtc = float(balance.get("balance", 0))
            if balance_rtc < 0.001:
                print("余额不足，跳过转账")
                return

            # 执行转账
            result = await client.wallet_transfer_with_wallet(
                wallet=wallet,
                to_address=to_address,
                amount=1_000_000,  # 0.000001 RTC
                fee=0,
            )
            print(f"✅ 转账成功: {result.get('tx_hash')}")

    except RCConnectionError as e:
        print(f"🔌 连接错误: {e.message}")
        print("请检查节点地址和网络连接")
    except APIError as e:
        print(f"📡 API 错误 [{e.status_code}]: {e.message}")
        if e.response_body:
            print(f"   响应体: {e.response_body}")
    except ValidationError as e:
        print(f"⚠️  参数校验失败: {e.message}")
    except RustChainError as e:
        print(f"❌ SDK 错误: {e.message}")
        if e.details:
            print(f"   详情: {e.details}")
    except Exception as e:
        print(f"💥 未知错误: {type(e).__name__}: {e}")

asyncio.run(robust_transfer())
```

### 9.2 常见错误及解决方案

| 错误场景 | 异常类型 | 解决方案 |
|----------|----------|----------|
| 节点不可达 | `ConnectionError` | 检查 URL 是否正确，网络是否通畅 |
| SSL 证书错误 | `ConnectionError` | 安装节点证书到 `~/.rustchain/node_cert.pem` |
| 余额不足 | 业务逻辑（无异常） | 查询余额后再发起转账 |
| 无效地址格式 | `ValidationError` | 确认地址以 `RTC` 开头且长度为正确 |
| 交易签名无效 | `APIError` (400) | 检查签名算法是否为 Ed25519 |
| 提案不存在 | `APIError` (404) | 检查 `proposal_id` 是否正确 |

---

## 10. CLI 命令行工具

安装 SDK 后会自动注册 `rustchain` 命令行工具：

```bash
# 创建新钱包
rustchain wallet create

# 查询余额
rustchain wallet balance RTC1a2b3c4d5e6f...

# 从助记词恢复钱包（12 词或 24 词）
rustchain wallet import "word1 word2 ... word12"

# 发送 RTC
rustchain wallet send <from_address> <to_address> <amount>

# 查看节点状态
rustchain node status

# 查看当前 Epoch
rustchain epoch info

# 列出矿工
rustchain miners list

# 执行硬件证明
rustchain attest <wallet_address>
```

---

## 11. 完整实战案例：批量监控矿工余额

以下是一个生产级别的脚本，演示如何结合 SDK 的多个功能来构建实用的监控系统：

```python
"""
RustChain 矿工余额监控脚本
功能：
1. 从配置文件加载矿工地址列表
2. 批量查询每个矿工的余额
3. 检测余额异常变动（如大额转出）
4. 将结果输出为表格并记录到日志

运行方式：
    python miner_monitor.py --config miners.txt --interval 300
"""

import asyncio
import json
import argparse
from datetime import datetime
from tabulate import tabulate
from rustchain_sdk import (
    RustChainClient,
    RustChainError,
    ConnectionError,
)

# ─── 辅助函数 ────────────────────────────────────────────────

def load_addresses(filepath: str) -> list[str]:
    """从文件加载矿工地址列表（每行一个，以 # 开头为注释）"""
    addresses = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                addresses.append(line)
    return addresses


async def fetch_balance(client: RustChainClient, address: str) -> dict:
    """查询单个地址余额，带超时保护"""
    try:
        info = await client.get_balance(address)
        return {
            "address": address,
            "balance": float(info.get("balance", 0)),
            "status": "ok",
        }
    except RustChainError as e:
        return {
            "address": address,
            "balance": None,
            "status": f"error: {e.message}",
        }


async def monitor_miners(addresses: list[str], interval: int = 300):
    """
    主监控循环
    - 每隔 interval 秒刷新一次所有矿工余额
    - 检测余额变化并打印告警
    """
    print(f"[{datetime.now():%H:%M:%S}] 启动矿工余额监控，共 {len(addresses)} 个地址")
    print("按 Ctrl+C 退出\n")

    prev_balances = {}  # 上次记录的余额，用于检测变动

    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*60}")
        print(f"⏰ {timestamp}  — 刷新中...")

        async with RustChainClient() as client:
            # 并发查询所有地址（提升性能）
            tasks = [fetch_balance(client, addr) for addr in addresses]
            results = await asyncio.gather(*tasks)

        # 构建表格数据
        table_data = []
        alerts = []

        for result in results:
            addr = result["address"]
            balance = result["balance"]
            status = result["status"]

            prev = prev_balances.get(addr)
            change = None
            if prev is not None and balance is not None:
                change = balance - prev
                if abs(change) > 0.1:  # 余额变动超过 0.1 RTC 则告警
                    direction = "⬆️" if change > 0 else "⬇️"
                    alerts.append(
                        f"{direction} {addr[:12]}... "
                        f"变动: {change:+.4f} RTC "
                        f"({prev:.4f} -> {balance:.4f})"
                    )

            row_status = "✅" if status == "ok" else f"❌ {status}"
            table_data.append([
                addr[:16] + "...",
                f"{balance:.4f}" if balance is not None else "N/A",
                f"{change:+.4f}" if change else "—",
                row_status,
            ])

            # 记录当前余额
            if balance is not None:
                prev_balances[addr] = balance

        # 打印告警
        for alert in alerts:
            print(f"  🚨 {alert}")

        # 打印表格
        print("\n矿工余额概览：")
        print(tabulate(
            table_data,
            headers=["地址", "余额 (RTC)", "变动", "状态"],
            tablefmt="grid",
        ))

        # 等待下次刷新
        await asyncio.sleep(interval)


# ─── 程序入口 ────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="RustChain 矿工余额监控")
    parser.add_argument(
        "--config",
        default="miners.txt",
        help="矿工地址列表文件（每行一个 RTC 地址）",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="刷新间隔（秒），默认 300 秒（5 分钟）",
    )
    args = parser.parse_args()

    addresses = load_addresses(args.config)
    if not addresses:
        print("❌ 未找到有效地址，请检查配置文件")
        return

    try:
        asyncio.run(monitor_miners(addresses, args.interval))
    except KeyboardInterrupt:
        print("\n\n监控已停止。")


if __name__ == "__main__":
    main()
```

**`miners.txt` 示例**

```
# RustChain 矿工地址列表
# 格式：每行一个 RTC 地址
RTC1a2b3c4d5e6f789012345678901234567890abcd
RTC9x8y7z6w5v4u3t2s1r0q9p8o7n6m5l4k3j2i1h
# RTC0000000000000000000000000000000000000000  # 已弃用地址
```

**运行效果**

```
================================================================
⏰ 2026-03-17 10:05:00  — 刷新中...
  🚨 ⬇️ RTC1a2b3c4d5e... 变动: -5.2340 RTC (12.3450 -> 7.1110)

矿工余额概览：
+------------------+-----------+-----------+--------+
| 地址             | 余额 (RTC) | 变动      | 状态   |
+==================+===========+===========+========+
| RTC1a2b3c4d5e... | 7.1110    | -5.2340   | ✅     |
+------------------+-----------+-----------+--------+
| RTC9x8y7z6w5v... | 0.5000    | —         | ✅     |
+------------------+-----------+-----------+--------+
```

---

## 附录：SDK 核心类速查

### RustChainClient

| 方法 | 返回类型 | 说明 |
|------|----------|------|
| `health()` | `Dict` | 节点健康状态 |
| `get_epoch()` | `Dict` | 当前 Epoch 信息 |
| `get_headers_tip()` | `Dict` | 链头区块信息 |
| `get_miners()` | `List[Dict]` | 活跃矿工列表 |
| `get_balance(address)` | `Dict` | 钱包余额 |
| `get_wallet_history(address, limit)` | `Dict` | 交易历史 |
| `get_attestation_status(miner_pk)` | `Dict` | 硬件证明状态 |
| `attest_challenge(miner_pk)` | `Dict` | 获取证明挑战 |
| `attest_submit(...)` | `Dict` | 提交证明 |
| `get_bounty_multiplier()` | `Dict` | 奖励倍数信息 |
| `wallet_transfer_with_wallet(...)` | `Dict` | 签名并发送转账 |
| `transfer_signed(...)` | `Dict` | 发送已签名交易 |
| `beacon_submit(envelope)` | `Dict` | 提交信标信封 |
| `governance_propose(...)` | `Dict` | 提交治理提案 |
| `governance_vote(...)` | `Dict` | 投票 |
| `list_governance_proposals(status)` | `List[Dict]` | 提案列表 |
| `explorer_blocks(limit)` | `List[Dict]` | 最新区块 |
| `explorer_transactions(address, limit)` | `List[Dict]` | 交易列表 |
| `get_epoch_rewards(epoch_number)` | `Dict` | Epoch 奖励分配 |

### RustChainWallet

| 属性/方法 | 返回类型 | 说明 |
|-----------|----------|------|
| `address` | `str` | RTC 地址 |
| `public_key_hex` | `str` | 公钥（十六进制） |
| `seed_phrase` | `List[str]` | BIP39 助记词 |
| `private_key_hex` | `str` | 私钥（十六进制） |
| `create(strength=128)` | `Wallet` | 创建新钱包 |
| `from_seed_phrase(words)` | `Wallet` | 从助记词恢复 |
| `sign(message)` | `bytes` | Ed25519 签名 |
| `sign_transfer(to, amount, fee)` | `Dict` | 签名转账 |
| `export()` | `Dict` | 导出钱包数据 |
| `import_(data)` | `Wallet` | 导入钱包 |

---

*文档基于 RustChain SDK v1.0.0 编写。当前节点版本：2.2.1-rip200（RustChain v2 主网）*  
*如有问题，欢迎在 [rustchain-bounties](https://github.com/Scottcjn/rustchain-bounties) 提交 Issue。*
