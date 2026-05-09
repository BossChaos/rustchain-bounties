# Security Audit: sophia_api.py + payout_ledger.py

**Reporter:** BossChaos
**Files Audited:** `sophia_api.py`, `payout_ledger.py` (RustChain main repo)
**Bounty:** #71 Bug Bounty
**Wallet:** RTC6d1f27d28961279f1034d9561c2403697eb55602

---

## Critical Findings

### C1: Unauthenticated Payout Creation — payout_ledger.py:168

```python
@app.route("/api/ledger", methods=["POST"])
def api_ledger_create():
    record_id = ledger_create(
        bounty_id=data.get("bounty_id"),
        contributor=data.get("contributor"),
        amount_rtc=float(data["amount_rtc"]),
        ...
    )
```

**Severity:** Critical

**Impact:** Any internet user can create fake payout records and set status to `queued`. No authentication, no API key check, no HMAC signature.

**Attack Scenario:** Attacker calls `POST /api/ledger` with arbitrary bounty_id, contributor, and amount. Ledger shows fake confirmed payouts. Real contributors are displaced from payment queue.

**Fix:** Add `@require_admin_auth` decorator. Require `X-Ledger-Admin-Key` header or HMAC signature.

---

### C2: Unauthenticated Status Update — payout_ledger.py:187

```python
@app.route("/api/ledger/<record_id>/status", methods=["PATCH"])
def api_ledger_update(record_id):
    new_status = data.get("status")
    ledger_update_status(record_id, new_status)
```

**Severity:** Critical

**Impact:** Any user can change any record's status to `confirmed` or `voided`. Can void legitimate payouts or mark fake ones as confirmed.

**Attack Scenario:** Attacker obtains record_id from public ledger page, then calls `PATCH /api/ledger/<id>/status` with `{"status":"voided"}`.

**Fix:** Add `@require_admin_auth`. Add state transition validation: `queued→pending→confirmed` only, `voided` as terminal.

---

## High Findings

### H1: Unauthenticated Inspector Submission — sophia_api.py:34

```python
@app.route("/sophia/inspect", methods=["POST"])
def inspect_fingerprint():
    data = request.get_json(force=True)
    miner_id = data.get("miner_id")
    result = sophia_inspect(miner_id, ...)
    sophia_save(result)
```

**Severity:** High

**Impact:** Anyone can submit fake inspector data, polluting the oracle with false records. Affects Sophia AI training quality and agent reputation scores.

**Fix:** Require miner wallet signature (`X-Miner-Signature` header) or API key.

---

### H2: Unauthenticated Admin Dashboard — sophia_api.py:84

```python
@app.route("/sophia/dashboard", methods=["GET"])
def dashboard():
    miners = get_all_miners()
    return render_template("sophia_dashboard.html", miners=miners)
```

**Severity:** High

**Impact:** Full miner database exposed without authentication. PII risk if miner_id maps to GitHub accounts or real identities.

**Fix:** Require `X-Sophia-Admin-Key` header.

---

### H3: No Payout Amount Upper Bound — payout_ledger.py:179

```python
amount_rtc = float(data["amount_rtc"])
```

**Severity:** High

**Impact:** Any amount accepted. Floats like `NaN`, negative values, and extremely large values propagate to `ledger_summary()`.

**Attack Scenario:** `POST /api/ledger` with `{"amount_rtc": "NaN"}` corrupts aggregate statistics.

**Fix:** Validate `amount_rtc > 0`, `amount_rtc < MAX_PAYOUT_RTC`, and `math.isfinite(amount_rtc)`.

---

## Medium Finding

### M1: Unvalidated miner_id — sophia_api.py:51

```python
@app.route("/sophia/status/<miner_id>", methods=["GET"])
def miner_status(miner_id: str):
    row = db_get("SELECT * FROM miners WHERE miner_id=?", (miner_id,))
```

**Severity:** Medium

**Impact:** Regex injection risk if miner_id is passed unsanitized to SQL. No format validation allows arbitrary strings.

**Fix:** Add `MINER_ID_PATTERN = re.compile(r'^(RTC[1-9A-HJ-NP-Za-km-z]{20,50}|0x[0-9a-fA-F]{40})$')`. Reject non-matching.

---

## Recommended Fixes

See `security/payout_sophia_fixes.py` for complete patch code.
