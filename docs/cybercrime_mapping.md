# ⚖️ Cybercrime Decomposition & Legal Mapping

**Assignment sub-problem 1.** Six distinct offences are deconstructed below and mapped to
Indian law (IT Act 2000 as amended by ITAA 2008, and the Bharatiya Nyaya Sanhita 2023 which
replaced the IPC) and to global equivalents (US CFAA, EU GDPR, Council of Europe Budapest
Convention ETS 185).

> Legal mapping is for **academic discussion**. This is not legal advice. Section numbers are
> cited as taught in Unit 2; practitioners must verify current texts.

---

## Crime index (6 distinct offences)

| # | Crime | Where in the case |
|---|-------|-------------------|
| C1 | **Phishing / identity theft** | 212 spoofed e-mails, 41 credential harvests |
| C2 | **E-mail & web spoofing** | spoofed `hr@auroralogistics.in`, clone portal `aurora-hrportal.net` |
| C3 | **Unauthorized access** | 17 accounts logged into by actor with stolen creds |
| C4 | **Malware injection (RAT/keylogger)** | `INVOICE_MAR2026.pdf.xlsm` → HydraRAT implant |
| C5 | **Card/UPI financial fraud + cheating** | ₹6.2 lakh drained via CNP + collect-request frauds |
| C6 | **Money laundering via mules & crypto** | 4 mule accounts → P2P → BTC `bc1qhydra…` |

---

## C1 — Phishing & identity theft

| Jurisdiction | Provision | Fit |
|---|---|---|
| 🇮🇳 IT Act | **S.66C** — identity theft (dishonest use of another's unique ID: e-mail id, password) | harvesting credentials = identity theft |
| 🇮🇳 IT Act | **S.66D** — cheating by personation using a computer resource | fake HR sender |
| 🇮🇳 BNS 2023 | **S.318(4)** — cheating (old IPC §420) | inducement to surrender credentials |
| 🇮🇳 BNS 2023 | **S.319(2)** — cheating by personation (old IPC §416/417) | impersonating HR |
| 🌍 US | **18 U.S.C. §1028A** (aggravated identity theft), **CFAA §1030(a)(4)** | access device / credential abuse |
| 🌍 EU | **GDPR Art. 32** (processor duty — breached by both sides: employer's mail flow, harvested PI) | data protection angle |
| 🌍 Budapest | **Art. 7** (computer-related forgery), **Art. 8** (computer-related fraud) | cross-border prosecution basis |

**Punishment (India):** S.66C — up to 3 yrs + ₹1 lakh; S.66D — up to 3 yrs + ₹1 lakh;
BNS 318(4) — up to 7 yrs + fine.

## C2 — E-mail & web spoofing

| Jurisdiction | Provision | Fit |
|---|---|---|
| 🇮🇳 IT Act | **S.66D** — personation using computer resource (spoofed From:, clone site) | core provision |
| 🇮🇳 IT Act | **S.43** — unauthorised access to a computer resource (company mail server relaying) | civil liability + compensation |
| 🇮🇳 BNS 2023 | **S.338** — forgery of electronic records (old IPC §463/468, forged headers) | forged `Reply-To`/headers |
| 🌍 US | **CAN-SPAM §7704** (header falsification) + CFAA | header spoofing |
| 🌍 EU | **GDPR Art. 5(1)(a)** fairness in processing harvested employee data | — |
| 🌍 Budapest | **Art. 7** | electronic forgery |

**Punishment (India):** S.66D — up to 3 yrs + ₹1 lakh.

## C3 — Unauthorized access

| Jurisdiction | Provision | Fit |
|---|---|---|
| 🇮🇳 IT Act | **S.43** read with **S.66** — accessing webmail/HR portal accounts without authorisation | 17 accounts |
| 🇮🇳 IT Act | **S.66(2)** aggravated where identity is dishonestly used | — |
| 🇮🇳 BNS 2023 | **S.305** — theft/dishonest intention in respect of property incl. intangible | credential misuse |
| 🌍 US | **CFAA 18 U.S.C. §1030(a)(2)/(4)** — unauthorised access to obtain information | exact analogue |
| 🌍 EU | NIS2 Directive Art. 21 (security measures) — employer-side duty breach | supervisory angle |
| 🌍 Budapest | **Art. 2** — illegal access | first substantive offence |

**Punishment (India):** S.66 — up to 3 yrs + ₹5 lakh (civil: damages under S.43/45).

## C4 — Malware injection (RAT + keylogger + logic bomb)

| Jurisdiction | Provision | Fit |
|---|---|---|
| 🇮🇳 IT Act | **S.43(c)** — introduction of computer contaminant | implanting HydraRAT |
| 🇮🇳 IT Act | **S.66** + **S.66F** (cyber-terrorism arguable if critical infra; kept at S.66 here) | system damage |
| 🇮🇳 IT Act | **S.66E** — violation of privacy (keylogger capturing private communications) | keystrokes incl. passwords |
| 🇮🇳 IT Act | **S.66B** — dishonestly receiving stolen computer resource | handling exfiltrated data |
| 🇮🇳 BNS 2023 | **S.303(2)** theft; **S.326(g)** mischief by computer (old IPC §426/§66 IT Act bridge) | persistence + logic bomb |
| 🌍 US | **CFAA §1030(a)(5)** — transmission of a program causing damage | precise match for the implant |
| 🌍 EU | **GDPR Art. 33** — 72-hour breach notification duty triggered | employer compliance failure |
| 🌍 Budapest | **Art. 4** (data interference), **Art. 3** (illegal interception for keylogger) | dual fit |

**Punishment (India):** S.66E — up to 3 yrs + ₹2 lakh; S.66F — up to life if terrorism limb met.

## C5 — Card / UPI financial fraud

| Jurisdiction | Provision | Fit |
|---|---|---|
| 🇮🇳 IT Act | **S.66C** identity theft (card data, UPI PIN) | — |
| 🇮🇳 IT Act | **S.66D** cheating by personation (3-D Secure OTP impersonation calls) | — |
| 🇮🇳 BNS 2023 | **S.318(4)** cheating; **S.316(2)** criminal breach of trust (for the *mule* holders who assisted) | — |
| 🇮🇳 RBI | Payment System Operators rules — **UPI collect-request** misuse notification (2023 guidelines) | regulatory breach by PSP |
| 🌍 US | 18 U.S.C. §1029 (access-device fraud) | CNP card fraud |
| 🌍 EU | **PSD2 Art. 97** strong-customer-authentication bypass | bank-side liability |
| 🌍 Budapest | **Art. 8** computer-related fraud | — |

**Punishment (India):** BNS 318(4) — up to 7 yrs + fine; restitution under S.395 BNSS (victim compensation).

## C6 — Money laundering (mule accounts → crypto)

| Jurisdiction | Provision | Fit |
|---|---|---|
| 🇮🇳 **PMLA 2002** | **S.3** (proceeds of crime) & **S.4** punishment; scheduled offence = BNS 318(4) | layering via 4 mules |
| 🇮🇳 IT Act | **S.66B** receiving stolen computer resource (crypto purchased with proceeds) | — |
| 🇮🇳 BNS 2023 | **S.111** organised crime (small-value, repeated, syndicated) | — |
| 🌍 US | 18 U.S.C. §1956/§1957 (money laundering), §1960 (unlicensed money transmitting — P2P desk) | — |
| 🌍 EU | **AMLD5/AMLD6** — VASP KYC duty evaded by P2P cash-out | — |
| 🌍 Budapest | **Art. 11** laundering of the proceeds of cyber-crime | added by 2AP |

**Punishment (India):** PMLA S.4 — rigorous imprisonment 3–7 yrs + fine up to ₹5 lakh.

---

## Responsibility matrix

| Actor role | Offences |
|---|---|
| THREAT-ACTOR-HYDRA (principal) | C1, C2, C3, C4, C5, C6 |
| Phishing-kit vendor (infra as a service) | C1, C2 (abetment S.65 IT Act / S.61 BNS) |
| Mule account holders (4) | C5 (CBT), C6 (PMLA layering) |
| P2P crypto desk | C6 (S.1960 US; PMLA S.3 if knowledge proved) |
| Compromised cPanel host owner (45.142.213.107) | negligent — S.43 IT Act civil only |

## Appellate & forum notes (for the report)

- **Adjudicating officer:** MeitY-appointed AO under S.46 IT Act for S.43/66 civil compensation.
- **Criminal trial:** Magistrate, Pune; police complaint under S.66C/66D/66 IT Act (police may
  investigate offences with imprisonment > 3 yrs — S.78 IT Act).
- **PMLA:** Enforcement Directorate complaint before Special PMLA Court.
- **Evidence:** S.65B(4) Indian Evidence Act (now **S.63 BSA 2023**) certificate mandatory for
  the .eml files, transaction CSV and memory dumps — produced in `docs/AUTHORSHIP_DECLARATION.md`.
