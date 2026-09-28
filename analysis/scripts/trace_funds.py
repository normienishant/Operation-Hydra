#!/usr/bin/env python3
"""Follow the money: link synthetic transactions -> mule accounts -> BTC wallet.

Usage:
    python analysis/scripts/trace_funds.py                # full ledger trace
    python analysis/scripts/trace_funds.py --burst        # only the 02:4x burst
Writes: analysis/logs/06_funds.log
"""
from __future__ import annotations

import argparse
import csv
import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CSV_PATH = os.path.join(ROOT, "evidence", "transactions", "hydra_transactions.csv")
LOGDIR = os.path.join(ROOT, "analysis", "logs")

EMULATE = "bank-PSU ledger analytics + manual chain analysis"

BTC_WALLET = "bc1qhydra9f2x7k04mule7qq0wv8nzx3a9c0dpeel7"
PEEL_CHAIN = [
    ("bc1q9x7hop1fake4addr5zz6789012345", 0.35, "T+3h"),
    ("bc1q9x7hop2fake4addr5zz6789012345", 0.34, "T+9h"),
    ("MIXER (endpoint deliberately undocumented)", 0.33, "T+26h"),
]

# Expected totals from the case brief - the tracer asserts these as invariants
EXPECT_CNP = 342900
EXPECT_UPI = 278580


def load() -> list[dict]:
    with open(CSV_PATH, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def inr(rows: list[dict]) -> int:
    return sum(int(r["amount_inr"]) for r in rows)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--burst", action="store_true", help="only the 02:41-02:47 burst")
    args = ap.parse_args()

    os.makedirs(LOGDIR, exist_ok=True)
    rows = load()

    cnp = [r for r in rows if r["channel"] == "CNP"]
    upi = [r for r in rows if r["channel"] == "PSP"]
    transfers = [r for r in rows if r["channel"] == "IMPS"]

    assert inr(cnp) == EXPECT_CNP, f"CNP total drift: {inr(cnp)}"
    assert inr(upi) == EXPECT_UPI, f"UPI total drift: {inr(upi)}"

    if args.burst:
        burst = [r for r in rows if r["date"] == "2026-03-15" and r["time"] < "02:48"]
        for r in burst:
            print(f"{r['txn_id']} {r['date']} {r['time']} {r['amount_inr']:>7} {r['counterparty']}")
        return

    mules = defaultdict(int)
    for r in transfers:
        key = r["counterparty"].split(":")[0]
        mules[key] += int(r["amount_inr"])

    lines = [
        "=" * 74,
        f"STEP 06 - FINANCIAL FRAUD TRACING   [emulates {EMULATE}]",
        "=" * 74,
        "",
        f"Dataset                : {os.path.relpath(CSV_PATH, ROOT)} ({len(rows)} rows)",
        f"Card-not-present (CNP) : {len(cnp):>3} txns  INR {inr(cnp):>9,}  (incl. 12 card-testing probes)",
        f"UPI collect-request    : {len(upi):>3} txns  INR {inr(upi):>9,}",
        f"Mule transfers (IMPS)  : {len(transfers):>3} txns  INR {inr(transfers):>9,} (layering legs)",
        "",
        "TEMPORAL FINGERPRINT",
        "------------------------------------------------",
        "  15 Mar 10:00-12:00  12 probes  INR 101-500 each      (card testing)",
        "  15 Mar 02:41-02:49   9 CNP     INR 41k-49,999 each   (burst - SOC alert)",
        "  15 Mar 02:47-03:20  11 CNP     INR 12k-24k           (post-alert throttle)",
        "  15 Mar 03:20-04:00  13 UPI     INR 500-49,999        (collect-request approvals)",
        "  16 Mar 09:00-17:00   8 IMPS    layering to 4 mules",
        "",
        "MULE LEDGER (from layering legs)",
        "------------------------------------------------",
    ]
    for m, amt in sorted(mules.items()):
        lines.append(f"  {m}: INR {amt:>9,}  ({mule_meta(m)})")

    lines += [
        "",
        "LEDGER TRACE  victims -> mules -> P2P desk -> BTC",
        "------------------------------------------------",
        f"  {len(cnp)} CNP + {len(upi)} UPI victim transactions  INR {inr(cnp) + inr(upi):,}",
        f"  -> MULE-1..4 receive                  INR {sum(mules.values()):>9,} (incl. repeat legs)",
        f"  -> consolidated to MULE-3             INR   5,21,480",
        "  -> P2P crypto desk (simulated) 2 trades",
        f"  -> BTC {BTC_WALLET}  0.71 BTC",
        "",
        "PEEL CHAIN (simulated)",
        "------------------------------------------------",
    ]
    for addr, amt, when in PEEL_CHAIN:
        lines.append(f"  {when:<6} {amt:>5} BTC -> {addr}")

    lines += [
        "",
        "RECOVERY OUTLOOK",
        "------------------------------------------------",
        "  Frozen (MULE-1 + MULE-4, T+1)        INR   2,04,000  (33%)",
        "  Dissipated (ATM cash-out + mixer)    INR   4,17,480  (67%)",
        "",
        "LEGAL HOOKS",
        "------------------------------------------------",
        "  Card/UPI fraud        : IT Act S.66C/66D + BNS S.318(4)",
        "  Mule holders          : BNS S.316(2) CBT; PMLA S.3 layering",
        "  P2P desk              : PMLA S.3; US 18 U.S.C. S.1960 analogue",
        "  Freezing              : PMLA S.5; BNSS S.106 seizure",
    ]
    out = "\n".join(lines) + "\n"
    with open(os.path.join(LOGDIR, "06_funds.log"), "w", encoding="utf-8") as fh:
        fh.write(out)
    print(out)


def mule_meta(m: str) -> str:
    meta = {
        "MULE-1": "HDFC ****4412 Rakesh V. - pass-through within 11 min",
        "MULE-2": "ICICI ****8830 Sana K. - 7 ATM withdrawals / 40 min",
        "MULE-3": "Paytm ****2170 Dummy Traders LLP - shell entity",
        "MULE-4": "SBI ****7791 Imran S. - account opened 3 days pre-attack",
    }
    return meta.get(m, "?")


if __name__ == "__main__":
    main()

