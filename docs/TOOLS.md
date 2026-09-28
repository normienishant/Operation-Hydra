# 🧰 Tool Catalog — usage commands & justification

Every tool below is free/open or has a free tier, and is standard in phishing/malware/fraud
triage. For each: what it does, the exact command used (or emulated offline by this repo),
and why it earns its place.

## 1. MXToolbox — e-mail header analysis

- **Purpose:** paste raw headers → SPF/DKIM/DMARC verdicts, Received-chain, blacklist hits.
- **Live command:** paste `evidence/phishing/hydra01.eml` headers into
  `https://mxtoolbox.com/EmailHeaders.aspx`; or
  `curl "https://mxtoolbox.com/api/v2/lookup/emailheaders/{base64-header}" -H "Authorization:1"`
- **Offline equivalent:** `python analysis/scripts/analyze_headers.py`
- **Justification:** the de-facto first step; proves the spoof (From↔Return-Path mismatch,
  SPF hard-fail, DMARC p=none) in one view.

## 2. dig / nslookup — DNS authentication records

- **Live command:**

  ```bash
  dig TXT auroralogistics.in +short
  dig TXT _dmarc.auroralogistics.in +short
  dig TXT aurora-hrportal.net +short
  ```

- **Justification:** independently verifies the gateway's SPF/DMARC verdicts and exposes the
  attacker's `+all` anything-goes policy on the clone domain.

## 3. WHOIS / RDAP — domain intelligence

- **Live command:** `whois aurora-hrportal.net` or `curl https://rdap.org/domain/aurora-hrportal.net`
- **Offline equivalent:** `python analysis/scripts/whois_lookup.py` (offline db:
  `evidence/tool_outputs/whois_records.json`)
- **Justification:** 6- and 9-day domain ages + privacy proxies are the strongest
  pre-click spoofing signal; corroborates intent.

## 4. AbuseIPDB — IP reputation

- **Live command:**

  ```bash
  curl -s -H "Key: $ABUSEIPDB_KEY" -H "Accept: application/json" \
    "https://api.abuseipdb.com/api/v2/check?ipAddress=45.142.213.107&maxAgeInDays=90"
  ```

- **Offline equivalent:** `python analysis/scripts/ip_trace.py`
- **Justification:** abuse-confidence scores turn "an IP" into "an actionable indicator";
  the 90-day report categories characterise each hop's role.

## 5. VirusTotal — file/URL multi-engine verdict

- **Live command:** `vt url "aurora-hrportal.net/login"`; `vt file <sha256>` (VT CLI)
- **Offline equivalent:** simulated verdict tables in `evidence/tool_outputs/virustotal_verdict.md`
- **Justification:** multi-engine consensus detects what a single AV misses; behaviour-tab
  summaries pre-correlate sandbox findings.

## 6. CyberChef — payload decoding

- **Live command:** load recipe `From_Base64 → XOR {Key: 0x5A}` in the CyberChef web UI on
  `specimen.hydra.json → dropper.encoded_payload_b64`.
- **Offline equivalent:** `python analysis/scripts/malware_decoder.py`
- **Justification:** instant, local, no-upload decoding of base64/XOR stage payloads —
  crucial when a specimen must not leave the lab.

## 7. Wireshark — C2 traffic inspection

- **Live command (sandbox only):** capture filter `host 185.220.101.47`, display filter
  `tls.handshake.type == 1` → read JA3 mimic; statistics → conversations for beacon period.
- **Justification:** proves the TLS beacon cadence (T+120s SLEEP 1800) claimed in the log.

## 8. Python standard library (this repo's scripts)

- **Commands:** see `docs/SETUP.md` — the six analysis scripts.
- **Justification:** reproducibility + zero cost; every "tool output" in the repo is
  regenerable with one command, and CI proves it on every push.

## 9. markdownlint-cli2 — documentation hygiene (CI)

- **Live command:** `npx markdownlint-cli2 "**/*.md" "#node_modules"`
- **Justification:** the deliverable is documentation; linting keeps it reviewable
  (workflow: `.github/workflows/markdown-lint.yml`).
