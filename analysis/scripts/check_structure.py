#!/usr/bin/env python3
"""Directory-structure / deliverable check for Operation Hydra (used by CI).

Fails (exit 1) if any deliverable from the assignment brief is missing.
Usage: python analysis/scripts/check_structure.py
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

REQUIRED = [
    "README.md",
    "LICENSE",
    ".gitignore",
    ".markdownlint.yml",
    ".github/workflows/markdown-lint.yml",
    ".github/workflows/repo-check.yml",
    "docs/case_brief.md",
    "docs/cybercrime_mapping.md",
    "docs/phishing_investigation.md",
    "docs/malware_analysis.md",
    "docs/financial_fraud.md",
    "docs/impact_ethics_report.md",
    "docs/AUTHORSHIP_DECLARATION.md",
    "docs/SETUP.md",
    "docs/TOOLS.md",
    "docs/report",                      # deliverable DOCX/PDF land here
    "evidence/phishing/hydra01.eml",
    "evidence/phishing/hydra02.eml",
    "evidence/phishing/hydra03.eml",
    "evidence/phishing/hydra04.eml",
    "evidence/phishing/hydra05.eml",
    "evidence/malware/specimen.hydra.json",
    "evidence/malware/sample_logs.txt",
    "evidence/malware/iocs.json",       # generated
    "evidence/transactions/hydra_transactions.csv",
    "evidence/tool_outputs/mxtoolbox_header.md",
    "evidence/tool_outputs/virustotal_verdict.md",
    "evidence/tool_outputs/abuseipdb_ipintel.md",
    "evidence/tool_outputs/whois_records.json",
    "evidence/tool_outputs/screenshots/README.md",
    "analysis/scripts/generate_phishing.py",
    "analysis/scripts/analyze_headers.py",
    "analysis/scripts/ip_trace.py",
    "analysis/scripts/whois_lookup.py",
    "analysis/scripts/malware_decoder.py",
    "analysis/scripts/generate_transactions.py",
    "analysis/scripts/trace_funds.py",
    "analysis/scripts/run_all.py",
    "analysis/scripts/check_structure.py",
    "analysis/logs/02_headers.log",     # generated
    "analysis/logs/03_iptrace.log",
    "analysis/logs/04_whois.log",
    "analysis/logs/05_malware.log",
    "analysis/logs/06_funds.log",
    "builder/build_report.py",
]

GENERATED_HINT = (
    "\nSome listed files are generated. If missing locally run:\n"
    "  python analysis/scripts/run_all.py\n"
    "  python builder/build_report.py\n"
)


def main() -> int:
    missing = [rel for rel in REQUIRED if not os.path.exists(os.path.join(ROOT, rel))]
    if missing:
        print("MISSING DELIVERABLES:")
        for m in missing:
            print(f"  - {m}")
        print(GENERATED_HINT)
        return 1
    print(f"Structure OK: {len(REQUIRED)} required deliverables present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
