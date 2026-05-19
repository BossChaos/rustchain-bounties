# RustChain 贡献者指南

> 欢迎为 RustChain 做贡献！本文档帮助你开始。

---

## 目录

1. [项目概览](#1-项目概览)
2. [开发环境设置](#2-开发环境设置)
3. [代码规范](#3-代码规范)
4. [贡献流程](#4-贡献流程)
5. [测试要求](#5-测试要求)
6. [文档贡献](#6-文档贡献)
7. [赏金任务](#7-赏金任务)
8. [社区资源](#8-社区资源)

---

## 1. 项目概览

RustChain 是一个基于硬件证明共识 (PoA) 的去中心化区块链平台。

### 核心组件

| 组件 | 说明 | 路径 |
|------|------|------|
| 节点 | 区块链节点服务 | `node/` |
| SDK | Python SDK | `sdk/python/` |
| 矿工 | 跨平台挖矿脚本 | `miners/` |
| 文档 | 项目文档 | `docs/` |
| 工具 | 辅助工具 | `tools/` |

### 技术栈

- **共识**: Proof of Attestation (PoA)
- **语言**: Python 3.8+
- **API**: REST API + OpenAPI 3.0
- **智能审查**: SophiaCore (AI-powered)

---

## 2. 开发环境设置

### 2.1 克隆仓库

```bash
git clone https://github.com/Scottcjn/Rustchain.git
cd Rustchain
```

### 2.2 安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 开发依赖
```

### 2.3 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_wallet.py

# 带覆盖率
pytest --cov=rustchain_sdk
```

### 2.4 代码格式

```bash
# 格式化代码
black .

# 检查类型
mypy .

# 检查代码质量
flake8 .
```

---

## 3. 代码规范

### 3.1 Python 风格

遵循 PEP 8 和 Black 格式化规则：

```python
# ✅ 正确
def calculate_balance(address: str, decimals: int = 18) -> float:
    """Calculate wallet balance with proper decimal handling."""
    pass

# ❌ 错误
def calcBal(addr,dec=18):
    pass
```

### 3.2 提交信息格式

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

类型：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 日常维护

示例：

```
feat(wallet): add multi-signature support

Implement multi-signature wallet with configurable threshold.
- Add MultiSigWallet class
- Add signature collection flow
- Add unit tests

Closes #123
```

---

## 4. 贡献流程

### 4.1 Fork 和克隆

1. 在 GitHub 上 Fork 仓库
2. 克隆到本地：

```bash
git clone https://github.com/YOUR_USERNAME/Rustchain.git
cd Rustchain
```

### 4.2 创建分支

```bash
git checkout -b feat/your-feature-name
```

### 4.3 提交更改

```bash
git add .
git commit -m "feat: your commit message"
git push origin feat/your-feature-name
```

### 4.4 创建 Pull Request

1. 在 GitHub 上创建 PR
2. 填写 PR 描述模板
3. 关联相关 Issue
4. 等待审核

### 4.5 PR 审核流程

1. 提交 PR 后，自动运行 CI 测试
2. 维护者进行代码审核
3. 根据反馈修改
4. 合并到主分支

---

## 5. 测试要求

### 5.1 单元测试

每个新功能必须有对应的单元测试：

```python
import pytest
from rustchain_sdk import Wallet

def test_wallet_creation():
    wallet = Wallet.create()
    assert wallet.address is not None
    assert wallet.mnemonic is not None
    assert len(wallet.mnemonic.split()) == 12

def test_wallet_recovery():
    wallet1 = Wallet.create()
    wallet2 = Wallet.from_mnemonic(wallet1.mnemonic)
    assert wallet1.address == wallet2.address
```

### 5.2 集成测试

测试完整工作流程：

```python
def test_full_transaction_flow():
    # 创建钱包
    sender = Wallet.create()
    receiver = Wallet.create()
    
    # 发送交易
    client = RustChainClient()
    tx = client.send_transaction(
        from_wallet=sender,
        to_address=receiver.address,
        amount="1.0"
    )
    
    # 验证交易
    assert tx['status'] == 'confirmed'
    assert client.get_balance(receiver.address)['balance'] == "1.0"
```

### 5.3 覆盖率要求

- 新功能：≥ 80% 行覆盖率
- Bug 修复：必须包含回归测试
- 文档更新：无需测试

---

## 6. 文档贡献

### 6.1 文档位置

所有文档位于 `docs/` 目录。

### 6.2 文档格式

- Markdown (.md)
- 包含代码示例
- 使用中文编写（优先）

### 6.3 文档赏金

参考 [Documentation Sprint #72](https://github.com/Scottcjn/rustchain-bounties/issues/72) 获取文档赏金任务列表。

---

## 7. 赏金任务

### 7.1 如何参与

1. 查看 [rustchain-bounties](https://github.com/Scottcjn/rustchain-bounties) 仓库
2. 选择感兴趣的 Issue
3. 在 Issue 中评论表示参与
4. 完成工作后提交 PR
5. 在 PR 中声明赏金

### 7.2 赏金声明格式

在 PR 描述中添加：

```markdown
## Bounty Claim

**Issue**: #XXX
**Reward**: XX RTC
**Type**: Documentation / Code / Review
```

### 7.3 可用赏金类型

| 类型 | 奖励范围 | 说明 |
|------|---------|------|
| 文档 | 10-25 RTC | 编写/改进文档 |
| 代码 | 15-50 RTC | 功能开发/Bug修复 |
| 审核 | 5-15 RTC | PR 代码审核 |
| 测试 | 10-30 RTC | 编写测试用例 |

---

## 8. 社区资源

### 8.1 链接

- GitHub: https://github.com/Scottcjn/Rustchain
- 赏金: https://github.com/Scottcjn/rustchain-bounties
- API 文档: https://rustchain.org/api

### 8.2 联系方式

- Slack: 加入 RustChain 社区
- GitHub Discussions: 提问和讨论

---

*文档版本: 1.0 | 最后更新: 2026-05-19*
*RustChain 团队感谢你的贡献！*
