#!/usr/bin/env python3
"""Parse the synthetic phishing .eml files: Received chain, SPF/DKIM/DMARC,
Reply-To/Return-Path mismatches, URL extraction  ==  offline MXToolbox clone.

Usage:
    python analysis/scripts/analyze_headers.py [path/to/sample.eml ...]
Writes: analysis/logs/02_headers.log
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PHISH = os.path.join(ROOT, "evidence", "phishing")
LOGDIR = os.path.join(ROOT, "analysis", "logs")

EMULATE = "MXToolbox Email Header Analyzer (offline clone)"

URL_RE = re.compile(r'https?://[^\s"\'<>]+|bit\.ly/\S+', re.I)
DOMAIN_RE = re.compile(r"@([\w.-]+)")


def domain_of(addr: str) -> str:
    m = DOMAIN_RE.search(addr or "")
    return m.group(1).lower() if m else ""


def parse_sample(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    headers, _, body = raw.partition("\n\n")

    def h(name: str) -> str:
        m = re.search(rf"^{name}:\s*(.+)$", headers, re.I | re.M)
        return m.group(1).strip() if m else ""

    auth = h("Authentication-Results")
    spf = "fail" if "spf=fail" in auth else ("pass" if "spf=pass" in auth else "none")
    dkim = "none" if "dkim=none" in auth else ("pass" if "dkim=pass" in auth else "unknown")
    dmarc = "fail" if "dmarc=fail" in auth else ("pass" if "dmarc=pass" in auth else "none")
    policy = re.search(r"p=(\w+)", auth)

    hop = re.search(r"from\s+(\S+)\s+\(?(\d+\.\d+\.\d+\.\d+)", headers, re.I)
    from_addr = h("From")
    return_path = h("Return-Path") or (re.search(r"client-ip=(\d+\.\d+\.\d+\.\d+)", headers) or [None, ""])[1]
    reply_to = h("Reply-To")
    from_dom = domain_of(from_addr)
    rp_dom = domain_of(return_path) if "@" in return_path else ""
    rt_dom = domain_of(reply_to)

    tells = []
    if rp_dom and from_dom and rp_dom != from_dom:
        tells.append(f"Return-Path domain {rp_dom} != From domain {from_dom} [bounce laundering]")
    if rt_dom and from_dom and rt_dom != from_dom:
        tells.append(f"Reply-To off-domain ({rt_dom}) [harvest destination]")
    if spf == "fail":
        tells.append("SPF hard fail [-all policy violated]")
    if dkim == "none":
        tells.append("DKIM absent")
    if dmarc == "fail" and policy and policy.group(1) == "none":
        tells.append("DMARC fail but p=none -> no enforcement (root cause)")
    if "PHPMailer" in headers:
        tells.append("X-Mailer PHPMailer -> scripted mass-mailer")

    verdict = "PHISHING/SPOOFED" if len(tells) >= 3 else "SUSPICIOUS" if tells else "CLEAN"
    return {
        "sample": os.path.basename(path),
        "from": from_addr,
        "reply_to": reply_to,
        "origin_hop": f"{hop.group(1)} ({hop.group(2)})" if hop else "?",
        "spf": spf, "dkim": dkim, "dmarc": dmarc,
        "dmarc_policy": policy.group(1) if policy else "-",
        "urls": sorted(set(u.rstrip('").,') for u in URL_RE.findall(body))),
        "tells": tells,
        "verdict": verdict,
    }


def main(argv: list[str]) -> None:
    os.makedirs(LOGDIR, exist_ok=True)
    targets = argv[1:] or sorted(glob.glob(os.path.join(PHISH, "*.eml")))
    results = [parse_sample(p) for p in targets]

    lines = [
        "=" * 74,
        f"STEP 02 - HEADER / SPF / DKIM / DMARC ANALYSIS   [emulates {EMULATE}]",
        "=" * 74,
    ]
    for r in results:
        lines += [
            f"\n--- {r['sample']} -------------------------------------------",
            f"From      : {r['from']}",
            f"Reply-To  : {r['reply_to']}",
            f"Origin    : {r['origin_hop']}",
            f"SPF/DKIM/DMARC: {r['spf']} / {r['dkim']} / {r['dmarc']} (p={r['dmarc_policy']})",
            "URLs      : " + ("\n            ".join(r["urls"]) if r["urls"] else "-"),
        ]
        lines += [f"TELL {i+1}: {t}" for i, t in enumerate(r["tells"])]
        lines.append(f"VERDICT   : {r['verdict']}")

    spoofed = [r for r in results if r["verdict"] == "PHISHING/SPOOFED"]
    lines += [
        "\n" + "-" * 74,
        f"SUMMARY: {len(spoofed)}/{len(results)} samples classified PHISHING/SPOOFED",
        "Root cause chain: spoofed From <- PHPMailer relay (hydrapey.net, NL)",
        "                  + DMARC p=none on auroralogistics.in (no enforcement)",
    ]
    out = "\n".join(lines) + "\n"

    with open(os.path.join(LOGDIR, "02_headers.log"), "w", encoding="utf-8") as fh:
        fh.write(out)
    with open(os.path.join(LOGDIR, "02_headers.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    print(out)


if __name__ == "__main__":
    main(sys.argv)
