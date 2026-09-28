# MXToolbox Header Analyzer — simulated output (hydra01.eml)

> Real command: paste `evidence/phishing/hydra01.eml` headers into
> <https://mxtoolbox.com/EmailHeaders.aspx> — equivalent offline run:
> `python analysis/scripts/analyze_headers.py evidence/phishing/hydra01.eml`

```
DELIVERABILITY  FAIL
├─ SPF          fail (mechanism: -all; sender IP 45.142.213.107 not authorized for auroralogistics.in)
├─ DKIM         none (no signature present)
├─ DMARC        fail — policy p=none → no enforcement action taken
├─ From ↔ Return-Path mismatch   auroralogistics.in ≠ hydrapey.net   [SPOOF]
├─ Reply-To     hr.verify@aurora-hrportal.net (off-domain)            [SPOOF]
├─ X-Mailer     PHPMailer 6.8.0 (mass-mailer fingerprint)
└─ Received hop 1: mail.hydrapey.net (45.142.213.107, NL AS208475)   [origin]

MXTOOLBOX RISK SCORE: 9.4/10 (phishing)
Blacklist check (simulated): 45.142.213.107 on 14 of 104 DNSBLs
```

## Raw verdict JSON (as written to analysis/logs/02_headers.log)

```json
{"sample": "hydra01.eml", "spf": "fail", "dkim": "none", "dmarc": "fail",
 "from_domain": "auroralogistics.in", "return_path_domain": "hydrapey.net",
 "reply_to": "hr.verify@aurora-hrportal.net", "origin_ip": "45.142.213.107",
 "verdict": "PHISHING/SPOOFED"}
```
