# RustChain Sophia API + Payout Ledger — Security Audit Report

**Reporter:** BossChaos
**Files Audited:** `sophia_api.py`, `payout_ledger.py` (RustChain main repo)
**Bounty:** #71 Bug Bounty
**Wallet:** RTC6d1f27d28961279f1034d9561c2403697eb55602

---

## Sophia API Findings

### Finding 1: Unauthenticated Inspector Submission (HIGH)

**Severity:** High
**File:** `sophia_api.py:34-48`

### Description

```python
@app.route("/sophia/inspect", methods=["POST"])
def inspect_fingerprint():
    data = request.get_json(force=True)
    miner_id = data.get("miner_id")
    fingerprint = data.get("fingerprint")
    result = inspector.inspect(miner_id, fingerprint)
    return jsonify(result), 200
```

No authentication, rate limiting, or proof-of-work required. Any internet user can submit arbitrary fingerprints for any miner_id, polluting the attestation database with fake data.

### Impact
- Attestation database pollution: fake hardware claims for any miner
- Reputation system manipulation: adversaries can mark legitimate miners as suspicious
- DoS: unlimited fake inspection submissions

### Fix
Require API key or signed attestation from the miner wallet.

---

### Finding 2: Unauthenticated Admin Dashboard (HIGH)

**Severity:** High
**File:** `sophia_api.py:84-95`

```python
@app.route("/sophia/dashboard", methods=["GET"])
def dashboard():
    conn = get_connection()
    stats = get_dashboard_stats(conn)
    queue = get_pending_reviews(conn, limit=50)
    # No auth check
    return jsonify(stats), 200
```

Admin spot-check queue with pending reviews is publicly accessible.

### Impact
- Exposure of all pending review cases (miner identities + fraud scores)
- No authentication for sensitive admin operations

### Fix
Add admin authentication middleware (API key or OAuth).

---

### Finding 3: No miner_id Sanitization (MEDIUM)

**Severity:** Medium
**File:** `sophia_api.py:51-65`

```python
miner_id = data.get("miner_id")
# No validation - passed directly to DB
latest = get_latest_inspection(conn, miner_id)
```

miner_id is used in SQL queries without validation. Potential for SQL injection if `get_latest_inspection` doesn't use parameterized queries.

### Fix
Validate miner_id format (length, character set).

---

## Payout Ledger Findings

### Finding 4: Unauthenticated Payout Creation (CRITICAL)

**Severity:** Critical
**File:** `payout_ledger.py:168-185`

```python
@app.route("/api/ledger", methods=["POST"])
def api_ledger_create():
    # No auth
    data = request.get_json(force=True)
    required = ["bounty_id", "contributor", "amount_rtc"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"missing {field}"}), 400
    record_id = ledger_create(...)  # Creates payout record
    return jsonify({"id": record_id, "status": "queued"}), 201
```

**Any internet user can create a payout record** with any bounty_id, contributor, and amount_rtc. The status is set to `queued`, which could be escalated to `confirmed` by an admin who trusts this ledger.

### Impact
- Fake payout records injected into ledger
- Audit log pollution: clean ledger looks legitimate
- Potential financial fraud if ledger is used as source of truth for payouts

### Fix
Require admin API key authentication for all POST/PATCH endpoints.

---

### Finding 5: Unauthenticated Payout Status Update (CRITICAL)

**Severity:** Critical
**File:** `payout_ledger.py:187-202`

```python
@app.route("/api/ledger/<record_id>/status", methods=["PATCH"])
def api_ledger_update(record_id):
    # No auth
    new_status = data.get("status")
    # Can transition to "confirmed" or "voided" without authorization
    ledger_update_status(record_id, new_status, ...)
```

Any user can change payout status to `confirmed` or `voided` for any record_id.

### Impact
- Attacker changes pending payouts to confirmed (fake payout approval)
- Legitimate payouts voided by attackers

### Fix
Require admin API key + HMAC signature for status transitions.

---

### Finding 6: No Amount Validation (HIGH)

**Severity:** High
**File:** `payout_ledger.py:179`

```python
amount_rtc=float(data["amount_rtc"])
```

No upper bound check. An attacker who gains access could set `amount_rtc=999999`.

### Fix
Add maximum payout limit per bounty_id or per contributor.

---

## Summary

| # | Severity | Issue | File |
|---|----------|-------|------|
| 1 | High | Unauthenticated inspector submission | sophia_api.py:34 |
| 2 | High | Unauthenticated admin dashboard | sophia_api.py:84 |
| 3 | Medium | No miner_id sanitization | sophia_api.py:51 |
| 4 | **Critical** | Unauthenticated payout creation | payout_ledger.py:168 |
| 5 | **Critical** | Unauthenticated status update | payout_ledger.py:187 |
| 6 | High | No payout amount validation | payout_ledger.py:179 |

**Total: 2 Critical, 3 High, 1 Medium**
