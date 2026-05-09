# RustChain Faucet — Security Audit Report

**Reporter:** BossChaos
**Files Audited:** `faucet.py` (RustChain main repo)
**Bounty:** #71 Bug Bounty
**Wallet:** RTC6d1f27d28961279f1034d9561c2403697eb55602

---

## Finding 1: IP Spoofing Bypass — Rate Limit Defeat (HIGH)

**Severity:** High
**File:** `faucet.py:45-51`
**CWE:** CWE-346 (Origin Validation Error)

### Description

The faucet relies on `request.remote_addr` for IP-based rate limiting. While `ProxyFix` is configured (`x_for=1`), it only trusts the `X-Forwarded-For` header from the first proxy hop. An attacker behind a NAT or VPN can trivially bypass rate limiting:

```python
# Any client can set this header:
curl -H "X-Forwarded-For: 1.2.3.4" https://faucet.rustchain.ai/faucet/drip
```

The faucet will record `1.2.3.4` as the IP address. Since `1.2.3.4` has never made a request, rate limiting is bypassed entirely. A single attacker can drain the faucet by rotating spoofed IPs.

### Impact
- Unbounded faucet drain — single attacker can obtain unlimited test RTC
- Legitimate users rate-limited while attackers extract tokens

### Fix
Validate `X-Forwarded-For` against a whitelist of known proxy IPs, or require CAPTCHA/bot protection before drip endpoint.

---

## Finding 2: No Wallet Address Validation (MEDIUM)

**Severity:** Medium
**File:** `faucet.py:316-317`

### Description

```python
if not wallet.startswith('0x') or len(wallet) < 10:
    return jsonify({'ok': False, 'error': 'Invalid wallet address'}), 400
```

The validation is trivially bypassed:
```python
wallet = "0x" + "A" * 9  # len=11, passes validation but invalid
```

Accepts any string starting with `0x` with length >= 10, with no checksum validation.

### Impact
- Invalid addresses recorded in database
- Could confuse accounting and block explorers

### Fix
Implement proper RTC address format validation (Bech32 or checksum depending on address type).

---

## Finding 3: SQLite Race Condition — Time-of-Check to Time-of-Use (MEDIUM)

**Severity:** Medium
**File:** `faucet.py:75-85, 103-112`

### Description

Between checking `can_drip()` and recording with `record_drip()`, there is no locking. Concurrent requests can pass rate limit checks simultaneously:

```python
# Thread A: can_drip(ip) -> True  (11:00:00)
# Thread B: can_drip(ip) -> True  (11:00:00)  <- same time window
# Thread A: record_drip(..., ip)  (11:00:00)
# Thread B: record_drip(..., ip)  (11:00:00)
```

SQLite's default isolation allows this TOCTOU race. An attacker with concurrent connections can drip multiple times within the same 24-hour window.

### Impact
- Rate limit bypassed via concurrent requests
- Increased faucet drain rate

### Fix
Use SQLite `BEGIN IMMEDIATE` transaction or add a unique constraint on (wallet, timestamp window) with retry logic.

---

## Finding 4: No Input Sanitization on Wallet Field (LOW)

**Severity:** Low
**File:** `faucet.py:313`

### Description

```python
wallet = data['wallet'].strip()
```

No length limit. A malicious client could submit extremely long strings, potentially causing:
- Log injection (if logged to file/stdout)
- UI rendering issues in admin dashboards
- Database storage waste

### Fix
Enforce maximum wallet string length (e.g., 64 characters).

---

## Finding 5: Hardcoded Rate Limit (LOW)

**Severity:** Low
**File:** `faucet.py:24-25`

```python
MAX_DRIP_AMOUNT = 0.5  # RTC
RATE_LIMIT_HOURS = 24
```

No environment variable override. Production deployments cannot adjust without code changes.

### Fix
Read from environment variables with defaults.

---

## Summary

| # | Severity | Issue | Status |
|---|----------|-------|--------|
| 1 | High | IP Spoofing — rate limit bypass via X-Forwarded-For | Requires fix |
| 2 | Medium | No wallet format validation | Requires fix |
| 3 | Medium | SQLite race condition TOCTOU | Requires fix |
| 4 | Low | No wallet input length limit | Enhancement |
| 5 | Low | Hardcoded rate limit | Enhancement |

**Total findings:** 1 High, 2 Medium, 2 Low
