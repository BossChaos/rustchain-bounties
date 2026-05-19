# RustChain 矿工设置完整指南

> **RIP-200 硬件证明共识 (Proof of Attestation)** — 在真实硬件上运行 RustChain 矿工的完整步骤。
> 
> **重要**: RustChain 必须在**真实硬件**上运行。虚拟机可能能够认证，但奖励可能被扣除或拒绝。

---

## 目录

1. [系统要求](#1-系统要求)
2. [获取矿工脚本](#2-获取矿工脚本)
3. [Linux 安装与运行](#3-linux-安装与运行)
4. [macOS 安装与运行](#4-macos-安装与运行)
5. [Windows 安装与运行](#5-windows-安装与运行)
6. [钱包与矿工 ID](#6-钱包与矿工-id)
7. [连接到网络节点](#7-连接到网络节点)
8. [查看矿工状态](#8-查看矿工状态)
9. [故障排除](#9-故障排除)
10. [常见问题](#10-常见问题)

---

## 1. 系统要求

### 最低配置

| 项目 | 要求 |
|------|------|
| CPU | x86_64 架构（Intel/AMD），2 核心以上 |
| 内存 | 4 GB RAM |
| 存储 | 500 MB 可用空间 |
| Python | 3.8 或更高版本 |
| 网络 | 稳定的互联网连接 |
| 操作系统 | Linux (x86_64) / macOS (Intel/M1/M2) / Windows 10+ |

### 推荐配置

| 项目 | 推荐 |
|------|------|
| CPU | 4 核心以上 |
| 内存 | 8 GB RAM |
| GPU | NVIDIA GPU（可获得额外算力） |
| 网络 | 带宽 ≥ 10 Mbps |

### ⚠️ 重要限制

- **不能使用虚拟机**：AWS EC2、Google Cloud VM、Docker 容器等均不符合 PoA 要求
- **必须使用真实物理硬件**：矿工会收集硬件指纹进行认证
- **虚拟机挖矿可能被检测到并拒绝奖励**

---

## 2. 获取矿工脚本

### 方法一：克隆完整仓库（推荐）

```bash
git clone https://github.com/Scottcjn/Rustchain.git
cd Rustchain
```

优点：自动获取最新更新，包含所有平台脚本。

### 方法二：直接下载脚本

```bash
# Linux (x86_64)
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/miners/linux/rustchain_linux_miner.py -o rustchain_linux_miner.py

# macOS (Intel / Apple Silicon)
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/miners/macos/rustchain_mac_miner_v2.4.py -o rustchain_mac_miner_v2.4.py

# Windows (GUI 矿工)
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/miners/windows/rustchain_windows_miner.py -o rustchain_windows_miner.py
```

---

## 3. Linux 安装与运行

### 3.1 从仓库运行

```bash
cd Rustchain
python3 miners/linux/rustchain_linux_miner.py --wallet YOUR_MINER_ID
```

### 3.2 从独立脚本运行

```bash
python3 rustchain_linux_miner.py --wallet YOUR_MINER_ID
```

### 3.3 配置节点地址

Linux 矿工脚本中使用 `NODE_URL` 常量指定节点地址。如果需要连接不同的节点，编辑脚本中的该常量：

```python
# 在 rustchain_linux_miner.py 中找到这行
NODE_URL = "https://rustchain.org"
# 修改为自定义节点
# NODE_URL = "https://50.28.86.131"
```

### 3.4 作为后台服务运行

```bash
# 使用 nohup 后台运行
nohup python3 rustchain_linux_miner.py --wallet my_miner > miner.log 2>&1 &

# 查看日志
tail -f miner.log

# 停止矿工
pkill -f rustchain_linux_miner
```

### 3.5 使用 systemd 管理（推荐）

创建 systemd 服务文件：

```bash
sudo nano /etc/systemd/system/rustchain-miner.service
```

内容：

```ini
[Unit]
Description=RustChain Miner
After=network.target

[Service]
Type=simple
User=YOUR_USER
WorkingDirectory=/path/to/Rustchain/miners/linux
ExecStart=/usr/bin/python3 rustchain_linux_miner.py --wallet YOUR_MINER_ID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable rustchain-miner
sudo systemctl start rustchain-miner
sudo systemctl status rustchain-miner
```

---

## 4. macOS 安装与运行

### 4.1 从仓库运行

```bash
cd Rustchain
python3 miners/macos/rustchain_mac_miner_v2.4.py --wallet YOUR_MINER_ID --node https://50.28.86.131
```

### 4.2 从独立脚本运行

```bash
python3 rustchain_mac_miner_v2.4.py --wallet YOUR_MINER_ID --node https://50.28.86.131
```

### 4.3 macOS 特定注意事项

- **Apple Silicon (M1/M2)**: 确保使用 arm64 版本的 Python
- **Intel Mac**: 使用 x86_64 版本的 Python
- **系统权限**: 首次运行时 macOS 可能弹出安全提示，允许 Python 访问网络

### 4.4 Python 版本检查

```bash
# 检查 Python 版本
python3 --version

# 如果是 macOS 自带的旧版本 Python，使用 Homebrew 安装
brew install python3
```

---

## 5. Windows 安装与运行

### 5.1 安装 Python

1. 从 [python.org](https://python.org) 下载 Python 3.8+ 安装程序
2. 安装时勾选 **"Add Python to PATH"**
3. 完成安装后验证：

```cmd
python --version
```

### 5.2 运行矿工

```cmd
python rustchain_windows_miner.py --wallet YOUR_MINER_ID
```

### 5.3 Windows GUI 矿工

Windows 版本包含图形界面，运行后会弹出窗口显示：
- 当前算力
- 已挖区块数
- 连接状态
- 钱包余额

### 5.4 防火墙设置

Windows Defender 可能阻止矿工访问网络。需要添加入站规则：

1. 打开 Windows Defender 防火墙
2. 高级设置 → 入站规则 → 新建规则
3. 选择"程序" → 浏览到 Python 可执行文件
4. 允许连接

---

## 6. 钱包与矿工 ID

### 6.1 创建钱包

矿工 ID 就是你的钱包名称，用于接收挖矿奖励。

```python
from rustchain_sdk import Wallet

# 创建新钱包
wallet = Wallet.create()
print(f"钱包地址: {wallet.address}")
print(f"助记词: {wallet.mnemonic}")

# ⚠️ 务必安全保存助记词！
```

### 6.2 使用现有钱包

```python
# 从助记词恢复
wallet = Wallet.from_mnemonic("your twelve word mnemonic phrase here")

# 从私钥恢复
wallet = Wallet.from_private_key("0xprivatekey...")
```

### 6.3 矿工 ID 命名规范

- 可以使用任何字符串作为矿工 ID
- 建议：使用钱包地址前 8 位或自定义名称
- 示例：`--wallet 0x742d35Cc` 或 `--wallet my_first_miner`

### 6.4 查询钱包余额

```bash
curl "https://rustchain.org/wallet/balance?address=YOUR_ADDRESS"
```

或使用 Python SDK：

```python
from rustchain_sdk import RustChainClient

client = RustChainClient()
balance = client.get_balance("YOUR_ADDRESS")
print(f"余额: {balance['balance']} RTC")
```

---

## 7. 连接到网络节点

### 7.1 公共节点

| 节点地址 | 位置 | 状态 |
|---------|------|------|
| https://rustchain.org | 主节点 | 默认 |
| https://50.28.86.131 | 备用节点 | 可用 |

### 7.2 切换节点

在矿工脚本中修改 `NODE_URL` 常量：

```python
NODE_URL = "https://50.28.86.131"  # 备用节点
```

### 7.3 检查节点连通性

```bash
# 健康检查
curl https://rustchain.org/health

# 预期响应
# {"status": "healthy", "version": "1.0.0", "timestamp": 1640000000}
```

### 7.4 网络状态查询

```bash
# 当前 Epoch
curl https://rustchain.org/epoch

# 活跃矿工列表
curl "https://rustchain.org/api/miners?limit=5"
```

---

## 8. 查看矿工状态

### 8.1 日志输出

矿工运行时会输出以下信息：

```
[2024-01-15 12:00:00] Miner started with wallet: my_miner
[2024-01-15 12:00:01] Connected to node: https://rustchain.org
[2024-01-15 12:00:02] Hardware fingerprint collected
[2024-01-15 12:00:03] Attestation submitted: 0xabc123...
[2024-01-15 12:00:05] Mining... Block #456789
```

### 8.2 关键日志含义

| 日志信息 | 含义 |
|---------|------|
| "Miner started" | 矿工成功启动 |
| "Connected to node" | 网络连接正常 |
| "Hardware fingerprint collected" | 硬件指纹采集完成 |
| "Attestation submitted" | 认证成功 |
| "Mining... Block #XXX" | 正在挖矿 |
| "Block found!" | 成功挖到区块 |

### 8.3 查询矿工排名

```bash
# 查看矿工在网络中的排名
curl "https://rustchain.org/api/miners?limit=100" | grep -A2 "YOUR_ADDRESS"
```

---

## 9. 故障排除

### 9.1 连接失败

**问题**: `ConnectionError: Could not connect to node`

**解决方案**:
1. 检查网络连接
2. 尝试备用节点
3. 检查防火墙设置

```bash
# 测试连通性
ping rustchain.org

# 测试端口
curl -I https://rustchain.org/health
```

### 9.2 Python 版本过旧

**问题**: `SyntaxError: invalid syntax`

**解决方案**:
```bash
# 检查版本
python3 --version

# 升级 Python
# Ubuntu/Debian
sudo apt update && sudo apt install python3.10

# macOS (Homebrew)
brew upgrade python3

# Windows
# 重新从 python.org 下载安装
```

### 9.3 硬件指纹采集失败

**问题**: `FingerprintError: Could not collect hardware fingerprint`

**解决方案**:
- 确认在真实硬件上运行（非虚拟机）
- 检查系统权限
- Linux: 确保有 `dmidecode` 或 `lshw` 命令

```bash
# 安装硬件信息工具
# Ubuntu/Debian
sudo apt install dmidecode lshw

# macOS
brew install hwinfo
```

### 9.4 认证失败

**问题**: `AttestationError: Signature verification failed`

**解决方案**:
1. 检查钱包地址格式
2. 确认私钥正确
3. 重新创建钱包

### 9.5 内存不足

**问题**: `MemoryError`

**解决方案**:
```bash
# 检查可用内存
free -h

# 关闭不必要的应用
# 增加 swap 空间
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 10. 常见问题

### Q: 可以在云服务器上挖矿吗？

**A**: 不建议。RustChain 使用 PoA（硬件证明）共识机制，需要真实硬件指纹。云服务器（AWS EC2、Google Cloud 等）的硬件指纹可能被检测到并拒绝奖励。

### Q: 挖矿需要 GPU 吗？

**A**: 不需要。CPU 即可挖矿，但有 GPU 可能获得更高的算力和更多的奖励。

### Q: 一个钱包可以运行多个矿工吗？

**A**: 可以。每个矿工使用相同的钱包地址，但需要不同的硬件指纹。

### Q: 挖矿奖励如何计算？

**A**: 奖励基于以下因素：
- 出块数量
- 硬件证明质量
- 网络难度
- Epoch 周期

### Q: 如何查看我的挖矿收益？

**A**: 使用钱包余额查询：

```bash
curl "https://rustchain.org/wallet/balance?address=YOUR_ADDRESS"
```

### Q: 矿工意外退出怎么办？

**A**: 使用 systemd 或 nohup 运行矿工会自动重启。也可以设置 cron job：

```bash
# 每 5 分钟检查矿工是否在运行
*/5 * * * * pgrep -f rustchain_linux_miner || python3 /path/to/rustchain_linux_miner.py --wallet my_miner
```

---

*文档版本: 1.0 | 最后更新: 2026-05-19*
*基于 RustChain 仓库代码和 openapi.yaml 规范编写*
