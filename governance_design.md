# RustChain On-Chain Governance — Implementation Design

**Author:** BossChaos  
**Bounty:** #50 (50-100 RTC)  
**Wallet:** RTC6d1f27d28961279f1034d9561c2403697eb55602

---

## Executive Summary

Design for an on-chain governance system where RTC holders can propose and vote on network changes. The system ties voting power to the existing Proof-of-Antiquity antiquity_multiplier, ensuring vintage hardware miners have proportional influence.

---

## Architecture

### Database Schema

```sql
CREATE TABLE governance_proposals (
    id TEXT PRIMARY KEY,
    rip_number TEXT NOT NULL UNIQUE,
    proposer_wallet TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL, -- 'protocol', 'bounty', 'parameter', 'treasury'
    status TEXT NOT NULL DEFAULT 'active', -- 'active', 'passed', 'rejected', 'vetoed', 'expired'
    yes_votes_urtc INTEGER NOT NULL DEFAULT 0,
    no_votes_urtc INTEGER NOT NULL DEFAULT 0,
    abstain_votes_urtc INTEGER NOT NULL DEFAULT 0,
    quorum_required INTEGER NOT NULL DEFAULT 100000, -- URTC threshold
    voting_period_blocks INTEGER NOT NULL DEFAULT 2016, -- ~2 weeks at 600s/block
    created_at INTEGER NOT NULL,
    expires_at INTEGER NOT NULL,
    onchain_tx TEXT,
    metadata TEXT
);

CREATE TABLE governance_votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id TEXT NOT NULL,
    voter_wallet TEXT NOT NULL,
    vote TEXT NOT NULL, -- 'yes', 'no', 'abstain'
    voting_power_urtc INTEGER NOT NULL,
    antiquity_multiplier REAL NOT NULL,
    block_height INTEGER NOT NULL,
    voter_ip TEXT,
    signature TEXT NOT NULL,
    voted_at INTEGER NOT NULL,
    UNIQUE(proposal_id, voter_wallet)
);

CREATE TABLE governance_delegations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    delegator_wallet TEXT NOT NULL,
    delegate_wallet TEXT NOT NULL,
    voting_power_percentage INTEGER NOT NULL DEFAULT 100,
    created_at INTEGER NOT NULL,
    revoked_at INTEGER,
    UNIQUE(delegator_wallet, delegate_wallet)
);

CREATE INDEX idx_votes_proposal ON governance_votes(proposal_id);
CREATE INDEX idx_votes_wallet ON governance_votes(voter_wallet);
```

---

## API Endpoints

### POST /governance/propose

Create a new governance proposal.

**Request:**
```json
{
  "title": "RIP-0145: Increase vintage hardware bonus to 3.0x",
  "description": "Proposal to increase the base antiquity multiplier for pre-2000 hardware from 2.0x to 3.0x...",
  "category": "parameter",
  "quorum_urpc": 100000,
  "voting_period_blocks": 2016,
  "metadata": {"affected_file": "CPU_ANTIQUITY_SYSTEM.md", "current_value": "2.0", "proposed_value": "3.0"},
  "signature": "<Ed25519 signature of RIP_NUMBER + proposer_wallet + title_hash>"
}
```

**Response:**
```json
{
  "proposal_id": "RIP-0145-abc123",
  "rip_number": "RIP-0145",
  "status": "active",
  "expires_at": 1779000000,
  "onchain_tx": "tx_hash_here"
}
```

**Validation:**
- Proposer must have ≥ 1000 RTC balance
- RIP number must not already exist on-chain
- Description must be ≥ 100 characters
- Signature must verify against proposer's public key

---

### GET /governance/proposals

List all proposals with pagination.

**Query params:** `?status=active&category=protocol&limit=20&offset=0`

**Response:**
```json
{
  "proposals": [
    {
      "id": "RIP-0145-abc123",
      "rip_number": "RIP-0145",
      "title": "Increase vintage hardware bonus",
      "category": "parameter",
      "status": "active",
      "yes_votes_urtc": 150000,
      "no_votes_urtc": 45000,
      "abstain_votes_urtc": 10000,
      "quorum_met": true,
      "current_result": "likely_pass",
      "expires_at": 1779000000
    }
  ],
  "total": 47,
  "page": 1
}
```

---

### POST /governance/vote

Cast a vote on an active proposal.

**Request:**
```json
{
  "proposal_id": "RIP-0145-abc123",
  "vote": "yes",
  "wallet_address": "RTCabc123...",
  "signature": "<Ed25519 sig of proposal_id + wallet + vote + nonce>"
}
```

**Voting Power Formula:**
```
voting_power_urtc = rtc_balance * antiquity_multiplier

# Examples from live network:
# POWER8 miner (2.0x multiplier, 500 RTC): 500 * 2.0 = 1000 URTC
# Modern x86 (0.8x multiplier, 1000 RTC): 1000 * 0.8 = 800 URTC
# Raspberry Pi (0.0005x penalty, 10000 RTC): 10000 * 0.0005 = 5 URTC
```

**Response:**
```json
{
  "vote_id": 12345,
  "proposal_id": "RIP-0145-abc123",
  "vote": "yes",
  "voting_power_urtc": 1000,
  "current_yes_urtc": 151000,
  "current_no_urtc": 45000
}
```

---

### GET /governance/proposal/{id}

Full proposal details with vote breakdown.

---

## Voting Outcomes

| Condition | Result |
|-----------|--------|
| `yes > no` AND `yes >= quorum` | **PASSED** |
| `no >= yes` | **REJECTED** |
| Expires before quorum met | **EXPIRED** |
| Admin veto (critical security) | **VETOED** |

---

## Implementation Notes

1. **Antiquity multiplier tie-in:** Voting power = `balance * antiquity_multiplier`. This rewards real hardware commitment, not just token holding.

2. **Signature requirements:** All proposals and votes require valid Ed25519 signatures tied to the wallet address. No anonymous voting.

3. **No-transfer clause:** Votes are tied to the wallet at block snapshot. Tokens moved after vote submission don't retroactively change voting power.

4. **Delegation:** RTC holders can delegate voting power to another wallet (partial or full), enabling staking pool participation in governance.

5. **Treasury category:** Proposals with `category=treasury` require higher quorum (500000 URTC) and 67% supermajority.

---

## File Structure

```
node/
  governance.py           # Main Flask routes + vote tallying
  governance_db.py        # Database initialization + queries
  governance_signature.py # Signature verification
proposals/
  RIP-0145_governance.py # Example proposal implementation
scripts/
  tally_votes.py         # Admin script to finalize expired proposals
tests/
  test_governance.py     # Unit tests for all endpoints
```
