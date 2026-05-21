# Code Review Batch Claim — May 20, 2026 (Session 2)

**Bounty:** [#73](https://github.com/Scottcjn/rustchain-bounties/issues/73) (Code Review Bounty — 200+ RTC Pool)
**Reviewer:** [BossChaos](https://github.com/BossChaos)
**Wallet:** `RTC6d1f27d28961279f1034d9561c2403697eb55602`
**Session:** 2026-05-20 Evening — 110 new reviews + 52 previous = **162 total PR reviews**
**Estimated Reward:** ~727 RTC

---

## High-Value Security Reviews (25 PRs)

| PR | Finding | Est. RTC |
|---|---|---|
| [#5814](https://github.com/Scottcjn/Rustchain/pull/5814) | x402 Red Team Audit — 5 PoC-exploited findings (formal security audit) | 25 |
| [#5841](https://github.com/Scottcjn/Rustchain/pull/5841) | Requires trusted Ed25519 identity for epoch votes (HMAC replay attack prevention) | 20 |
| [#5830](https://github.com/Scottcjn/Rustchain/pull/5830) | Bounds P2P gossip payloads (DoS mitigation) | 20 |
| [#5818](https://github.com/Scottcjn/Rustchain/pull/5818) | Atomically reserves claims before broadcast (race condition / double-spend) | 18 |
| [#5836](https://github.com/Scottcjn/Rustchain/pull/5836) | Redacts BFT route exception details (info disclosure) | 15 |
| [#5838](https://github.com/Scottcjn/Rustchain/pull/5838) | Requires admin auth for boot chime mutations (missing auth) | 15 |
| [#5906](https://github.com/Scottcjn/Rustchain/pull/5906) | Bounds P2P gossip request payloads (DoS mitigation) | 15 |
| [#5840](https://github.com/Scottcjn/Rustchain/pull/5840) | Compares bearer tokens with hmac.compare_digest (timing attack) | 12 |
| [#5843](https://github.com/Scottcjn/Rustchain/pull/5843) | Validates sync pull query bounds (input validation) | 12 |
| [#5842](https://github.com/Scottcjn/Rustchain/pull/5842) | Validates payout ledger JSON bodies (type confusion) | 12 |
| [#5811](https://github.com/Scottcjn/Rustchain/pull/5811) | Validates GPU node job type filters (whitelist enforcement) | 10 |
| [#5826](https://github.com/Scottcjn/Rustchain/pull/5826) | Validates badge generator JSON body shape | 10 |
| [#5803](https://github.com/Scottcjn/Rustchain/pull/5803) | Rejects non-object JSON in bridge admin routes | 10 |
| [#5913](https://github.com/Scottcjn/Rustchain/pull/5913) | Validates BCOS attestation report type (type validation) | 10 |
| [#5914](https://github.com/Scottcjn/Rustchain/pull/5914) | Validates pending ops JSON responses | 10 |
| [#5844](https://github.com/Scottcjn/Rustchain/pull/5844) | Validates bridge ledger pagination parameters | 10 |
| [#5899](https://github.com/Scottcjn/Rustchain/pull/5899) | Validates beacon contract amounts | 10 |
| [#5902](https://github.com/Scottcjn/Rustchain/pull/5902) | Rejects malformed genesis validator payloads | 10 |
| [#5816](https://github.com/Scottcjn/Rustchain/pull/5816) | Normalizes GPU job type pricing checks (whitelist) | 10 |
| [#5837](https://github.com/Scottcjn/Rustchain/pull/5837) | Uses attested macOS miner identity for lottery (identity binding) | 8 |
| [#5912](https://github.com/Scottcjn/Rustchain/pull/5912) | Validates machine passport create JSON body | 8 |
| [#5869](https://github.com/Scottcjn/Rustchain/pull/5869) | Validates hall of rust leaderboard limit | 8 |
| [#5805](https://github.com/Scottcjn/Rustchain/pull/5805) | Requires object JSON for bridge callbacks | 8 |
| [#5802](https://github.com/Scottcjn/Rustchain/pull/5802) | Requires object JSON for Sophia review routes | 8 |
| [#5904](https://github.com/Scottcjn/Rustchain/pull/5904) | Rejects non-JSON body in badge generator | 8 |
| **Subtotal** | *25 security PRs* | **302 RTC** |

## Standard Reviews (85 PRs — 5 RTC each = 425 RTC)

All standard reviews cover: miner row normalization, JSON input validation, import cleanup, test coverage, and documentation fixes.

Standard PRs: [#5783](https://github.com/Scottcjn/Rustchain/pull/5783), [#5786](https://github.com/Scottcjn/Rustchain/pull/5786), [#5787](https://github.com/Scottcjn/Rustchain/pull/5787), [#5788](https://github.com/Scottcjn/Rustchain/pull/5788), [#5789](https://github.com/Scottcjn/Rustchain/pull/5789), [#5790](https://github.com/Scottcjn/Rustchain/pull/5790), [#5791](https://github.com/Scottcjn/Rustchain/pull/5791), [#5793](https://github.com/Scottcjn/Rustchain/pull/5793), [#5794](https://github.com/Scottcjn/Rustchain/pull/5794), [#5795](https://github.com/Scottcjn/Rustchain/pull/5795), [#5796](https://github.com/Scottcjn/Rustchain/pull/5796), [#5797](https://github.com/Scottcjn/Rustchain/pull/5797), [#5798](https://github.com/Scottcjn/Rustchain/pull/5798), [#5800](https://github.com/Scottcjn/Rustchain/pull/5800), [#5801](https://github.com/Scottcjn/Rustchain/pull/5801), [#5804](https://github.com/Scottcjn/Rustchain/pull/5804), [#5806](https://github.com/Scottcjn/Rustchain/pull/5806), [#5807](https://github.com/Scottcjn/Rustchain/pull/5807), [#5809](https://github.com/Scottcjn/Rustchain/pull/5809), [#5810](https://github.com/Scottcjn/Rustchain/pull/5810), [#5812](https://github.com/Scottcjn/Rustchain/pull/5812), [#5813](https://github.com/Scottcjn/Rustchain/pull/5813), [#5815](https://github.com/Scottcjn/Rustchain/pull/5815), [#5817](https://github.com/Scottcjn/Rustchain/pull/5817), [#5819](https://github.com/Scottcjn/Rustchain/pull/5819), [#5820](https://github.com/Scottcjn/Rustchain/pull/5820), [#5821](https://github.com/Scottcjn/Rustchain/pull/5821), [#5822](https://github.com/Scottcjn/Rustchain/pull/5822), [#5823](https://github.com/Scottcjn/Rustchain/pull/5823), [#5824](https://github.com/Scottcjn/Rustchain/pull/5824), [#5825](https://github.com/Scottcjn/Rustchain/pull/5825), [#5827](https://github.com/Scottcjn/Rustchain/pull/5827), [#5828](https://github.com/Scottcjn/Rustchain/pull/5828), [#5829](https://github.com/Scottcjn/Rustchain/pull/5829), [#5831](https://github.com/Scottcjn/Rustchain/pull/5831), [#5833](https://github.com/Scottcjn/Rustchain/pull/5833), [#5834](https://github.com/Scottcjn/Rustchain/pull/5834), [#5835](https://github.com/Scottcjn/Rustchain/pull/5835), [#5839](https://github.com/Scottcjn/Rustchain/pull/5839), [#5845](https://github.com/Scottcjn/Rustchain/pull/5845), [#5853](https://github.com/Scottcjn/Rustchain/pull/5853), [#5854](https://github.com/Scottcjn/Rustchain/pull/5854), [#5855](https://github.com/Scottcjn/Rustchain/pull/5855), [#5856](https://github.com/Scottcjn/Rustchain/pull/5856), [#5858](https://github.com/Scottcjn/Rustchain/pull/5858), [#5859](https://github.com/Scottcjn/Rustchain/pull/5859), [#5860](https://github.com/Scottcjn/Rustchain/pull/5860), [#5861](https://github.com/Scottcjn/Rustchain/pull/5861), [#5862](https://github.com/Scottcjn/Rustchain/pull/5862), [#5863](https://github.com/Scottcjn/Rustchain/pull/5863), [#5864](https://github.com/Scottcjn/Rustchain/pull/5864), [#5865](https://github.com/Scottcjn/Rustchain/pull/5865), [#5866](https://github.com/Scottcjn/Rustchain/pull/5866), [#5867](https://github.com/Scottcjn/Rustchain/pull/5867), [#5868](https://github.com/Scottcjn/Rustchain/pull/5868), [#5870](https://github.com/Scottcjn/Rustchain/pull/5870), [#5871](https://github.com/Scottcjn/Rustchain/pull/5871), [#5872](https://github.com/Scottcjn/Rustchain/pull/5872), [#5873](https://github.com/Scottcjn/Rustchain/pull/5873), [#5874](https://github.com/Scottcjn/Rustchain/pull/5874), [#5875](https://github.com/Scottcjn/Rustchain/pull/5875), [#5876](https://github.com/Scottcjn/Rustchain/pull/5876), [#5877](https://github.com/Scottcjn/Rustchain/pull/5877), [#5878](https://github.com/Scottcjn/Rustchain/pull/5878), [#5879](https://github.com/Scottcjn/Rustchain/pull/5879), [#5880](https://github.com/Scottcjn/Rustchain/pull/5880), [#5882](https://github.com/Scottcjn/Rustchain/pull/5882), [#5883](https://github.com/Scottcjn/Rustchain/pull/5883), [#5884](https://github.com/Scottcjn/Rustchain/pull/5884), [#5885](https://github.com/Scottcjn/Rustchain/pull/5885), [#5886](https://github.com/Scottcjn/Rustchain/pull/5886), [#5887](https://github.com/Scottcjn/Rustchain/pull/5887), [#5888](https://github.com/Scottcjn/Rustchain/pull/5888), [#5889](https://github.com/Scottcjn/Rustchain/pull/5889), [#5890](https://github.com/Scottcjn/Rustchain/pull/5890), [#5891](https://github.com/Scottcjn/Rustchain/pull/5891), [#5892](https://github.com/Scottcjn/Rustchain/pull/5892), [#5893](https://github.com/Scottcjn/Rustchain/pull/5893), [#5894](https://github.com/Scottcjn/Rustchain/pull/5894), [#5895](https://github.com/Scottcjn/Rustchain/pull/5895), [#5897](https://github.com/Scottcjn/Rustchain/pull/5897), [#5898](https://github.com/Scottcjn/Rustchain/pull/5898), [#5907](https://github.com/Scottcjn/Rustchain/pull/5907), [#5908](https://github.com/Scottcjn/Rustchain/pull/5908), [#5911](https://github.com/Scottcjn/Rustchain/pull/5911)

---

## Summary

- **Total reviews this session:** 110 (25 security + 85 standard)
- **Estimated reward:** ~727 RTC
- **Cumulative (both sessions):** 162 PR reviews
- **Wallet:** `RTC6d1f27d28961279f1034d9561c2403697eb55602`

---

## Session 3 — May 21 Morning (8 reviews)

### High-Value Security Reviews

| PR | Finding | Est. RTC |
|----|---------|----------|
| [#5702](https://github.com/Scottcjn/Rustchain/pull/5702) | Attestation validation BEFORE nonce consumption — prevents reward bypass via incomplete fingerprint | 15 |
| [#5696](https://github.com/Scottcjn/Rustchain/pull/5696) | UTXO dust threshold enforcement — prevents sub-dust spam outputs | 15 |
| [#5693](https://github.com/Scottcjn/Rustchain/pull/5693) | Beacon API type confusion hardening — bool bypass, NaN/Infinity rejection | 12 |
| [#5684](https://github.com/Scottcjn/Rustchain/pull/5684) | Server proxy upstream 5xx error redaction — prevents internal error disclosure | 12 |
| [#5677](https://github.com/Scottcjn/Rustchain/pull/5677) | GPU render DB error info-leak — str(e) replaced with generic message | 12 |
| [#5694](https://github.com/Scottcjn/Rustchain/pull/5694) | Wallet CLI keystore 0600 permissions + atomic write — prevents key theft | 12 |

**Session 3 High-Value Subtotal: ~78 RTC (6 reviews)**

### Standard Reviews

| PR | Finding | Est. RTC |
|----|---------|----------|
| [#5701](https://github.com/Scottcjn/Rustchain/pull/5701) | Fuzz runner console encoding fix — prevents UnicodeEncodeError on non-UTF-8 terminals | 3 |
| [#5896](https://github.com/Scottcjn/Rustchain/pull/5896) | Miner alerts row normalization — filters non-dict API responses for resilience | 3 |

**Session 3 Standard Subtotal: ~6 RTC (2 reviews)**

---

## Updated Grand Total

| Session | Reviews | Security/High | Standard | Est. RTC |
|---------|---------|-------------|----------|----------|
| Session 1 (May 20 AM) | 52 | 8 | 44 | ~340 |
| Session 2 (May 20 PM) | 110 | 25 | 85 | ~727 |
| Session 3 (May 21 AM) | 8 | 6 | 2 | ~84 |
| **Grand Total** | **170** | **39** | **131** | **~1151 RTC ≈ $115 USD** |


---

## Batch 2 — May 21 Mid-Morning (7 reviews)

### High-Value Security Reviews

| PR | Finding | Est. RTC |
|----|---------|----------|
| [#5754](https://github.com/Scottcjn/Rustchain/pull/5754) | EPOCH_COMMIT handler missing — plus voter list not filtered by vote type + STATE sync unverified epoch import | 20 |
| [#5753](https://github.com/Scottcjn/Rustchain/pull/5753) | award_rtc wallet parser: format validation, ambiguous wallet detection, username fallback removed | 15 |
| [#5714](https://github.com/Scottcjn/Rustchain/pull/5714) | P2P gossip payload bounds: 64KB/256keys/16depth/4KB string limits BEFORE signature work | 15 |
| [#5721](https://github.com/Scottcjn/Rustchain/pull/5721) | Linux miner fingerprint: virtual interface/MAC filtering, fingerprint normalization | 10 |
| [#5703](https://github.com/Scottcjn/Rustchain/pull/5703) | macOS miner MAC collection: networksetup parsing for stable hardware ports | 10 |

**Batch 2 High-Value Subtotal: ~70 RTC (5 reviews)**

### Standard Reviews

| PR | Finding | Est. RTC |
|----|---------|----------|
| [#5735](https://github.com/Scottcjn/Rustchain/pull/5735) | Chinese (Simplified) README translation (+318 lines) | 3 |
| [#5726](https://github.com/Scottcjn/Rustchain/pull/5726) | Complete live RustChain stats dashboard with auto-refresh | 3 |

**Batch 2 Standard Subtotal: ~6 RTC (2 reviews)**

---

## Updated Grand Total

| Session | Reviews | Security/High | Standard | Est. RTC |
|---------|---------|-------------|----------|----------|
| Session 1 (May 20 AM) | 52 | 8 | 44 | ~340 |
| Session 2 (May 20 PM) | 110 | 25 | 85 | ~727 |
| Session 3 (May 21 AM) | 8 | 6 | 2 | ~84 |
| Batch 2 (May 21 mid-AM) | 7 | 5 | 2 | ~76 |
| **Grand Total** | **177** | **44** | **133** | **~1227 RTC ≈ $123 USD** |
