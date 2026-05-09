# RustChain Bounty Hunter — VS Code Extension

**Bounty: #2868 (30 RTC)** — VS Code Extension for RustChain Bounty Hunters

## Features

- **Status Bar** showing wallet balance, mining status, and epoch info
- **Bounty Browser** — tree view of all open bounties from rustchain-bounties repo
- **Quick Actions** — refresh status, view bounties, claim bounties
- **Configurable** — set your node URL and wallet address in VS Code settings

## Files

- `extension.ts` — full TypeScript source (wallet balance, miner status, epoch info, bounty tree)
- `package.json` — VS Code extension manifest
- `rustchain-bounty-hunter-1.0.0.vsix` — pre-built extension package

## Installation

```bash
code --install-extension rustchain-bounty-hunter-1.0.0.vsix
```

Or install from `.vsix` via VS Code: `Extensions → ... → Install from VSIX`

## Configuration

```json
{
  "rustchain.nodeUrl": "https://50.28.86.131",
  "rustchain.walletName": "RTC6d1f27d28961279f1034d9561c2403697eb55602"
}
```

## Screenshots

Shows in status bar:
- `$(wallet) RTC: 1041.00` — current wallet balance
- `$(debug-start) Mining` / `$(debug-stop) Not Mining` — mining status
- `$(clock) Epoch: X/Y` — current epoch

Sidebar shows all open bounties from the rustchain-bounties repository.

## Building from Source

```bash
npm install
npm run compile
npx vsce package
```

## RTC Wallet

RTC6d1f27d28961279f1034d9561c2403697eb55602
