#!/usr/bin/env python3
"""Generate the SYNTHETIC transaction dataset for the Operation Hydra case.

Assignment: Unit 2 - Types of Cyber Crimes (Assignment 2).
Output: evidence/transactions/hydra_transactions.csv
Every card, VPA and account is fictional (Luhn-valid dummies only).
"""
from __future__ import annotations

import csv
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "evidence", "transactions", "hydra_transactions.csv")

random.seed(20260314)  # deterministic build

VICTIM_CARDS = {
    "p.nair":     "4532 8812 4471 0036",
    "v.rao":      "5241 9034 7712 8840",
    "r.desai":    "4539 2210 6634 1201",
    "a.mehta":    "5412 7788 3310 9921",
    "s.iyer":     "4532 6604 1129 7716",
    "k.bose":     "5244 1109 8876 3316",
}

MULES = {
    "MULE-1": {"bank": "HDFC", "acct": "50100XXXXXX4412", "holder": "Rakesh V.", "ifsc": "HDFC0000521"},
    "MULE-2": {"bank": "ICICI", "acct": "0231XXXXXX8830", "holder": "Sana K.", "ifsc": "ICIC0000231"},
    "MULE-3": {"bank": "Paytm Payments", "acct": "9900XXXXXX2170", "holder": "Dummy Traders LLP", "ifsc": "PYTM0123456"},
    "MULE-4": {"bank": "SBI", "acct": "3822XXXXXX7791", "holder": "Imran S.", "ifsc": "SBIN0003822"},
}

DUMP_MERCHANTS = ["STAR-DUMPSHOP-7", "HYDRA-MARKET-3", "CC-LIVE.IN-SHOP9"]


def luhn_ok(num: str) -> bool:
    digits = [int(d) for d in num.replace(" ", "")]
    total, alt = 0, False
    for d in reversed(digits):
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        alt = not alt
    return total % 10 == 0


def rows() -> list[dict]:
    out: list[dict] = []
    txid = 1000

    # -- Stage A: 12 daytime card-testing probes on 15 Mar (INR 101-500)
    for i in range(12):
        txid += 1
        out.append({
            "txn_id": f"OHX-{txid}", "date": "2026-03-15",
            "time": f"{10 + i // 6:02d}:{i * 5 % 60:02d}:13", "channel": "CNP",
            "method": "card",            "card": VICTIM_CARDS[list(VICTIM_CARDS)[i % 6]], "vpa": "",
            "counterparty": DUMP_MERCHANTS[i % 3], "amount_inr": random.choice([101, 250, 375, 500]),
            "status": "APPROVED", "ip": "45.142.213.107", "note": "card-testing probe",
        })

    # -- Stage B: 02:41-02:47 IST burst, 15 Mar (9 CNP, 41k-49,999)
    for i in range(9):
        txid += 1
        out.append({
            "txn_id": f"OHX-{txid}", "date": "2026-03-15",
            "time": f"02:{41 + i}:44", "channel": "CNP", "method": "card",
            "card": VICTIM_CARDS[list(VICTIM_CARDS)[(i * 2) % 6]], "vpa": "",
            "counterparty": DUMP_MERCHANTS[i % 3],
            "amount_inr": random.choice([41000, 45000, 47500, 49000, 49999]),
            "status": "APPROVED", "ip": "185.220.101.47",
            "note": "3DS bypassed via OTP SIM-swap" if i in (2, 6) else "3DS bypassed",
        })

    # -- Stage C: 11 throttled follow-ups 02:47-03:15 (CNP)
    for i in range(11):
        txid += 1
        out.append({
            "txn_id": f"OHX-{txid}", "date": "2026-03-15",
            "time": f"02:{47 + i * 2 % 60:02d}:{(i * 17) % 60:02d}", "channel": "CNP",
            "method": "card", "card": VICTIM_CARDS[list(VICTIM_CARDS)[(i * 5) % 6]], "vpa": "",
            "counterparty": DUMP_MERCHANTS[i % 3], "amount_inr": random.choice([12000, 18500, 24000]),
            "status": "APPROVED", "ip": "185.220.101.47", "note": "post-alert throttle",
        })

    # -- Stage D: 6 more CNP daytime 15-16 Mar (to reach 27 CNP, 342,900 total)
    cnp_b = sum(r["amount_inr"] for r in out if r["channel"] == "CNP")
    targets = [8410] * 6
    drift = 342900 - cnp_b - sum(targets)
    targets[3] += drift
    for i, amt in enumerate(targets):
        txid += 1
        out.append({
            "txn_id": f"OHX-{txid}", "date": "2026-03-16",
            "time": f"1{i % 3}:{5 + i}:08", "channel": "CNP", "method": "card",
            "card": VICTIM_CARDS[list(VICTIM_CARDS)[(i * 3) % 6]], "vpa": "",
            "counterparty": DUMP_MERCHANTS[i % 3], "amount_inr": amt,
            "status": "APPROVED", "ip": "103.87.12.90", "note": "second-wave drain",
        })

    # -- Stage E: 13 UPI collect-request frauds (278,580 total)
    upi_amt = [49999, 45000, 41000, 38000, 25000, 24000, 18500, 15000, 9999, 7500, 3999, 2082, 500]
    pad = 278580 - sum(upi_amt)
    upi_amt[4] += pad
    for i, amt in enumerate(upi_amt):
        txid += 1
        out.append({
            "txn_id": f"OHX-{txid}", "date": "2026-03-15",
            "time": f"03:{20 + i}:{(i * 7) % 60:02d}", "channel": "PSP",
            "method": "upi-collect", "card": "", "vpa": f"{list(VICTIM_CARDS)[i % 6]}@upay",
            "counterparty": "aurorahrpay@ptyes", "amount_inr": amt,
            "status": "APPROVED", "ip": "91.215.85.21",
            "note": "collect request approved by victim",
        })

    # -- Stage F: 8 cash-out drains to mules (already counted in totals? No - separate legs)
    cashouts = [
        ("MULE-1", 204000), ("MULE-2", 186480), ("MULE-3", 131000), ("MULE-4", 100000),
    ]
    for i, (m, amt) in enumerate(cashouts * 2):
        if i >= 8:
            break
        txid += 1
        out.append({
            "txn_id": f"OHX-{txid}", "date": "2026-03-16",
            "time": f"{9 + i}:{10 + i}:52", "channel": "IMPS",
            "method": "transfer", "card": "", "vpa": "",
            "counterparty": f"{m}:{MULES[m]['acct']}:{MULES[m]['holder']}",
            "amount_inr": amt // 2 if i >= 4 else amt,
            "status": "APPROVED", "ip": "103.87.12.90",
            "note": "layering to mule account",
        })
    return out


def main() -> None:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    data = rows()
    # integrity: no card may exist that fails Luhn
    for r in data:
        if r["card"] and not luhn_ok(r["card"]):
            raise SystemExit(f"Luhn check failed for {r['card']}")
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(data[0].keys()))
        w.writeheader()
        w.writerows(data)

    cnp = [r for r in data if r["channel"] == "CNP"]
    upi = [r for r in data if r["channel"] == "PSP"]
    print(f"wrote {OUT}")
    print(f"  rows: {len(data)} (CNP {len(cnp)} = INR {sum(r['amount_inr'] for r in cnp):,} | "
          f"UPI {len(upi)} = INR {sum(r['amount_inr'] for r in upi):,})")


if __name__ == "__main__":
    main()
