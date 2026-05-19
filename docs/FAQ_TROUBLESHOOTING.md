# RustChain FAQ & Troubleshooting Guide
## RustChain 常见问题与故障排除指南

> **文档版本:** v1.0  
> **适用版本:** RustChain v2.2.1-rip200 及以上  
> **最后更新:** 2026年3月  
> **主节点:** https://50.28.86.131

---

## 目录

1. [安装问题](#1-安装问题)
2. [节点连接问题](#2-节点连接问题)
3. [钱包问题](#3-钱包问题)
4. [挖矿问题](#4-挖矿问题)
5. [SDK 连接与编程问题](#5-sdk-连接与编程问题)
6. [网络与安全相关问题](#6-网络与安全相关问题)
7. [错误代码速查表](#7-错误代码速查表)
8. [常用诊断命令](#8-常用诊断命令)

---

## 1. 安装问题

### 1.1 Python 环境问题

#### 问题：运行 miner 脚本提示 `Python version 3.8+ required`

**原因：** 当前系统 Python 版本过低。

**解决方案：**

```bash
# 检查当前 Python 版本
python3 --version

# Ubuntu/Debian 升级 Python
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.11
python3.11 --version

# macOS 使用 Homebrew
brew install python@3.11

# 使用指定版本运行脚本
python3.11 rustchain_linux_miner.py --wallet YOUR_MINER_ID
```

#### 问题：安装依赖时提示 `pip: command not found`

**解决方案：**

```bash
# Debian/Ubuntu
sudo apt install python3-pip

# macOS
brew install pip

# 验证 pip 安装
python3 -m pip --version
```

#### 问题：运行脚本时提示 `ModuleNotFoundError: No module named 'requests'`

**解决方案：**

```bash
# 安装 requests 库
python3 -m pip install requests

# 或一次性安装所有常见依赖
python3 -m pip install requests cryptography ecdsa
```

---

### 1.2 操作系统兼容性问题

#### 问题：macOS 运行 miner 脚本报错 `Permission denied`

**原因：** macOS 安全机制阻止了未签名脚本的执行。

**解决方案：**

```bash
# 方法一：临时允许（macOS 偏好设置 > 安全性与隐私）
# 方法二：使用 Python 直接运行
python3 miners/macos/rustchain_mac_miner_v2.4.py --wallet YOUR_MINER_ID

# 方法三：添加执行权限
chmod +x rustchain_mac_miner_v2.4.py
```

#### 问题：Windows 用户无法运行 miner 脚本

**解决方案：**

```powershell
# 确保安装 Python 3.8+
python --version

# 安装依赖
python -m pip install requests

# 从 repo 目录运行
cd Rustchain
python miners\windows\rustchain_windows_miner.py

# 或使用命令行参数
python miners\windows\rustchain_windows_miner.py --wallet YOUR_MINER_ID
```

---

### 1.3 下载与克隆问题

#### 问题：克隆仓库提示 `Permission denied (publickey)` 或 `SSL certificate problem`

**原因：** 未配置 Git SSH 密钥或 SSL 证书问题。

**解决方案：**

```bash
# 使用 HTTPS 方式克隆（推荐）
git clone https://github.com/Scottcjn/Rustchain.git
cd Rustchain

# 如遇 SSL 错误，临时跳过证书验证
GIT_SSL_NO_VERIFY=true git clone https://github.com/Scottcjn/Rustchain.git

# 修复 SSL 后重新配置
git config --global http.sslVerify true
```

#### 问题：curl 下载脚本失败 `Failed to connect`

**解决方案：**

```bash
# 检查网络连通性
ping github.com

# 使用 -L 参数跟随重定向
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/miners/linux/rustchain_linux_miner.py -o rustchain_linux_miner.py

# 检查文件是否下载完整
ls -la rustchain_linux_miner.py
file rustchain_linux_miner.py
```

---

## 2. 节点连接问题

### 2.1 节点健康检查失败

#### 问题：`curl` 请求节点 `/health` 返回非 200 或 `ok: false`

**诊断步骤：**

```bash
# 第一步：检查节点是否可达
curl -sk https://50.28.86.131/health

# 期望输出：
# {"ok": true, "version": "2.2.1-rip200", "uptime_s": ..., "db_rw": true, "tip_age_slots": 0}

# 第二步：检查节点版本
curl -sk https://50.28.86.131/health | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"

# 第三步：对比预期版本
# 预期版本应为：2.2.1-rip200
```

**常见原因及解决方案：**

| 原因 | 症状 | 解决方案 |
|------|------|----------|
| 节点宕机 | 连接超时 | 等待恢复或更换备用节点 |
| 版本过旧 | `version` 低于 `2.2.1-rip200` | 升级节点软件到最新版本 |
| SSL 证书问题 | `SSL_ERROR_SYSCALL` | 使用 `-k` 参数跳过证书验证 |
| 网络隔离 | `db_rw: false` | 检查防火墙，确保 `8099/tcp` 开放 |

---

### 2.2 自签名证书错误

#### 问题：请求时报错 `SSL: CERTIFICATE_VERIFY_FAILED`

**原因：** RustChain 节点使用自签名 SSL 证书，常见 HTTP 客户端默认不信任。

**解决方案：**

```bash
# curl：使用 -k 参数
curl -sk https://50.28.86.131/health

# Python requests：
import requests
response = requests.get('https://50.28.86.131/health', verify=False)

# Python requests（自定义证书路径）：
response = requests.get('https://50.28.86.131/health', verify='/path/to/ca-cert.pem')

# 长期解决方案：导入自签名证书到系统信任存储
sudo cp rustchain.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

---

### 2.3 连接超时问题

#### 问题：`HTTPSConnectionPool(host='50.28.86.131', port=443): Max retries exceeded` 或 `Connection timed out`

**排查步骤：**

```bash
# 1. 测试基本连通性
ping 50.28.86.131

# 2. 测试端口可达性
nc -zv 50.28.86.131 443
nc -zv 50.28.86.131 8099

# 3. 测试 HTTP 端点
curl -sk --connect-timeout 10 https://50.28.86.131/health
```

**解决方案：**

```python
# Python SDK 增加超时配置
import requests

response = requests.get(
    'https://50.28.86.131/health',
    timeout=(5, 30),  # (连接超时, 读取超时)
    verify=False
)

# 重试机制
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))
```

---

### 2.4 API 端点返回 404

#### 问题：API 调用返回 `404 Not Found`

**原因：** 端点路径错误或节点版本过旧。

**解决方案：**

```bash
# 确认端点路径正确
curl -sk https://50.28.86.131/api/stats
curl -sk https://50.28.86.131/epoch
curl -sk https://50.28.86.131/api/miners

# 检查节点版本（v2 API 需要 v2.2+）
curl -sk https://50.28.86.131/health | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"
```

---

## 3. 钱包问题

### 3.1 钱包余额查询问题

#### 问题：查询余额返回 `0` 或 `{"balance": 0}`

**可能原因：**
1. miner_id/wallet 名称拼写错误
2. 钱包确实没有余额
3. 该钱包从未参与过挖矿

**诊断与解决方案：**

```bash
# 方法一：通过 API 查询（使用 miner public key）
curl -sk "https://50.28.86.131/balance/0x0000000000000000000000000000000000000000000000000000000000000001"

# 方法二：通过 wallet 名称查询
curl -sk "https://50.28.86.131/wallet/balance?miner_id=YOUR_MINER_ID"

# 方法三：检查所有 miner 数据
curl -sk https://50.28.86.131/api/miners > miners.json
python3 -c "
import json
with open('miners.json') as f:
    miners = json.load(f)
# 搜索特定 miner
target = 'YOUR_MINER_ID'
found = [m for m in miners if m.get('miner') == target or m.get('miner_pk', '').lower() == target.lower()]
print(found)
"
```

---

### 3.2 钱包创建与导入

#### 问题：创建新钱包后无法收到挖矿奖励

**原因：** 新钱包需要先在节点注册并参与挖矿。

**解决方案：**

```bash
# 1. 确保新钱包已在节点注册
curl -sk https://50.28.86.131/api/miners | python3 -c "
import json, sys
miners = json.load(sys.stdin)
for m in miners:
    if 'YOUR_WALLET_NAME' in str(m):
        print(json.dumps(m, indent=2))
"

# 2. 检查钱包的设备家族和 antiquity_multiplier
# 新设备通常没有历史记录，multiplier 可能为 1.0x

# 3. 参与当前 epoch
curl -sk -X POST https://50.28.86.131/epoch/enroll \
  -H "Content-Type: application/json" \
  -d '{"miner_pk": "YOUR_PUBLIC_KEY"}'
```

#### 问题：导入钱包后显示余额不一致

**原因：** 导入了错误的公钥地址或使用了不同的链 ID。

**解决方案：**

```bash
# 1. 确认导入的公钥与原链一致
curl -sk "https://50.28.86.131/api/stats" | python3 -c "
import json, sys
stats = json.load(sys.stdin)
print('chain_id:', stats['chain_id'])
"

# 2. 对比原始链 ID
# 主网 chain_id 应为：rustchain-mainnet-v2

# 3. 如使用 SDK：
from rustchain_sdk import Wallet
wallet = Wallet.import_key('your_private_key_or_seed')
print('chain_id:', wallet.chain_id)
print('public_key:', wallet.public_key)
```

---

### 3.3 提现问题

#### 问题：发起提现请求后状态一直是 `pending`

**诊断：**

```bash
# 检查提现历史
curl -sk "https://50.28.86.131/withdraw/history/YOUR_MINER_PK"

# 查询具体提现 ID 状态
curl -sk "https://50.28.86.131/withdraw/status/WITHDRAWAL_ID"
```

**常见原因：**

| 状态 | 含义 | 解决方案 |
|------|------|----------|
| `pending` | 等待处理 | 等待区块确认，通常 1-3 分钟 |
| `processing` | 处理中 | 区块链确认中，继续等待 |
| `completed` | 完成 | 检查目标钱包 |
| `failed` | 失败 | 检查失败原因，重新发起 |
| `rejected` | 拒绝 | 检查签名是否正确，余额是否充足 |

**解决方案：**

```bash
# 重新发起提现（确保签名正确）
curl -sk -X POST https://50.28.86.131/withdraw/request \
  -H "Content-Type: application/json" \
  -d '{
    "miner_pk": "YOUR_MINER_PK",
    "amount": 100,
    "signature": "YOUR_SIGNATURE"
  }'
```

#### 问题：提现签名验证失败

**原因：** 签名使用的密钥与注册时不一致。

**解决方案：**

```bash
# 1. 检查已注册的提现密钥
# 查看 withdraw/register 文档确认密钥格式

# 2. 使用正确的 SR25519 密钥签名
# 确保使用与注册时相同的 withdrawal_pk 对应的私钥签名

# 3. 重新注册提现密钥
curl -sk -X POST https://50.28.86.131/withdraw/register \
  -H "Content-Type: application/json" \
  -d '{
    "miner_pk": "YOUR_MINER_PK",
    "withdrawal_pk": "YOUR_SR25519_PUBLIC_KEY"
  }'
```

---

## 4. 挖矿问题

### 4.1 Miner 不出现在矿工列表中

#### 问题：运行 miner 后，在 `/api/miners` 中找不到自己的 miner

**诊断步骤：**

```bash
# 步骤 1：下载完整矿工列表
curl -sk https://50.28.86.131/api/miners > miners.json

# 步骤 2：搜索你的 miner
python3 -c "
import json
with open('miners.json') as f:
    miners = json.load(f)
print(f'总矿工数: {len(miners)}')
target = 'YOUR_MINER_ID'
for m in miners:
    if target.lower() in str(m.get('miner', '')).lower():
        print(json.dumps(m, indent=2))
"

# 步骤 3：检查矿工最后 attestation 时间
# 如果 last_attest 为空或很久以前，说明 attestation 失败
```

**常见原因及解决方案：**

| 原因 | 表现 | 解决方案 |
|------|------|----------|
| VM 环境运行 | 可能被识别为非真实硬件 | 在真实硬件上运行 |
| attestation 失败 | last_attest 为空 | 检查硬件证明生成流程 |
| 节点版本不匹配 | miner 注册后消失 | 升级到 `2.2.1-rip200` |
| 网络不稳定 | miner 间歇性消失 | 改善网络连接 |
| miner_id 拼写错误 | 搜索不到 | 仔细核对 miner_id |

---

### 4.2 硬件证明（Attestation）失败

#### 问题：挖矿脚本日志显示 `attestation failed` 或 `hardware_proof` 验证失败

**原因：** RIP-200 Proof of Attestation 需要在真实硬件上运行，虚拟机或容器环境可能无法通过。

**诊断与解决：**

```bash
# 1. 确认在真实硬件上运行（非 VM）
# VM 环境会有较低的 antiquity_multiplier 或被拒绝

# 2. 手动测试 attestation 流程
# 步骤 1：获取 challenge
curl -sk -X POST https://50.28.86.131/attest/challenge \
  -H "Content-Type: application/json" \
  -d '{"miner_pk": "YOUR_MINER_PK"}'

# 步骤 2：生成硬件证明（本地）
# miner 脚本应自动完成此步骤

# 步骤 3：提交 attestation
curl -sk -X POST https://50.28.86.131/attest/submit \
  -H "Content-Type: application/json" \
  -d '{
    "miner_pk": "YOUR_MINER_PK",
    "challenge": "CHALLENGE_STRING",
    "response": "RESPONSE_STRING",
    "hardware_proof": {}
  }'
```

**硬件乘数参考（当前默认值）：**

| 设备类型 | 乘数 | 说明 |
|----------|------|------|
| PowerPC G4 | 2.5x | 最高奖励，面向古董硬件 |
| PowerPC G5 | 2.0x | 经典 PowerPC 架构 |
| POWER8 | 1.5x | IBM Power 架构服务器 |
| Apple Silicon | 1.2x | M1/M2/M3 芯片 |
| Modern x86 | 1.0x | 标准现代 CPU |

---

### 4.3 挖矿脚本运行中断

#### 问题：miner 脚本运行一段时间后自动停止

**解决方案：**

```bash
# 方法一：使用 nohup 后台运行
nohup python3 rustchain_linux_miner.py --wallet YOUR_MINER_ID > miner.log 2>&1 &

# 方法二：使用 systemd 服务（推荐，崩溃自动重启）
sudo tee /etc/systemd/system/rustchain-miner.service >/dev/null <<'EOF'
[Unit]
Description=RustChain Miner
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/Rustchain
ExecStart=/usr/bin/python3 /home/YOUR_USERNAME/Rustchain/miners/linux/rustchain_linux_miner.py --wallet YOUR_MINER_ID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now rustchain-miner.service
sudo systemctl status rustchain-miner.service

# 方法三：使用 tmux/screen
tmux new -s rustchain-miner
python3 rustchain_linux_miner.py --wallet YOUR_MINER_ID
# 按 Ctrl+B 然后按 D 分离会话
# 重新连接：tmux attach -t rustchain-miner
```

---

### 4.4 Epoch 相关问题

#### 问题：未注册到当前 epoch，无法获得奖励

**诊断：**

```bash
# 检查当前 epoch 信息
curl -sk https://50.28.86.131/epoch

# 期望输出：
# {"epoch": 104, "slot": 15066, "blocks_per_epoch": 144, "enrolled_miners": 30, "epoch_pot": 1.5}

# 检查是否已注册
curl -sk https://50.28.86.131/api/miners | python3 -c "
import json, sys
miners = json.load(sys.stdin)
target = 'YOUR_MINER_ID'
for m in miners:
    if target in str(m.get('miner', '')):
        enrolled = m.get('enrolled_in_current_epoch', False)
        print(f'已注册: {enrolled}')
"
```

**解决方案：**

```bash
# 注册到当前 epoch
curl -sk -X POST https://50.28.86.131/epoch/enroll \
  -H "Content-Type: application/json" \
  -d '{"miner_pk": "YOUR_MINER_PK"}'

# 注意：每个 epoch 开始时需要重新注册
# 关注 epoch 时间：每个 epoch 有 144 个区块，区块时间 600 秒
# 即每个 epoch 约 24 小时
```

---

## 5. SDK 连接与编程问题

### 5.1 SDK 异常类型

RustChain Python SDK 定义了以下异常类型，位于 `rustchain_sdk.exceptions`：

| 异常类 | 说明 | 触发场景 |
|--------|------|----------|
| `RustChainError` | 所有 SDK 异常的基类 | 通用错误 |
| `ConnectionError` | 节点连接失败 | 网络问题、节点宕机 |
| `APIError` | API 请求返回非 2xx | 400/401/403/404/429/500 |
| `AuthenticationError` | 认证失败 | 签名验证失败、无权限 |
| `ValidationError` | 输入验证失败 | 地址格式错误、金额非法 |
| `WalletError` | 钱包操作失败 | 创建/签名/导入错误 |
| `AttestationError` | 认证证明失败 | 硬件证明验证不通过 |
| `GovernanceError` | 治理操作失败 | 提案/投票错误 |
| `HealthError` | 节点健康检查失败 | `/health` 返回 `ok: false` |
| `EpochError` | Epoch 操作失败 | 注册/状态查询失败 |
| `TransferError` | 转账失败 | 余额不足、签名错误 |
| `RPCError` | RPC 调用失败 | 通用 RPC 错误 |

### 5.2 处理 SDK 异常

**推荐模式：**

```python
from rustchain_sdk import RustChainClient
from rustchain_sdk.exceptions import (
    RustChainError,
    ConnectionError,
    APIError,
    ValidationError,
    HealthError,
)

node_url = 'https://50.28.86.131'
client = RustChainClient(node_url)

try:
    # 检查节点健康
    health = client.health()
    if not health.get('ok'):
        raise HealthError(f"Node unhealthy: {health}")
    
    # 获取余额
    balance = client.get_balance('YOUR_MINER_PK')
    print(f"Balance: {balance}")
    
except ConnectionError as e:
    print(f"无法连接到节点: {e.message}")
    print(f"详情: {e.details}")
    # 解决方案：检查网络、节点是否在线
except APIError as e:
    print(f"API 请求失败: {e.message}")
    print(f"HTTP 状态码: {e.status_code}")
    print(f"响应内容: {e.response_body}")
    # 解决方案：根据状态码处理
except ValidationError as e:
    print(f"输入验证失败: {e.message}")
    # 解决方案：检查输入参数格式
except HealthError as e:
    print(f"节点健康检查失败: {e.message}")
    # 解决方案：等待节点恢复
except RustChainError as e:
    print(f"RustChain SDK 错误: {e.message}")
    print(f"详细信息: {e.details}")
except Exception as e:
    print(f"未知错误: {e}")
finally:
    client.close()
```

### 5.3 SDK 连接池与重试

**最佳实践：**

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from rustchain_sdk.exceptions import ConnectionError, APIError

def create_session():
    """创建带重试机制的会话"""
    session = requests.Session()
    
    # 配置重试策略
    retries = Retry(
        total=5,
        backoff_factor=2,  # 指数退避：2s, 4s, 8s, 16s, 32s
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "POST"],
        raise_on_status=False
    )
    
    adapter = HTTPAdapter(
        max_retries=retries,
        pool_connections=10,
        pool_maxsize=20
    )
    
    session.mount('https://', adapter)
    session.verify = False  # 自签名证书
    
    return session

# 使用
session = create_session()
try:
    response = session.get('https://50.28.86.131/health', timeout=30)
except requests.exceptions.RequestException as e:
    raise ConnectionError(f"请求失败: {e}")
```

---

## 6. 网络与安全相关问题

### 6.1 防火墙配置

#### 问题：本地miner无法连接到节点，提示 `Connection refused`

**原因：** 防火墙阻止了出站或入站连接。

**解决方案：**

```bash
# 检查防火墙状态
sudo ufw status

# 开放必要端口（节点主机端）
sudo ufw allow 8099/tcp
sudo ufw allow 443/tcp

# 客户端（miner）通常只需开放出站 HTTPS (443)
sudo iptables -L -n | grep 443

# 如果使用云服务器，检查安全组规则
# AWS: 检查 EC2 安全组入站规则
# 阿里云: 检查安全组入站规则
```

### 6.2 速率限制（Rate Limiting）

#### 问题：频繁请求 API 返回 429 Too Many Requests

**原因：** 节点对单个 IP 的请求频率有限制。

**解决方案：**

```python
import time
from functools import wraps

def rate_limit(calls=10, period=1):
    """简单速率限制装饰器"""
    def decorator(func):
        calls_history = []
        def wrapper(*args, **kwargs):
            now = time.time()
            # 清理过期记录
            calls_history[:] = [t for t in calls_history if now - t < period]
            
            if len(calls_history) >= calls:
                sleep_time = period - (now - calls_history[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)
            
            calls_history.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 使用示例
@rate_limit(calls=5, period=1)  # 每秒最多 5 次
def safe_get_balance(miner_pk):
    return client.get_balance(miner_pk)
```

**通用建议：**
- 健康检查：每 30-60 秒一次
- 余额查询：每 5-10 分钟一次
- 批量操作：使用队列和延迟

### 6.3 版本不匹配问题

#### 问题：miner 或 SDK 与节点版本不兼容

**诊断：**

```bash
# 检查网络预期版本
curl -sk https://50.28.86.131/health | python3 -c "
import sys, json
h = json.load(sys.stdin)
print(f\"网络版本: {h['version']}\")
print(f\"最低兼容版本: 2.2.1-rip200\")
"

# 检查 SDK 版本
python3 -c "from rustchain_sdk import __version__; print(__version__)"

# 检查 miner 脚本版本（查看文件头部）
head -20 rustchain_linux_miner.py
```

**解决方案：**

```bash
# 升级 RustChain repo
cd Rustchain
git pull origin main

# 重新下载 miner 脚本
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/miners/linux/rustchain_linux_miner.py -o rustchain_linux_miner.py

# 升级 SDK
pip install --upgrade rustchain-sdk
```

### 6.4 SSL/HTTPS 问题

#### 问题：本地网络环境无法访问节点

**备选方案：**

```bash
# 方法一：使用 HTTP（仅测试环境）
# 将 https:// 改为 http://

# 方法二：通过代理访问
export HTTPS_PROXY=http://proxy.example.com:8080
curl -sk https://50.28.86.131/health

# 方法三：使用 Websocket（如果支持）
# 参考 API 文档中的 Websocket 端点

# 方法四：联系节点管理员确认网络白名单
```

---

## 7. 错误代码速查表

### HTTP 状态码

| 状态码 | 含义 | 常见原因 | 解决方案 |
|--------|------|----------|----------|
| **200** | 成功 | 正常 | 无需处理 |
| **400** | 错误请求 | 参数格式错误、缺少必需字段 | 检查请求体格式 |
| **401** | 未认证 | 签名无效、密钥不匹配 | 重新签名或检查密钥 |
| **403** | 禁止访问 | 权限不足、操作被拒绝 | 检查账户权限 |
| **404** | 未找到 | 端点不存在、资源不存在 | 确认 API 路径和资源 ID |
| **429** | 请求过于频繁 | 超过速率限制 | 降低请求频率，等待后重试 |
| **500** | 服务器内部错误 | 节点软件问题 | 等待恢复或报告问题 |
| **502** | 网关错误 | 节点过载或维护中 | 稍后重试 |
| **503** | 服务不可用 | 节点暂时不可用 | 等待服务恢复 |
| **504** | 网关超时 | 节点响应过慢 | 增加超时时间或检查节点状态 |

### SDK 错误码

| 错误码 | 异常类 | 说明 | 排查方向 |
|--------|--------|------|----------|
| `RC001` | ConnectionError | 节点连接失败 | 检查网络、防火墙、节点状态 |
| `RC002` | APIError | API 请求失败 | 检查状态码和响应内容 |
| `RC003` | AuthenticationError | 认证失败 | 检查签名和密钥 |
| `RC004` | ValidationError | 参数验证失败 | 检查输入格式和范围 |
| `RC005` | WalletError | 钱包操作失败 | 检查钱包状态和余额 |
| `RC006` | AttestationError | 认证失败 | 检查硬件环境和证明生成 |
| `RC007` | GovernanceError | 治理操作失败 | 检查投票权和提案状态 |
| `RC008` | HealthError | 健康检查失败 | 节点可能需要维护 |
| `RC009` | EpochError | Epoch 操作失败 | 检查注册状态和时间窗口 |
| `RC010` | TransferError | 转账失败 | 检查余额和目标地址 |
| `RC011` | RPCError | RPC 调用失败 | 检查方法和参数 |

### Miner 状态码

| 状态 | 含义 | 说明 |
|------|------|------|
| `active` | 活跃 | miner 正常工作 |
| `inactive` | 非活跃 | 长时间无 attestation |
| `pending` | 待处理 | 等待下一 epoch 开始 |
| `banned` | 被禁止 | 违反规则，暂时禁止挖矿 |
| `upgrading` | 升级中 | 节点正在升级 |

---

## 8. 常用诊断命令

### 8.1 一键诊断脚本

```bash
#!/bin/bash
# rustchain_diag.sh - RustChain 诊断脚本

NODE_URL="https://50.28.86.131"
MINER_ID="${1:-}"

echo "=========================================="
echo "RustChain 诊断工具"
echo "=========================================="
echo ""

# 1. 节点健康检查
echo "[1/6] 检查节点健康状态..."
HEALTH=$(curl -sk --max-time 10 "$NODE_URL/health")
if [ $? -eq 0 ]; then
    OK=$(echo $HEALTH | python3 -c "import sys,json; print(json.load(sys.stdin).get('ok', False))")
    VERSION=$(echo $HEALTH | python3 -c "import sys,json; print(json.load(sys.stdin).get('version', 'N/A'))")
    echo "  ✓ 节点可达 | 版本: $VERSION | OK: $OK"
else
    echo "  ✗ 节点不可达"
fi

# 2. Epoch 信息
echo "[2/6] 获取 Epoch 信息..."
EPOCH=$(curl -sk --max-time 10 "$NODE_URL/epoch")
if [ $? -eq 0 ]; then
    EPOCH_NUM=$(echo $EPOCH | python3 -c "import sys,json; print(json.load(sys.stdin).get('epoch', 'N/A'))")
    ENROLLED=$(echo $EPOCH | python3 -c "import sys,json; print(json.load(sys.stdin).get('enrolled_miners', 'N/A'))")
    POT=$(echo $EPOCH | python3 -c "import sys,json; print(json.load(sys.stdin).get('epoch_pot', 'N/A'))")
    echo "  ✓ Epoch: $EPOCH_NUM | 已注册矿工: $ENROLLED | 奖池: ${POT} RTC"
else
    echo "  ✗ 无法获取 Epoch 信息"
fi

# 3. 网络统计
echo "[3/6] 获取网络统计..."
STATS=$(curl -sk --max-time 10 "$NODE_URL/api/stats")
if [ $? -eq 0 ]; then
    TOTAL_MINERS=$(echo $STATS | python3 -c "import sys,json; print(json.load(sys.stdin).get('total_miners', 'N/A'))")
    TOTAL_BALANCE=$(echo $STATS | python3 -c "import sys,json; print(json.load(sys.stdin).get('total_balance', 'N/A'))")
    BLOCK_TIME=$(echo $STATS | python3 -c "import sys,json; print(json.load(sys.stdin).get('block_time', 'N/A'))")
    echo "  ✓ 总矿工数: $TOTAL_MINERS | 总余额: ${TOTAL_BALANCE} RTC | 区块时间: ${BLOCK_TIME}s"
else
    echo "  ✗ 无法获取网络统计"
fi

# 4. Miner 列表（指定 miner）
if [ -n "$MINER_ID" ]; then
    echo "[4/6] 检查 Miner: $MINER_ID..."
    MINERS=$(curl -sk --max-time 10 "$NODE_URL/api/miners")
    RESULT=$(echo $MINERS | python3 -c "
import sys, json
try:
    miners = json.load(sys.stdin)
    for m in miners:
        if '$MINER_ID' in str(m.get('miner', '')):
            print(json.dumps(m, indent=2))
            sys.exit(0)
    print('未找到该 Miner')
except:
    print('解析失败')
")
    echo "$RESULT"
else
    echo "[4/6] 跳过 Miner 检查（未指定 MINER_ID）"
fi

# 5. 余额查询（指定 miner）
if [ -n "$MINER_ID" ]; then
    echo "[5/6] 查询余额..."
    BALANCE=$(curl -sk --max-time 10 "$NODE_URL/wallet/balance?miner_id=$MINER_ID")
    echo "  $BALANCE"
else
    echo "[5/6] 跳过余额查询（未指定 MINER_ID）"
fi

# 6. Prometheus Metrics
echo "[6/6] 检查 Metrics 端点..."
METRICS=$(curl -sk --max-time 10 "$NODE_URL/metrics")
if echo "$METRICS" | grep -q "Prometheus not available"; then
    echo "  ! Metrics 端点暂未启用"
else
    echo "  ✓ Metrics 可用"
fi

echo ""
echo "=========================================="
echo "诊断完成"
echo "=========================================="
```

**使用方式：**

```bash
# 保存脚本
chmod +x rustchain_diag.sh

# 运行通用诊断
./rustchain_diag.sh

# 运行并检查特定 Miner
./rustchain_diag.sh YOUR_MINER_ID
```

### 8.2 快速检查命令汇总

```bash
# 节点健康
curl -sk https://50.28.86.131/health

# Epoch 信息
curl -sk https://50.28.86.131/epoch

# 网络统计
curl -sk https://50.28.86.131/api/stats

# 获取 Miner 列表并保存
curl -sk https://50.28.86.131/api/miners -o miners.json

# 搜索特定 Miner
python3 -c "
import json
with open('miners.json') as f:
    miners = json.load(f)
for m in miners:
    if 'YOUR_MINER_ID' in str(m.get('miner', '')):
        print(json.dumps(m, indent=2))
"

# 查询余额
curl -sk "https://50.28.86.131/wallet/balance?miner_id=YOUR_MINER_ID"

# 测试节点版本
curl -sk https://50.28.86.131/health | python3 -c "import sys,json; h=json.load(sys.stdin); print('Version:', h['version'], '| OK:', h['ok'])"
```

---

## 联系方式与支持

- **Discord:** [discord.gg/VqVVS2CW9Q](https://discord.gg/VqVVS2CW9Q)
- **GitHub Issues:** [github.com/Scottcjn/rustchain-bounties/issues](https://github.com/Scottcjn/rustchain-bounties/issues)
- **区块浏览器:** [50.28.86.131/explorer](https://50.28.86.131/explorer)

---

> **提示：** 提交问题时请附带以下信息以加速排查：
> 1. 节点版本（`/health` 输出）
> 2. 完整的错误日志
> 3. 复现步骤
> 4. 使用的操作系统和 Python 版本
> 5. 节点 URL（如是自托管节点）
