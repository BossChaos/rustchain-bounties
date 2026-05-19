# RustChain 钱包用户指南

> **RIP-201** — RustChain 钱包的完整使用指南。

---

## 目录

1. [钱包类型](#1-钱包类型)
2. [创建钱包](#2-创建钱包)
3. [接收 RTC](#3-接收-rtc)
4. [发送 RTC](#4-发送-rtc)
5. [查看交易历史](#5-查看交易历史)
6. [钱包备份与恢复](#6-钱包备份与恢复)
7. [安全最佳实践](#7-安全最佳实践)
8. [常见问题](#8-常见问题)

---

## 1. 钱包类型

### 1.1 CLI 钱包 (命令行)

- 适合高级用户
- 完整功能
- 脚本友好

### 1.2 Python SDK 钱包

- 开发者使用
- 可编程控制
- 集成到 DApp

### 1.3 Web 钱包 (计划中)

- 浏览器界面
- 易于使用
- 即将推出

---

## 2. 创建钱包

### 2.1 使用 Python SDK 创建

```python
from rustchain_sdk import Wallet

# 创建新钱包
wallet = Wallet.create()

print(f"地址: {wallet.address}")
print(f"助记词: {wallet.mnemonic}")
```

### 2.2 从助记词恢复

```python
# 从 12 词助记词恢复
wallet = Wallet.from_mnemonic("word1 word2 word3 ... word12")

# 从私钥恢复
wallet = Wallet.from_private_key("0xprivatekey123...")
```

### 2.3 使用 CLI 工具

```bash
# 创建钱包
python3 tools/wallet.py create

# 查看地址
python3 tools/wallet.py address

# 导出私钥（谨慎使用！）
python3 tools/wallet.py export-private-key
```

---

## 3. 接收 RTC

### 3.1 获取收款地址

```python
from rustchain_sdk import Wallet

wallet = Wallet.from_mnemonic("your twelve words here...")
print(f"收款地址: {wallet.address}")
```

### 3.2 查询余额

```python
from rustchain_sdk import RustChainClient

client = RustChainClient()
balance = client.get_balance(wallet.address)
print(f"余额: {balance['balance']} RTC")
```

或使用 curl：

```bash
curl "https://rustchain.org/wallet/balance?address=YOUR_ADDRESS"
```

### 3.3 查看交易

```python
txs = client.get_transactions(wallet.address, limit=10)
for tx in txs['transactions']:
    print(f"哈希: {tx['hash'][:16]}...")
    print(f"  金额: {tx['value']} RTC")
    print(f"  时间: {tx['timestamp']}")
```

---

## 4. 发送 RTC

### 4.1 使用 SDK 发送

```python
from rustchain_sdk import Wallet, RustChainClient

# 加载钱包
sender = Wallet.from_mnemonic("your twelve words...")

# 创建客户端
client = RustChainClient()

# 发送交易
tx = client.send_transaction(
    from_wallet=sender,
    to_address="0xRecipientAddress...",
    amount="1.5",  # RTC
    gas_limit=21000,
    gas_price="1000000000"  # 1 gwei
)

print(f"交易哈希: {tx['hash']}")
print(f"状态: {tx['status']}")
```

### 4.2 交易确认

```python
# 等待交易确认
receipt = client.wait_for_transaction(tx['hash'], timeout=60)
print(f"确认区块: {receipt['block_number']}")
print(f"Gas 使用量: {receipt['gas_used']}")
```

---

## 5. 查看交易历史

### 5.1 查询交易列表

```python
from rustchain_sdk import RustChainClient

client = RustChainClient()
txs = client.get_transactions("0xYourAddress...", limit=20, offset=0)

for tx in txs['transactions']:
    direction = "发送" if tx['from'] == "0xYourAddress..." else "接收"
    print(f"{direction} {tx['value']} RTC")
    print(f"  哈希: {tx['hash']}")
    print(f"  时间戳: {tx['timestamp']}")
```

### 5.2 过滤交易

```python
# 只查看发送的交易
sent = [tx for tx in txs['transactions'] if tx['from'] == wallet.address]

# 只查看接收的交易
received = [tx for tx in txs['transactions'] if tx['to'] == wallet.address]

# 计算总额
total_sent = sum(float(tx['value']) for tx in sent)
total_received = sum(float(tx['value']) for tx in received)

print(f"总发送: {total_sent} RTC")
print(f"总接收: {total_received} RTC")
```

---

## 6. 钱包备份与恢复

### 6.1 备份助记词

```python
# 导出助记词（安全存储！）
wallet = Wallet.create()
mnemonic = wallet.mnemonic

# 保存到加密文件
import json
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)
encrypted = f.encrypt(mnemonic.encode())

with open('wallet_backup.enc', 'wb') as f:
    f.write(encrypted)

# 保存密钥（离线存储！）
with open('wallet_key.key', 'wb') as f:
    f.write(key)
```

### 6.2 从备份恢复

```python
from cryptography.fernet import Fernet

# 读取密钥
with open('wallet_key.key', 'rb') as f:
    key = f.read()

# 解密助记词
f = Fernet(key)
with open('wallet_backup.enc', 'rb') as f:
    encrypted = f.read()

mnemonic = f.decrypt(encrypted).decode()

# 恢复钱包
wallet = Wallet.from_mnemonic(mnemonic)
print(f"钱包地址: {wallet.address}")
```

---

## 7. 安全最佳实践

### 7.1 永远不要

- ❌ 将助记词或私钥提交到代码仓库
- ❌ 在公共网络传输私钥
- ❌ 使用弱密码保护钱包文件
- ❌ 在不受信任的设备上操作钱包

### 7.2 始终要

- ✅ 离线备份助记词
- ✅ 使用强密码
- ✅ 定期检查余额和交易
- ✅ 使用环境变量存储敏感信息

### 7.3 安全存储示例

```python
import os

# 从环境变量读取私钥
private_key = os.environ.get('RUSTCHAIN_PRIVATE_KEY')
if not private_key:
    raise ValueError("RUSTCHAIN_PRIVATE_KEY not set")

wallet = Wallet.from_private_key(private_key)
```

---

## 8. 常见问题

### Q: 丢失助记词怎么办？

**A**: 如果丢失助记词且没有备份，钱包中的资产将永久无法恢复。务必在创建钱包后立即备份助记词。

### Q: 可以一个钱包多设备使用吗？

**A**: 可以。只要导入相同的助记词或私钥，即可在多个设备上访问同一钱包。

### Q: 如何更改钱包地址？

**A**: 钱包地址由私钥决定，无法更改。如果需要新地址，创建新钱包即可。

### Q: 交易卡在待处理状态怎么办？

**A**: 检查 Gas 价格是否足够。如果太低，交易可能需要很长时间才能被确认。

```python
# 检查当前 Gas 价格
gas_price = client.get_gas_price()
print(f"当前 Gas 价格: {gas_price} wei")
```

---

*文档版本: 1.0 | 最后更新: 2026-05-19*
