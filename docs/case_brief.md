# 🐉 Operation Hydra — Case Brief

**Case ID:** OH-2026-0314
**Classification:** Simulated academic exercise — all entities fictional.
**Complainant:** Aurora Logistics Pvt. Ltd. (fictional), Pune, India
**Investigator:** Nishant (intern-cum-analyst), Cyber Forensics Cell
**Date of incident:** 14 March 2026, 09:12 IST onwards

---

## 1. How the campaign unfolded

### Stage 0 — Recon (T-14 days to T-1 day)

The threat actor (tracked internally as **THREAT-ACTOR-HYDRA**) spent two weeks on passive
reconnaissance:

- Harvested employee names/titles from a recruitment mirror of the company careers page.
- Registered the look-alike domains `aurora-hrportal.net` and `auroralogistics-support.com`
  (registrations 6 and 9 days before the attack — see `evidence/tool_outputs/whois_records.json`).
- Staged a credential-harvest clone of the company's HR portal on `aurora-hrportal.net`,
  served behind Cloudflare with a free Let's Encrypt certificate.

### Stage 1 — Phishing wave (14 Mar 2026, 09:12 IST)

212 employees received `Subject: Urgent: Pilot Leave Roster — action needed by 15:00 IST`.
The mail spoofed `hr@auroralogistics.in` but originated from a compromised cPanel host
`45.142.213.107` (NL). SPF failed (-all policy of the real domain), DKIM absent, DMARC p=none
so the spoof landed in inboxes. Samples: `evidence/phishing/hydra01.eml` … `hydra05.eml`.

- **68 recipients** clicked the embedded link.
- **41** submitted credentials to the fake portal; the kit redirected them to the genuine
  intranet (classic two-page harvest → live relay).

### Stage 2 — Malware injection (14–15 Mar 2026)

From 17 of the 41 harvested accounts, the actor logged into webmail and sent a second-wave
e-mail from *inside* the perimeter:
`Subject: INVOICE_MAR2026 — e-invoice copy attached` with `INVOICE_MAR2026.pdf.xlsm`.

Opening it triggered a malicious macro (`Auto_Open`) that:

1. Dropped and base64+XOR-decoded **HydraRAT** into `%APPDATA%\MsEdgeUpdate.exe`;
2. Registered `HKCU\...\Run\MsEdgeUpdater` for persistence;
3. Established C2 to `185.220.101.47:8443` over a TLS socket masquerading as Microsoft Edge traffic;
4. Installed a **keylogger** thread and a **logic bomb** set to wipe mapped-drive documents
   if ransom demands were unpaid after 72 h (the bomb was neutralised before trigger).

### Stage 3 — Financial fraud (15–16 Mar 2026)

Card dumps and UPI credentials harvested by the keylogger were monetised:

- 27 card-not-present transactions on a dump site (avg ₹8,410, all 3-D Secure bypassed via OTP
  SIM-swap on two employees).
- 13 UPI "collect-request" frauds (victims approved incoming collect requests while distracted
  by the fake HR portal).
- Funds landed in **4 mule accounts** (see `evidence/transactions/hydra_transactions.csv`),
  consolidated, then cashed out via P2P to BTC wallet
  `bc1qhydra9f2x7k04mule7qq0wv8nzx3a9c0dpeel7` (0.71 BTC ≈ ₹6.2 lakh).

### Stage 4 — Detection & response (16 Mar 2026)

The SOC flagged a ₹49,999 UPI collect burst at 02:47 IST. The forensic cell froze two mule
accounts via bank nodal officer, sinkholed the C2, and began this investigation.

---

## 2. Damage summary

| Impact | Figure |
|---|---|
| Direct financial loss | ₹6,21,480 |
| Machines re-imaged | 17 |
| Employee-hours lost | ~470 |
| Reputational | 1 client suspension letter, 3 press queries |
| Emotional (affected staff) | 6 employees reported stress; 2 filed grievance |

## 3. Investigative questions this repository answers

1. Which crimes were committed, and under which laws? → `docs/cybercrime_mapping.md`
2. How was the phishing/spoofing infrastructure proven? → `docs/phishing_investigation.md`
3. What did the malware do, and what are its IOCs? → `docs/malware_analysis.md`
4. Where did the money go? → `docs/financial_fraud.md`
5. What are the legal remedies, ethical dilemmas and policy suggestions? → `docs/impact_ethics_report.md`
