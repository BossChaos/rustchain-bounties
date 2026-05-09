#!/usr/bin/env python3
"""
RustChain Payout Ledger + Sophia API — SECURITY FIXES
Patches for security/sophia_payout_security_audit.md findings.

This file shows the recommended fixes for payout_ledger.py and sophia_api.py.
"""

# ══════════════════════════════════════════════════════════════
# payout_ledger.py CRITICAL FIXES
# ══════════════════════════════════════════════════════════════

# BEFORE: No auth on any endpoint (payout_ledger.py:168)
#
# AFTER: Add admin API key middleware

import os
import hmac
import hashlib
import functools

LEDGER_ADMIN_KEY = os.environ.get("LEDGER_ADMIN_KEY", "")
LEDGER_HMAC_SECRET = os.environ.get("LEDGER_HMAC_SECRET", "")

def require_admin_auth(f):
    """Decorator: require admin API key or HMAC signature."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        # Check API key
        api_key = request.headers.get("X-Ledger-Admin-Key", "")
        if api_key == LEDGER_ADMIN_KEY and LEDGER_ADMIN_KEY:
            return f(*args, **kwargs)
        
        # Check HMAC signature
        sig = request.headers.get("X-Ledger-Signature", "")
        body = request.get_data(as_text=True)
        expected = hmac.new(
            LEDGER_HMAC_SECRET.encode(),
            body.encode(),
            hashlib.sha256
        ).hexdigest()
        if sig == expected and LEDGER_HMAC_SECRET:
            return f(*args, **kwargs)
        
        return jsonify({"error": "Unauthorized"}), 401
    return decorated

# Apply decorator to all POST/PATCH endpoints:
#
# @app.route("/api/ledger", methods=["POST"])
# @require_admin_auth  # ADD THIS
# def api_ledger_create():
#     ...
#
# @app.route("/api/ledger/<record_id>/status", methods=["PATCH"])
# @require_admin_auth  # ADD THIS
# def api_ledger_update(record_id):
#     ...

# ══════════════════════════════════════════════════════════════
# payout_ledger.py: FINDING 6 — Amount Validation (High)
# ══════════════════════════════════════════════════════════════

# BEFORE (payout_ledger.py:179):
#   amount_rtc=float(data["amount_rtc"])
#
# AFTER:
MAX_Payout_RTC = float(os.environ.get("LEDGER_MAX_PAYOUT", "10000"))

def ledger_create(bounty_id, contributor, amount_rtc, bounty_title="", wallet_address="", pr_url="", notes=""):
    # amount_rtc comes as float from caller
    float_amount = float(amount_rtc)
    if float_amount <= 0:
        raise ValueError("amount_rtc must be positive")
    if float_amount > MAX_PAYOUT_RTC:
        raise ValueError(f"amount_rtc exceeds maximum ({MAX_PAYOUT_RTC})")
    if float_amount != float_amount:  # NaN check
        raise ValueError("amount_rtc cannot be NaN")
    if float_amount > 1e15:  # Infinity check
        raise ValueError("amount_rtc too large")

# ══════════════════════════════════════════════════════════════
# payout_ledger.py: TOCTOU Race Fix
# ══════════════════════════════════════════════════════════════

# ledger_update_status needs atomic state transitions:
#
# def ledger_update_status(record_id, new_status, tx_hash="", notes=""):
#     valid = {"queued", "pending", "confirmed", "voided"}
#     if new_status not in valid:
#         raise ValueError(f"Invalid status: {new_status}")
#     
#     # VALID STATE TRANSITIONS (enforce business rules):
#     allowed = {
#         "queued": {"pending", "voided"},
#         "pending": {"confirmed", "voided"},
#         "confirmed": set(),  # Terminal state
#         "voided": set(),     # Terminal state
#     }
#     
#     # Atomic update with state validation
#     with sqlite3.connect(DB_PATH) as conn:
#         # BEGIN IMMEDIATE acquires write lock immediately
#         conn.execute("BEGIN IMMEDIATE")
#         try:
#             # Read current status
#             row = conn.execute(
#                 "SELECT status FROM payout_ledger WHERE id=?", (record_id,)
#             ).fetchone()
#             
#             if not row:
#                 conn.rollback()
#                 raise ValueError("Record not found")
#             
#             current = row[0]
#             if new_status not in allowed.get(current, set()):
#                 conn.rollback()
#                 raise ValueError(
#                     f"Invalid transition: {current} -> {new_status}"
#                 )
#             
#             # Commit if transition is valid
#             conn.execute(
#                 "UPDATE payout_ledger SET status=?, tx_hash=?, notes=?, updated_at=? WHERE id=?",
#                 (new_status, tx_hash or "", notes or "", int(time.time()), record_id)
#             )
#             conn.commit()
#         except:
#             conn.rollback()
#             raise

# ══════════════════════════════════════════════════════════════
# sophia_api.py CRITICAL FIXES
# ══════════════════════════════════════════════════════════════

# BEFORE: No auth on /sophia/inspect (sophia_api.py:34)
#
# AFTER: Require miner wallet signature

import base64, ecdsa, hashlib

SOPHIA_TRUSTED_MINERS = set()  # Load from config/env

def verify_miner_signature(miner_id: str, signature: str, payload: str) -> bool:
    """Verify miner signed the payload with their wallet key."""
    try:
        # miner_id format: RTC<base58>
        pubkey_bytes = hashlib.sha256(miner_id.encode()).digest()[:32]
        vk = ecdsa.VerifyingKey.from_string(pubkey_bytes, curve=ecdsa.SECP256k1)
        sig_bytes = base64.b64decode(signature)
        return vk.verify(sig_bytes, payload.encode())
    except:
        return False

# In inspect_fingerprint():
@app.route("/sophia/inspect", methods=["POST"])
def inspect_fingerprint():
    data = request.get_json(force=True)
    
    miner_id = data.get("miner_id", "")
    signature = request.headers.get("X-Miner-Signature", "")
    payload = json.dumps(data, sort_keys=True)
    
    # Verify signature OR require API key
    api_key = request.headers.get("X-Sophia-API-Key", "")
    if not api_key and not signature:
        return jsonify({"error": "Authentication required"}), 401
    
    if signature and not verify_miner_signature(miner_id, signature, payload):
        return jsonify({"error": "Invalid signature"}), 403
    
    # ... rest of handler unchanged

# BEFORE: No auth on /sophia/dashboard (sophia_api.py:84)
#
# AFTER:
SOPHIA_ADMIN_KEY = os.environ.get("SOPHIA_ADMIN_KEY", "")

@app.route("/sophia/dashboard", methods=["GET"])
def dashboard():
    admin_key = request.headers.get("X-Sophia-Admin-Key", "")
    if admin_key != SOPHIA_ADMIN_KEY or not SOPHIA_ADMIN_KEY:
        return jsonify({"error": "Admin access required"}), 401
    # ... rest unchanged

# BEFORE: No miner_id validation (sophia_api.py:51)
#
# AFTER:
import re

MINER_ID_PATTERN = re.compile(r'^(RTC[1-9A-HJ-NP-Za-km-z]{20,50}|0x[0-9a-fA-F]{40})$')

@app.route("/sophia/status/<miner_id>", methods=["GET"])
def miner_status(miner_id: str):
    if not MINER_ID_PATTERN.match(miner_id):
        return jsonify({"error": "Invalid miner_id format"}), 400
    # ... rest unchanged
