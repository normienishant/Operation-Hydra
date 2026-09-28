#!/usr/bin/env python3
"""Trace and score the attacker IPs (offline AbuseIPDB-style emulation).

Usage:
    python analysis/scripts/ip_trace.py                # trace all case IPs
    python analysis/scripts/ip_trace.py --ip 1.2.3.4   # single IP
Writes: analysis/logs/03_iptrace.log
"""
from __future__ import annotations

import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
LOGDIR = os.path.join(ROOT, "analysis", "logs")

EMULATE = "AbuseIPDB /check API (offline clone)"

# Deterministic offline intel db (mirrors evidence/tool_outputs/abuseipdb_ipintel.md)
DB = {
    "45.142.213.107": {
        "rdns": "mail.hydrapey.net", "asn": "AS208475", "cc": "NL",
        "isp": "HydraNet Hosting B.V.", "score": 96, "reports": 311,
        "role": "phishing mail relay / bounce laundering",
    },
    "185.220.101.47": {
        "rdns": "tor-exit-47.hydrapey.net", "asn": "AS205100", "cc": "RO",
        "isp": "HydraTor Transit", "score": 88, "reports": 214,
        "role": "HydraRAT C2 + Tor exit (dual use)",
    },
    "103.87.12.90": {
        "rdns": "ns1.aurora-hrportal.net", "asn": "AS135318", "cc": "IN",
        "isp": "PuneHost Cloud", "score": 74, "reports": 96,
        "role": "clone-portal hosting (aurora-hrportal.net)",
    },
    "91.215.85.21": {
        "rdns": "cdn.auroralogistics-support.com", "asn": "AS204601", "cc": "UA",
        "isp": "DniproHost LLC", "score": 81, "reports": 142,
        "role": "kit CDN / MITM proxy endpoint",
    },
}

TOLERANCE = 60  # abuse score above which the IP is 'actionable'


def row(ip: str) -> list[str]:
    e = DB[ip]
    flag = "ACTIONABLE" if e["score"] >= TOLERANCE else "monitor"
    return [
        f"\nIP {ip}",
        f"  rDNS        : {e['rdns']}",
        f"  ASN/CC      : {e['asn']} / {e['cc']}   ISP: {e['isp']}",
        f"  Abuse score : {e['score']}/100   reports(90d): {e['reports']}   [{flag}]",
        f"  Case role   : {e['role']}",
    ]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ip", action="append", help="score a specific IP (repeatable)")
    args = ap.parse_args()

    os.makedirs(LOGDIR, exist_ok=True)
    targets = args.ip or list(DB)
    lines = [
        "=" * 74,
        f"STEP 03 - IP TRACE / ABUSE SCORING   [emulates {EMULATE}]",
        "=" * 74,
    ]
    for ip in targets:
        if ip in DB:
            lines += row(ip)
        else:
            lines.append(f"\nIP {ip}: not in offline case db - run live AbuseIPDB API for this one")

    hop_chain = [
        "HOP CHAIN (attacker traffic path):",
        "  victim browser -> 45.142.213.107 (phish relay, NL)",
        "  payload C2     -> 185.220.101.47:8443 (RAT C2, RO)",
        "  clone portal   -> 103.87.12.90 (IN) / 91.215.85.21 (UA)",
        "  mule banking   -> 103.87.12.0/24 device IPs (shared with clone host range!)",
    ]
    lines += [""] + hop_chain + [
        "",
        f"TOTAL: {len(targets)} IPs scored; "
        f"{sum(1 for t in targets if DB.get(t, {}).get('score', 0) >= TOLERANCE)} "
        f"actionable (score >= {TOLERANCE}).",
    ]
    out = "\n".join(lines) + "\n"
    with open(os.path.join(LOGDIR, "03_iptrace.log"), "w", encoding="utf-8") as fh:
        fh.write(out)
    with open(os.path.join(LOGDIR, "03_iptrace.json"), "w", encoding="utf-8") as fh:
        json.dump(DB, fh, indent=2)
    print(out)


if __name__ == "__main__":
    main()
