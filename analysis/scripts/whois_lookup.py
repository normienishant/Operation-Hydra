#!/usr/bin/env python3
"""Offline WHOIS lookup for the Hydra campaign domains (registrar/age spoofing tells).

Usage:
    python analysis/scripts/whois_lookup.py                # all case domains
    python analysis/scripts/whois_lookup.py --domain x.tld # single domain
Writes: analysis/logs/04_whois.log
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
LOGDIR = os.path.join(ROOT, "analysis", "logs")
WHOIS_DB = os.path.join(ROOT, "evidence", "tool_outputs", "whois_records.json")

EMULATE = "whois CLI + registrar RDAP"


def load_db() -> dict:
    with open(WHOIS_DB, encoding="utf-8") as fh:
        return json.load(fh)


def fmt(rec: dict) -> list[str]:
    created = date.fromisoformat(rec["created"])
    age_days = (date(2026, 3, 16) - created).days
    lines = [
        f"\nDomain       : {rec['domain']}",
        f"  Created    : {rec['created']}   (age at attack: {rec['age_days_at_attack']} days / {age_days} days since)",
        f"  Registrar  : {rec['registrar']}",
        f"  Registrant : {rec['registrant_org']} ({rec['registrant_country']})",
        f"  Privacy    : {'YES - proxy registration' if rec['privacy_proxy'] else 'no'}",
        f"  Nameservers: {', '.join(rec['ns'])}",
        f"  Verdict    : {rec['verdict']}",
    ]
    if rec.get("red_flag"):
        lines.append(f"  RED FLAGS  : {rec['red_flag']}")
    return lines


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--domain", action="append", help="look up specific domain (repeatable)")
    args = ap.parse_args()

    os.makedirs(LOGDIR, exist_ok=True)
    db = load_db()
    by_domain = {r["domain"]: r for r in db["records"]}
    targets = args.domain or list(by_domain)

    lines = [
        "=" * 74,
        f"STEP 04 - WHOIS / DOMAIN INTELLIGENCE   [emulates {EMULATE}]",
        "=" * 74,
    ]
    for d in targets:
        rec = by_domain.get(d)
        if rec:
            lines += fmt(rec)
        else:
            lines.append(f"\nDomain {d}: not in offline case db - run `whois {d}` for live data")

    lines += [
        "",
        "RED-FLAG SUMMARY",
    ] + [f"  - {f}" for f in db["red_flags_summary"]] + [
        "",
        "RULE OF THUMB: domain age < 30 days + privacy proxy + brand token in name",
        "              => treat as hostile until proved otherwise (passive DNS next).",
    ]
    out = "\n".join(lines) + "\n"
    with open(os.path.join(LOGDIR, "04_whois.log"), "w", encoding="utf-8") as fh:
        fh.write(out)
    print(out)


if __name__ == "__main__":
    main()
