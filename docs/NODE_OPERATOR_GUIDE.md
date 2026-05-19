# RustChain 节点操作员指南

> **RIP-200** — 运行 RustChain 认证节点的完整指南。

---

## 目录

1. [节点类型](#1-节点类型)
2. [系统要求](#2-系统要求)
3. [安装 RustChain 节点](#3-安装-rustchain-节点)
4. [配置认证节点](#4-配置认证节点)
5. [网络连接与同步](#5-网络连接与同步)
6. [监控与维护](#6-监控与维护)
7. [安全最佳实践](#7-安全最佳实践)
8. [故障排除](#8-故障排除)

---

## 1. 节点类型

### 1.1 全节点 (Full Node)

- 验证所有区块和交易
- 存储完整的区块链数据
- 参与网络共识

### 1.2 认证节点 (Attestation Node)

- 处理硬件认证请求
- 运行 SophiaCore 智能审查
- 验证矿工硬件指纹

### 1.3 轻节点 (Light Node)

- 仅验证区块头
- 不存储完整数据
- 适合资源受限环境

---

## 2. 系统要求

### 认证节点 (推荐)

| 项目 | 要求 |
|------|------|
| CPU | 4 核心以上，x86_64 |
| 内存 | 16 GB RAM |
| 存储 | 50 GB SSD |
| 网络 | 100 Mbps 以上，稳定连接 |
| 操作系统 | Ubuntu 22.04 LTS 或更高 |

### 全节点 (最低)

| 项目 | 要求 |
|------|------|
| CPU | 2 核心 |
| 内存 | 8 GB RAM |
| 存储 | 20 GB |
| 网络 | 10 Mbps |

---

## 3. 安装 RustChain 节点

### 3.1 安装依赖

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y build-essential pkg-config libssl-dev

# 安装 Rust（如果需要编译）
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# 安装 Python 3.10+
sudo apt install -y python3.10 python3-pip python3.10-venv
```

### 3.2 克隆仓库

```bash
git clone https://github.com/Scottcjn/Rustchain.git
cd Rustchain
```

### 3.3 安装 Python 依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3.4 配置节点

```bash
# 复制配置文件
cp config/node.example.yaml config/node.yaml

# 编辑配置
nano config/node.yaml
```

---

## 4. 配置认证节点

### 4.1 基础配置

```yaml
# config/node.yaml
node:
  name: "my-attestation-node"
  network: "mainnet"
  data_dir: "/var/lib/rustchain"
  
  # 监听地址
  rpc:
    host: "0.0.0.0"
    port: 8545
    
  # P2P 网络
  p2p:
    enabled: true
    port: 30303
    max_peers: 50
    
  # SophiaCore 配置
  sophia:
    enabled: true
    ollama_host: "http://localhost:11434"
    model: "rustchain-inspector"
    confidence_threshold: 0.8
```

### 4.2 启动节点

```bash
# 前台运行（调试）
python3 node/run_node.py --config config/node.yaml

# 后台运行
nohup python3 node/run_node.py --config config/node.yaml > node.log 2>&1 &

# 查看日志
tail -f node.log
```

---

## 5. 网络连接与同步

### 5.1 连接种子节点

```yaml
# 在配置中添加种子节点
p2p:
  bootnodes:
    - "enode://seed1@rustchain.org:30303"
    - "enode://seed2@50.28.86.131:30303"
```

### 5.2 检查同步状态

```bash
# 查询节点状态
curl http://localhost:8545/health

# 预期响应
{
  "status": "healthy",
  "version": "1.0.0",
  "sync_status": "synced",
  "peer_count": 12
}
```

---

## 6. 监控与维护

### 6.1 Prometheus 监控

```bash
# 启动 Prometheus 指标端点
# 节点默认在 /metrics 提供 Prometheus 格式指标

curl http://localhost:8545/metrics
```

### 6.2 Grafana 仪表板

推荐监控指标：
- 区块同步进度
- 连接对等体数量
- 认证请求处理量
- Sophia 审查延迟
- 内存和 CPU 使用率

### 6.3 日志轮转

```bash
# 配置 logrotate
sudo nano /etc/logrotate.d/rustchain
```

```
/var/log/rustchain/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

---

## 7. 安全最佳实践

### 7.1 防火墙配置

```bash
# 仅开放必要端口
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 8545/tcp  # RPC
sudo ufw allow 30303/tcp # P2P
sudo ufw enable
```

### 7.2 TLS 证书

```bash
# 使用 Let's Encrypt
sudo apt install certbot
sudo certbot certonly --standalone -d your-node.example.com
```

### 7.3 定期备份

```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backup/rustchain"
DATE=$(date +%Y%m%d)

# 备份数据目录
tar czf "$BACKUP_DIR/node-data-$DATE.tar.gz" /var/lib/rustchain

# 备份配置
cp config/node.yaml "$BACKUP_DIR/node-config-$DATE.yaml"

# 保留最近 7 天备份
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete
```

---

## 8. 故障排除

### 8.1 节点无法启动

```bash
# 检查日志
tail -100 node.log

# 检查端口占用
sudo lsof -i :8545
sudo lsof -i :30303

# 检查磁盘空间
df -h
```

### 8.2 同步卡顿

```bash
# 重置同步状态
python3 node/run_node.py --config config/node.yaml --reset-sync

# 检查网络连接
ping rustchain.org
```

### 8.3 SophiaCore 服务异常

```bash
# 检查 Ollama 服务
curl http://localhost:11434/api/tags

# 重启 SophiaCore
systemctl restart sophiacore
```

---

*文档版本: 1.0 | 最后更新: 2026-05-19*
