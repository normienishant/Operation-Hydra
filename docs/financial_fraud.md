# 💸 Financial Fraud Tracing

**Assignment sub-problem 4.** Simulated payment-fraud scenario built from the compromised card
and UPI credentials harvested by HydraRAT. Dataset: `evidence/transactions/hydra_transactions.csv`
(40 synthetic records); full analysis: `analysis/logs/06_funds.log`, produced by
`analysis/scripts/trace_funds.py`.

> All accounts, cards, UPI VPAs and wallets below are **synthetic** and pass Luhn only as dummy
> data. They belong to no one.

---

## 1. Fraud typologies observed in the dataset

| Type | Count | Amount | Mechanism |
|---|---|---|---|
| Card-not-present (CNP) | 38 (incl. 12 micro card-testing probes) | ₹3,42,900 | dumped card data on a "dump shop"; 3-D Secure bypassed by OTP SIM-swap (2 employees) |
| UPI collect-request fraud | 13 | ₹2,78,580 | victims approved fake "Aurora HR payroll refund" collect requests |
| **Total** | **51** | **₹6,21,480** | matches the case-brief loss figure |

## 2. Temporal pattern (the fingerprint)

```
10:00–12:00 IST  12 micro-probes (₹101–₹500)                    ← card testing
02:41–02:47 IST  burst of 9 transactions (₹41k–₹49,999 each)   ← SOC alert trigger
02:47–03:15      11 more, throttled after the alert
daytime 15 Mar   12 low-value probes (₹101–₹500, card testing)
16 Mar           8 cash-out drains to mules
```

Classic **card-testing → burst → throttle → drain** lifecycle; the 02:47 burst is what a real
rule engine (`velocity > 5 txn/min & ticket 40–50k & new MCC 5999`) would flag.

## 3. Money flow — the layering chain

```
38 CNP + 13 UPI victims
        │  (₹6,21,480 across 51 txns)
        ▼
MULE-1  HDFC ****4412  "Rakesh V."   ₹2,04,000  ← pass-through within 11 min
MULE-2  ICICI ****8830  "Sana K."    ₹1,86,480  ← 7 withdrawals @ ATM (card cloned)
MULE-3  Paytm  ****2170  "Dummy Traders LLP" ₹1,31,000 ← shell entity, GST fake
MULE-4  SBI   ****7791  "Imran S."    ₹1,00,000  ← student account, opened 3 days prior
        │  consolidation to MULE-3 (₹5,21,480)
        ▼
P2P crypto desk (Telegram @hydra_otc, simulated) — 2 trades
        ▼
BTC wallet  bc1qhydra9f2x7k04mule7qq0wv8nzx3a9c0dpeel7   (0.71 BTC)
        ├── hop → bc1q9x7wallet2hop0fake4addr5zz6789012345 (peel chain, 3 hops)
        └── mixer exit (simulated) — endpoint not traced (documented gap)
```

Full hop-by-hop table: `analysis/logs/06_funds.log` §"Ledger trace".

## 4. How the mules were identified

| Signal | Evidence |
|---|---|
| Account age < 30 days | MULE-4 opened 3 days pre-campaign |
| Velocity in/out ≈ 100% within minutes | MULE-1 ledger |
| Dormant → sudden ₹1–2 lakh inflow | MULE-3 |
| Shared device/IP fingerprints | MULE-2 & MULE-4 both from same mobile UA 103.87.12.0/24 (the clone-host range!) |
| Withdrawal pattern | 7 ATM pulls in 40 min across 2 cities — impossible for genuine owner |

## 5. Tracing the crypto leg (simulated)

```
bc1qhydra9f2… (receiving 0.71 BTC from 2 desk addresses)
   └─ tx1 0.35 BTC → bc1q9x7hop1fake… (T+3h)
        └─ tx2 0.34 BTC → bc1q9x7hop2fake… (T+9h, peel 0.01 fee)
             └─ tx3 0.33 BTC → mixer (SIMULATED — deliberately unresolvable)
```

Chain-analysis notes (methodology only): cluster by common-input-ownership heuristic, peel-chain
detection, change-address labelling. Endpoint deliberately undocumented → becomes an
**ethical-dilemma exhibit** in the impact report (see §Ethics).

## 6. Legal hooks for the money trail

| Step | Law |
|---|---|
| Card/UPI fraud | IT Act S.66C/66D + BNS S.318(4) |
| Mule holders | BNS S.316(2) criminal breach of trust; PMLA S.3 layering |
| P2P desk | PMLA S.3; US §1960 analogue |
| Freezing | PMLA S.5 attachment; S.102 CrPC (now BNSS S.106) seizure of mule accounts — 2 frozen T+1 |
| Crypto seizure | PMLA + IT Act S.66B; exchange KYC summons under FIU-IND VASP registration (2023) |

## 7. Recovery outlook (report figure)

₹2,04,000 frozen in MULE-1/MULE-4 (33%); ₹3,10,480 dissipated via ATMs/mixer (67%) —
the report uses this split to argue for **real-time mule-account screening** as the
highest-leverage fix.
