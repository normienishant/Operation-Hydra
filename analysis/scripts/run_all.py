#!/usr/bin/env python3
"""Orchestrator: run the full Operation Hydra analysis suite.

Runs the steps in dependency order and writes every log the docs reference:

    01  generate_phishing.py      -> evidence/phishing/*.eml
    02  analyze_headers.py        -> analysis/logs/02_headers.log
    03  ip_trace.py               -> analysis/logs/03_iptrace.log
    04  whois_lookup.py           -> analysis/logs/04_whois.log
    05  malware_decoder.py        -> analysis/logs/05_malware.log + iocs.json
    06  generate_transactions.py  -> evidence/transactions/*.csv
    07  trace_funds.py            -> analysis/logs/06_funds.log

Usage: python analysis/scripts/run_all.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

STEPS = [
    ("01", "generate_phishing.py", "rebuild synthetic .eml corpus"),
    ("02", "analyze_headers.py", "header / SPF / DKIM / DMARC analysis"),
    ("03", "ip_trace.py", "IP trace & abuse scoring"),
    ("04", "whois_lookup.py", "WHOIS domain intelligence"),
    ("05", "malware_decoder.py", "payload decode & classification"),
    ("06", "generate_transactions.py", "rebuild synthetic transaction ledger"),
    ("07", "trace_funds.py", "money-flow tracing"),
]


def main() -> int:
    t0 = time.time()
    print("=" * 74)
    print("OPERATION HYDRA - full analysis suite (all artefacts synthetic)")
    print("=" * 74)
    for num, script, desc in STEPS:
        t = time.time()
        print(f"\n[{num}] {desc}  ({script})")
        print("-" * 74)
        proc = subprocess.run(
            [sys.executable, os.path.join(HERE, script)],
            check=False,
        )
        status = "OK" if proc.returncode == 0 else f"FAILED (rc={proc.returncode})"
        print(f"--- {status} in {time.time() - t:.2f}s")
        if proc.returncode != 0:
            return proc.returncode
    print("\n" + "=" * 74)
    print(f"ALL STEPS COMPLETED in {time.time() - t0:.2f}s")
    print("Logs -> analysis/logs/   IOCs -> evidence/malware/iocs.json")
    print("Next: python builder/build_report.py to emit the DOCX/PDF deliverable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
