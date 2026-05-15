# RustChain Glossary

A comprehensive A-Z reference of 55+ terms covering RustChain-specific concepts, blockchain fundamentals, and related technologies.

---

## A

### API (Application Programming Interface)
A set of protocols and tools that allow different software applications to communicate. RustChain exposes a REST API for querying the chain state, submitting transactions, and interacting with miner nodes.

### ASIC (Application-Specific Integrated Circuit)
A specialized piece of hardware designed for a single purpose, such as Bitcoin mining. RustChain is deliberately ASIC-resistant — it rewards vintage general-purpose hardware instead.

### Atomic Swap
A smart contract that allows the exchange of one cryptocurrency for another without the need for a trusted third party. The wRTC bridge on Solana enables atomic swaps between wRTC (wrapped RTC) and native Solana tokens.

---

## B

### Beacon Node
A node in the RustChain network that coordinates block validation and propagates transactions across the network. Beacon nodes maintain the canonical chain state and communicate with miner nodes.

### Block
A batch of verified transactions recorded on the RustChain ledger. Each block contains a header (timestamp, previous block hash, merkle root, nonce) and a body (transaction list). RustChain deliberately produces blocks at a slow cadence to prioritize sustainability over throughput.

### Block Height
The number of blocks in the chain preceding a given block. Block 0 (the genesis block) has height 0. Each subsequent block increments the height by one.

### Block Reward
The amount of RTC awarded to a miner for successfully mining a block. In RustChain, the reward is weighted by hardware age — older processors receive higher multipliers.

### Bounty
A task posted on the RustChain Bounties platform (this repository) with a predetermined RTC reward. Bounties cover code contributions, documentation, bug reports, tutorials, and community work.

### Bridge
A protocol or mechanism that allows tokens or data to move between different blockchain networks. RustChain's wRTC (wrapped RTC) bridge connects to Solana, enabling RTC to circulate on high-throughput networks while the RustChain chain itself uses vintage hardware for consensus.

---

## C

### Chain State
The complete set of data representing the current status of the RustChain blockchain, including account balances, smart contract storage, and the transaction history leading to the current state.

### Consensus Mechanism
The method by which a distributed network agrees on the current state of the ledger. RustChain uses **Proof-of-Antiquity (PoA)**, which rewards hardware age and authenticity rather than computational work or financial stake.

### CPU (Central Processing Unit)
The primary processor of a computer. RustChain miners run on vintage CPUs, particularly PowerPC processors from Apple computers. The protocol can distinguish between CPU architectures (G3, G4, G5) and applies different mining multipliers based on age.

---

## D

### DAO (Decentralized Autonomous Organization)
An organization run by rules encoded as smart contracts, with no central authority. While RustChain itself is not a DAO, bounty governance and future protocol upgrades may involve DAO-like voting mechanisms.

### Difficulty
A network-wide parameter that controls how hard it is to mine a new block. RustChain's difficulty adjustment accounts for the diversity of hardware types, ensuring that both a G3 and a G5 can participate competitively within their respective hardware classes.

### Distributed Ledger
A database replicated across multiple nodes in a network, where all participants maintain an identical copy. Any changes are validated by consensus before being applied.

### DLT (Distributed Ledger Technology)
The broader category of technologies that enable decentralized record-keeping, of which RustChain is one example.

---

## E

### E-Waste (Electronic Waste)
Discarded electronic equipment. RustChain's core mission includes reducing e-waste by giving vintage computers a productive second life as mining nodes. A 1999 PowerPC G4 that would otherwise sit in a landfill earns RTC by running the RustChain miner.

### Epoch
A defined period of time or number of blocks after which certain network parameters are updated. In RustChain, epoch boundaries trigger difficulty adjustments and reward distribution.

### ERC-20
A technical standard for fungible tokens on the Ethereum Virtual Machine. RTC is not an ERC-20 token — it is a native coin on the RustChain chain. However, wRTC (wrapped RTC) on Solana follows SPL token standards.

### Ethereum Virtual Machine (EVM)
The runtime environment for executing smart contracts on Ethereum-compatible chains. RustChain does not use the EVM; it uses its own native execution model.

---

## F

### Finality
The assurance that a block cannot be reversed or changed. In RustChain, finality is achieved per-block due to the hardware-fingerprinting mechanism — once a block is accepted, reorganizing the chain would require re-mining on genuine vintage hardware.

### Fork
A split in the blockchain where two or more competing chains coexist temporarily. RustChain uses a longest-chain rule to resolve forks, with hardware authenticity serving as a Sybil-resistance mechanism during chain reorganizations.

### Full Node
A node that downloads and verifies the entire blockchain history. Full nodes in RustChain also validate hardware fingerprints submitted by miners.

### Fungible Token
A token where every unit is identical and interchangeable (like a dollar bill). RTC is a fungible native coin. Compare to **NFT**.

---

## G

### G3 / G4 / G5
Generations of PowerPC processors used in Apple Macintosh computers between 1997 and 2006. These are the primary mining hardware for RustChain:

- **G3**: First generation (1997-2003), ~300 MHz, used in original iMac and iBook.
- **G4**: Second generation (1999-2005), up to 1.8 GHz, used in PowerBook G4 and Power Mac G4.
- **G5**: Third generation (2003-2006), up to 2.7 GHz dual-core, used in Power Mac G5.

### Gas
A unit of computational work on EVM-compatible chains. RustChain does not use a gas model — transaction fees are fixed and minimal, designed for accessibility rather than compute markets.

### Genesis Block
The first block in the RustChain blockchain (Block 0). It contains the initial parameters of the network and is hardcoded into the miner software.

### GUI (Graphical User Interface)
A visual interface that allows users to interact with software through icons, windows, and menus. The RustChain dashboard provides a web-based GUI for monitoring miner status and network health.

---

## H

### Hard Fork
A permanent divergence in the blockchain protocol that makes previously invalid blocks valid. Hard forks require all nodes to upgrade. RustChain has not hard-forked yet.

### Hardware Fingerprinting
RustChain's core Sybil-resistance mechanism. The protocol measures CPU characteristics — including instruction timing, cache behavior, and FPU (floating-point unit) behavior — to cryptographically verify that mining occurs on genuine vintage silicon. Virtualized or emulated hardware produces detectable anomalies.

### Hash
The output of a cryptographic hash function. Each block header in RustChain contains a hash that commits to the previous block, creating an immutable chain. Hash functions used include SHA-256 variants suitable for the computational capabilities of PowerPC hardware.

### Hashrate
The total computational power dedicated to mining on the RustChain network, measured in hashes per second. Given RustChain's hardware diversity, hashrate is reported per hardware class (G3/G4/G5) rather than as a single aggregate number.

---

## I

### Immutable
Something that cannot be changed once written. Once a transaction is confirmed and added to a block on RustChain, it is immutable — there is no mechanism to reverse it except through a community-approved chain reorganization, which would require majority hardware consensus.

### Interoperability
The ability of different blockchain networks to communicate and share data. RustChain achieves interoperability through the wRTC bridge, which wraps RTC as an SPL token on Solana, enabling cross-chain DeFi participation.

---

## L

### Layer 1 (L1)
The base protocol of a blockchain network. RustChain is a Layer 1 chain, meaning it has its own consensus mechanism, ledger, and native token. Layer 2 solutions could theoretically be built on top of RustChain in the future.

### Light Node
A node that does not download the full blockchain. Light nodes rely on full nodes for block data and transaction verification. In RustChain, light nodes can query miner status and chain state without running a full mining node.

### Lightning Network
A Layer 2 payment protocol built on Bitcoin (and adaptable to other chains) that enables instant, low-fee transactions. RustChain does not currently implement Lightning, but its low-throughput design is philosophically aligned with the principle of few, meaningful transactions.

---

## M

### Merkle Tree
A data structure that allows efficient and secure verification of large datasets. Each block in RustChain contains a Merkle root hash of all transactions in that block, enabling lightweight clients to verify transaction inclusion without downloading the entire block.

### Miner
A participant in the RustChain network who runs the mining software on vintage hardware to produce blocks and earn RTC rewards. The term "miner" is used instead of "validator" because RustChain's mechanism is not staking-based.

### Mining Multiplier
A reward boost given to miners based on hardware age. The multiplier scales with the era of the processor:
- **G3**: 2.5x multiplier (oldest, rarest hardware)
- **G4**: 1.5x multiplier
- **G5**: 1.0x multiplier (still vintage but more modern)

### Multisig (Multi-Signature)
A transaction requiring multiple private keys to authorize. Multisig wallets can be used for RustChain treasury management, bounty payments, and DAO-like governance.

---

## N

### Native Coin
A cryptocurrency token that is built into the base protocol of a blockchain, as opposed to a token built on top of an existing chain (like an ERC-20). RTC is RustChain's native coin, used for transaction fees, staking (future), and bounty rewards.

### Node
Any computer connected to the RustChain network that runs the RustChain software and participates in the peer-to-peer network. Nodes can be full nodes (validate everything), mining nodes (produce blocks), or light nodes (query data).

### Nonce
A number used only once. In RustChain mining, miners vary a nonce value in the block header until they find a hash that meets the difficulty target. The nonce is a key component of the proof-of-work (in traditional PoW chains) or, in RustChain's case, the proof-of-computation on vintage hardware.

---

## O

### Opcode
A low-level instruction executed by a virtual machine. RustChain uses its own instruction set optimized for the capabilities of PowerPC processors, rather than the EVM opcodes used by Ethereum.

### Oracle
A service that feeds external real-world data into a blockchain. RustChain does not have a native oracle implementation, but external oracles could be integrated via bridge contracts on connected chains (Solana).

---

## P

### Peer-to-Peer (P2P)
A network architecture where participants communicate directly with each other without intermediaries. RustChain nodes connect in a P2P mesh to propagate blocks and transactions.

### PoA (Proof-of-Antiquity)
RustChain's novel consensus mechanism. Unlike Proof-of-Work (which rewards computational power) or Proof-of-Stake (which rewards locked capital), PoA rewards the age and authenticity of hardware. The protocol uses hardware fingerprinting to ensure that miners are running on genuine vintage processors.

### PoS (Proof-of-Stake)
A consensus mechanism where validators lock up (stake) cryptocurrency as collateral to participate in block production. Ethereum uses PoS. RustChain uses PoA instead.

### PoW (Proof-of-Work)
A consensus mechanism where miners compete to solve computationally expensive puzzles. Bitcoin uses PoW. RustChain does not use traditional PoW — its mining is hardware-verification-based rather than puzzle-solving.

### Private Key
A secret cryptographic key that allows a user to sign transactions and access their funds. Whoever holds the private key controls the associated RTC. Private keys must be kept secure — loss means permanent loss of funds.

### Protocol
The set of rules that define how a blockchain operates. The RustChain protocol specifies block structure, consensus rules, transaction format, and network communication standards.

### Public Address
A publicly shareable identifier for receiving RTC, derived from a public key. Addresses on RustChain follow a custom format starting with "RTC" (e.g., `RTC6d1f27d28961279f1034d9561c2403697eb55602`).

### Public Key
A cryptographic key derived from a private key, used to verify digital signatures. The public key can be shared freely; the private key must be kept secret.

---

## Q

### Query
A request to read data from the RustChain network. Queries (read operations) are typically free and do not require a transaction or fee. Examples include checking a wallet balance, fetching block data, or reading smart contract state.

---

## R

### Re-org (Chain Reorganization)
An event where the network abandons the current longest chain in favor of an alternative chain that has more accumulated work (or, in RustChain's case, more accumulated hardware-verified blocks). Deep re-orgs are extremely expensive in RustChain due to the hardware fingerprinting requirement.

### Reward Distribution
The mechanism by which block rewards are split among miners and any protocol-level allocations (e.g., treasury, developer fund). RustChain's reward distribution is handled at the epoch level.

### RTC (RustChain Coin)
The native cryptocurrency of the RustChain network. Used for transaction fees, miner rewards, and bounty payments. RTC can be wrapped (wRTC) and bridged to Solana via the wRTC bridge.

### RustChain Miner
The Python-based software that allows vintage computers to participate in the RustChain network as mining nodes. Available in the `rustchain-miner/` directory of this repository. Supports PowerPC G3/G4/G5 processors.

---

## S

### SHA (Secure Hash Algorithm)
A family of cryptographic hash functions. RustChain uses SHA-family algorithms for block hashing and Merkle tree construction, chosen for their compatibility with PowerPC instruction sets.

### Smart Contract
Self-executing code deployed on a blockchain that automatically enforces the terms of an agreement. RustChain has its own smart contract capability, though its execution model differs from the EVM.

### Soft Fork
A backward-compatible protocol change where existing rules become stricter. Soft forks do not require all nodes to upgrade. RustChain has not soft-forked yet.

### Solana
A high-throughput Layer 1 blockchain known for its fast transaction finality and low fees. RustChain is interoperable with Solana via the wRTC bridge, which wraps RTC as an SPL-compatible token.

### SPL Token
The token standard on Solana, analogous to ERC-20 on Ethereum. wRTC is an SPL token representing wrapped RTC on Solana.

### Staking
Locking cryptocurrency as collateral to participate in network validation. Currently, RustChain uses hardware-based mining rather than financial staking. A staking mechanism may be introduced in future protocol upgrades.

### Sybil Attack
An attack where a single entity creates multiple fake identities to gain disproportionate influence over a network. RustChain's hardware fingerprinting makes Sybil attacks expensive — an attacker would need to acquire many distinct, genuinely vintage machines rather than spinning up virtual instances.

---

## T

### Throughput
The number of transactions a blockchain can process per second (TPS). RustChain has low throughput by design — it prioritizes meaningful, verified transactions over raw volume. The wRTC bridge on Solana enables high-throughput use cases without compromising RustChain's core philosophy.

### Transaction
A signed data package that broadcasts a state change on the RustChain network. Transactions can transfer RTC, deploy smart contracts, or interact with existing contracts. Each transaction requires a valid signature from the sender's private key.

### Transaction Fee
A small amount of RTC paid to miners for processing a transaction. In RustChain, fees are minimal by design to keep the network accessible.

### TPS (Transactions Per Second)
A measure of blockchain throughput. RustChain targets a low TPS (by modern standards) as a deliberate choice — each transaction on the chain represents a hardware-verified action worth recording permanently.

### Treasury
A pool of funds managed by the RustChain community for development, bounty payments, and ecosystem growth. The treasury is governed by multisig keys held by trusted community members.

---

## U

### UTXO (Unspent Transaction Output)
A model used by some blockchains (like Bitcoin) where transaction outputs are either spent or unspent. RustChain uses an account-based model rather than UTXO, similar to Ethereum.

---

## V

### Validator
In traditional PoS chains, a validator is a participant who stakes capital to propose and attest to blocks. In RustChain, the equivalent role is the **miner** — someone running vintage hardware that has been fingerprinted and verified by the network.

### Virtual Machine
A software environment that executes smart contracts. Ethereum uses the EVM. RustChain uses a custom VM designed for its own instruction set and hardware compatibility.

### Vote
A mechanism for on-chain governance. While RustChain currently uses off-chain bounty governance (via GitHub Issues in this repository), future protocol changes may be decided by on-chain votes weighted by hardware age or token holdings.

---

## W

### Wallet
Software or hardware that stores private keys and allows users to interact with the RustChain network. Wallets can be:
- **Hot wallet**: Connected to the internet, for everyday transactions
- **Cold wallet**: Air-gapped or hardware-based, for secure long-term storage
- **Multisig wallet**: Requires multiple keys to authorize transactions

### wRTC (Wrapped RTC)
A version of RTC that exists on the Solana blockchain, wrapped via a bridge mechanism. wRTC is an SPL token that maintains a 1:1 peg with native RTC. It enables RTC to participate in Solana's DeFi ecosystem (lending, liquidity pools, swaps) while RustChain's own chain remains dedicated to vintage hardware mining.

### Wrapped Token
A token that represents an asset from another blockchain in a pegged, 1:1 ratio. Wrapping enables cross-chain liquidity. wRTC is the wrapped version of RTC, bridging RustChain's native coin to Solana.

---

## X

### Cross-Chain
Referring to interactions, bridges, or operations that span multiple blockchain networks. The wRTC bridge is RustChain's primary cross-chain mechanism, connecting to Solana.

---

## Z

### Zero-Knowledge Proof
A cryptographic technique that allows one party to prove knowledge of a statement without revealing the underlying data. While not currently a core feature of RustChain, ZK proofs could be integrated in future protocol upgrades for enhanced privacy.

---

*Closes [#9557](https://github.com/Scottcjn/rustchain-bounties/issues/9557)*
