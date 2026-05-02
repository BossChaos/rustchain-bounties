# Self-Audit: bridge/bridge_api.py

## Wallet
4TRdrSRZvShfgxhiXjBDFaaySzbK2rH3VijoTBGWpEcL

## Module reviewed
- Path: `bridge/bridge_api.py`
- Commit: `5952103b1f5a4581f95668f7e36a92a3696b6e5a`
- Lines reviewed: 1–624 (whole file)

## Deliverable: 3 specific findings

### 1. Admin key comparison is vulnerable to timing attacks — `X-Admin-Key` can be leaked byte-by-byte
- Severity: **medium**
- Location: `bridge/bridge_api.py:169`
- Description: The `_require_admin` decorator compares the incoming `X-Admin-Key` header against `BRIDGE_ADMIN_KEY` using Python's standard `!=` operator (`if key != BRIDGE_ADMIN_KEY:`). This comparison is not constant-time — it short-circuits on the first mismatched character. An attacker who can measure response time differences can recover the admin key character by character, gaining full access to `/bridge/confirm` and `/bridge/release` endpoints. Once compromised, an attacker could confirm fraudulent locks and mint wRTC to their own wallet.
- Reproduction: Send repeated requests with admin keys sharing increasing-length prefixes (e.g. `a`, `ab`, `abc`...) and measure response latency. The correct prefix will consistently take microseconds longer to reject because the comparison iterates further before finding the mismatch.

### 2. Expired locks have no automatic refund mechanism — user funds can be permanently stuck
- Severity: **medium**
- Location: `bridge/bridge_api.py:44–52` (state definitions) and `bridge/bridge_api.py:419–432` (release endpoint expiry check)
- Description: Locks have a 24-hour expiry (`LOCK_EXPIRY_SECONDS = 86_400`), but there is no `/bridge/refund` endpoint, no background sweeper to auto-refund expired locks, and no state transition from `confirmed` or `pending` to `refunded`. If a lock reaches `confirmed` state but the admin fails to release it within 24 hours (e.g. admin is offline, or the target chain is congested), the `release` endpoint rejects it with "lock has expired" (line 431). However, the lock remains in the database in `confirmed` state with no way to transition it to `refunded` — the user's RTC is effectively burned with no recovery path.
- Reproduction: Create a lock, have it confirmed, then wait 24 hours (or mock `time.time()`). Attempt to release — it returns 410 "lock has expired". There is no endpoint to refund the lock, so it stays in `confirmed` forever.

### 3. No rate limiting on `/bridge/lock` — unauthenticated endpoint vulnerable to resource exhaustion DoS
- Severity: **medium**
- Location: `bridge/bridge_api.py:179–340` (`lock_rtc` function)
- Description: The `/bridge/lock` endpoint has no rate limiting, CAPTCHA, or request throttling. Each request writes to both `bridge_locks` and `bridge_events` tables and holds `_db_lock` (a threading.Lock) during the entire database transaction. An attacker can flood this endpoint with valid-looking requests (different tx_hash values), causing: (a) SQLite WAL growth and disk exhaustion, (b) thread starvation as all workers hold `_db_lock`, (c) event table bloat since every lock creates at least one event row. The endpoint validates inputs but does not throttle by sender_wallet, IP, or any identifier.
- Reproduction: Script a loop sending POST requests to `/bridge/lock` with unique tx_hash values; the `bridge_events` table grows linearly, disk usage increases, and legitimate lock requests experience contention on `_db_lock`.

## Known failures of this audit
- I did **not** test the HMAC receipt verification end-to-end with a real `BRIDGE_RECEIPT_SECRET` — my analysis is limited to the algorithmic correctness of `_verify_receipt_signature` and `_canonical_lock_receipt`.
- I did **not** evaluate the Solana/Base chain address validation for edge cases (e.g. valid base58 strings that are not actual Solana addresses, or checksummed vs non-checksummed Base addresses).
- I did **not** review the interaction between `bridge_api.py` and the on-chain Rust lock contract — the assumption that `tx_hash` corresponds to an actual on-chain lock transaction is not validated by this API.
- I did **not** run the Flask app under load to measure actual `_db_lock` contention or SQLite write throughput limits.

## Confidence
- Overall confidence: 0.80
- Per-finding confidence:
  - Finding 1 (timing attack on admin key): 0.92
  - Finding 2 (no refund for expired locks): 0.88
  - Finding 3 (no rate limiting on lock endpoint): 0.85

## What I would test next
- Replace `key != BRIDGE_ADMIN_KEY` with `hmac.compare_digest(key.encode(), BRIDGE_ADMIN_KEY.encode())` and verify the decorator still rejects invalid keys.
- Implement a `/bridge/refund/<lock_id>` admin endpoint that transitions expired `confirmed` locks to `refunded` state, with appropriate event logging.
- Add Flask-Limiter or a token-bucket rate limiter keyed on sender_wallet (authenticated users) and IP (unauthenticated), with a cap of e.g. 10 lock requests per minute per sender.
