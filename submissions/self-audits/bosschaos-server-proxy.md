# Self-Audit: node/server_proxy.py

## Wallet
4TRdrSRZvShfgxhiXjBDFaaySzbK2rH3VijoTBGWpEcL

## Module reviewed
- Path: `node/server_proxy.py`
- Commit: `e0c23ff`
- Lines reviewed: 1–72 (whole file)

## Deliverable: 3 specific findings

### 1. Query parameters are silently dropped on forwarded requests
- Severity: **medium**
- Location: `node/server_proxy.py:19` (GET) and `node/server_proxy.py:25-30` (POST)
- Description: Neither the GET nor POST forwarding path includes `params=request.args` or equivalent. If a client calls `GET /api/mine?wallet=abc&nonce=42`, the proxy constructs `url = f"{LOCAL_SERVER}/api/{path}"` where `path` only captures the URL path segment — the query string `?wallet=abc&nonce=42` is lost entirely. The upstream server at 8088 receives the request with no query parameters, causing incorrect behavior for any endpoint that relies on them.
- Reproduction: Send `curl 'http://localhost:8089/api/stats?detail=true'` and observe that the upstream `http://localhost:8088/api/stats` receives no `detail` query parameter. With Flask's `request.args` being ignored, all query-string-driven filtering is broken.

### 2. Response headers from upstream are completely stripped
- Severity: **medium**
- Location: `node/server_proxy.py:38-46`
- Description: When returning the proxied response, only `response.text` (or `response.json()`) and `response.status_code` are forwarded. All upstream response headers — including `Content-Type`, `Set-Cookie`, `Cache-Control`, `X-RateLimit-Remaining`, CORS headers (`Access-Control-*`), and authentication tokens — are discarded. If the upstream server sets session cookies or CORS headers, the client will never receive them. The only header that survives is whatever Flask auto-generates for the response object.
- Reproduction: Have the upstream server at 8088 respond with a `Set-Cookie: session=xyz` header; a client hitting port 8089 will not receive any `Set-Cookie` header in the response.

### 3. No authentication or access control on the proxy endpoint
- Severity: **low**
- Location: `node/server_proxy.py:16-51`
- Description: The proxy accepts any request on `/api/<path>` without authentication, rate limiting, or IP allowlisting. Since it binds to `0.0.0.0:8089` (line 72), it is reachable on all network interfaces. Any external party who discovers the port can use the proxy as an open relay to the local server on 8088, potentially bypassing firewall rules that were intended to restrict access to 8088 to localhost only. If the upstream server assumes it is only receiving requests from localhost (and therefore trusts them), this proxy effectively exposes those trusted endpoints to the network.
- Reproduction: From any machine with network access to port 8089, send `curl http://target:8089/api/mine` with arbitrary payloads — the proxy will forward them to the upstream server without any credential check.

## Known failures of this audit
- I did **not** test the proxy live against a running upstream server. The analysis is static — I reviewed the source code and traced the request/response flow mentally. I did not verify whether the upstream server at 8088 actually uses query parameters or sets meaningful response headers.
- I did **not** check whether there is an external firewall or iptables rule blocking port 8089 from external access, which would mitigate finding 3.
- I did **not** examine the broader Rustchain architecture to determine whether the proxy is intended to be internet-facing or internal-only.

## Confidence
- Overall confidence: 0.78
- Per-finding confidence:
  - Finding 1 (query params dropped): 0.95
  - Finding 2 (response headers stripped): 0.90
  - Finding 3 (no authentication): 0.65

## What I would test next
- Start the proxy and upstream server, then send requests with query parameters and verify they are lost upstream using a packet capture or upstream access log.
- Check upstream response headers with `curl -v` to confirm that headers like `Set-Cookie` or `Cache-Control` are not relayed to the client.
- Review the server's deployment configuration (Docker compose, systemd unit, iptables rules) to determine whether port 8089 is externally accessible or firewalled.
