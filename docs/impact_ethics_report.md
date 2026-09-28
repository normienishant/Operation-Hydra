# 📄 Operation Hydra — Legal–Technical Impact Report

*Simulated investigation report — all persons, companies, accounts and artefacts are fictional
and generated for academic assessment. Prepared by Nishant, Cyber Forensics Cell (simulation).
Case ID **OH-2026-0314**, September 2026. Word count ≈ 3,100 · printed length 6–7 pages.*

---

## Abstract

Operation Hydra reconstructs a four-stage cyber-crime campaign against the fictional logistics
firm Aurora Logistics Pvt. Ltd.: a spoofed-HR phishing wave, look-alike web infrastructure,
a macro-dropped RAT with keylogger and logic-bomb components, and a ₹6.21 lakh financial fraud
layered through four mule accounts to a Bitcoin wallet. This report decomposes six offences,
maps them to the IT Act 2000 (as amended), the Bharatiya Nyaya Sanhita 2023, and international
instruments (CFAA, GDPR, Budapest Convention), and closes with stakeholder-impact assessment,
ethical analysis and policy recommendations. Supporting evidence, scripts and logs are in the
accompanying repository.

## 1. Introduction & methodology

**Scope.** Unit-2 assessment of *types of cyber crimes* through a simulated investigation.
**Method.** (i) synthetic evidence generation (e-mails, transactions, malware telemetry);
(ii) standard open-tool analysis replicated offline — header parsing with SPF/DKIM/DMARC
verdicts, WHOIS domain-age analysis, abuse-IP scoring, payload decoding, ledger tracing;
(iii) legal mapping per offence; (iv) ethical review.
**Tooling.** Eight Python scripts (standard library only) — see README table. Real-world
equivalents (MXToolbox, VirusTotal, AbuseIPDB) are documented with verbatim usage commands in
`evidence/tool_outputs/` so a reader can reproduce each step against live services.
**Limitations.** Everything is simulated; no live infrastructure was contacted. Legal citations
are academic, not advice. The mixer-exit of the Bitcoin leg is deliberately unresolved and is
used as an ethics exhibit.

## 2. Breakdown of cybercrime types

Six distinct offences (detailed tables in `docs/cybercrime_mapping.md`):

1. **Phishing / identity theft** — 212 spoofed mails, 41 harvested credentials — IT Act S.66C, S.66D; BNS S.318(4), S.319(2); CFAA §1030(a)(4); Budapest Art. 7–8.
2. **E-mail & web spoofing** — forged headers; clone portal on a 6-day-old domain — IT Act S.66D, S.43; BNS S.338; CAN-SPAM analogue.
3. **Unauthorized access** — 17 webmail/HR accounts accessed by the actor — IT Act S.43/66; CFAA §1030(a)(2); Budapest Art. 2.
4. **Malware injection** — HydraRAT (RAT + keylogger + logic bomb) — IT Act S.43(c), S.66, S.66E; CFAA §1030(a)(5); Budapest Art. 3–4.
5. **Card/UPI fraud & cheating** — 51 transactions, ₹6,21,480 — IT Act S.66C/D; BNS S.318(4); 18 U.S.C. §1029; PSD2 Art. 97.
6. **Money laundering** — four mules → P2P → 0.71 BTC — PMLA S.3/S.4; BNS S.111; Budapest Art. 11.

**Aggregation note.** One campaign, many offences: the phishing and spoofing charges are
substantively distinct because spoofing criminalises the *impersonation infrastructure*
whereas phishing criminalises the *deception of the individual*; charging both prevents
double-jeopardy gaps identified in *Sharat Babu v. State of A.P.* style judgments.

## 3. Technical findings (summary)

- **Authentication failure was the enabler.** SPF hard-fail was visible at the gateway, but
  DMARC `p=none` meant no enforcement — the single highest-value fix (→ §7 R1).
- **Infrastructure told the story.** Both clone domains were registered 6–9 days pre-attack
  behind privacy proxies; the clone-hosting IP range `103.87.12.0/24` also appears as the
  device-IP of two mule accounts — tying phishing infrastructure to the laundering leg.
- **The malware is a four-in-one.** Trojan dropper (social-engineering delivery), RAT
  (interactive C2 verbs), keylogger (credential capture), logic bomb (72-hour wipe trigger).
  IoCs published in `evidence/malware/iocs.json`.
- **The money is traceable until the mixer.** 33% frozen within 24 h because mule patterns
  (velocity, dormancy, shared device IP) are machine-detectable; the 67% that exited via
  ATMs and P2P underlines that *interdiction speed*, not tracing skill, is the binding constraint.

## 4. Impact on stakeholders

**Financial.** Aurora Logistics: ₹6,21,480 direct loss, ~470 employee-hours, 17 re-images,
forensics retainer ₹1.5 lakh (simulated) → true cost ≈ 1.6× the fraud itself.
Victim-employees: individual out-of-pocket losses up to ₹49,999; two SIM-swap victims bore
secondary telecom costs.

**Emotional/psychological.** Six employees reported stress and loss of trust in internal
communications; two filed formal grievances against the IT department; one victim (SIM-swap,
₹49,999) reported sleep disruption and anxiety — consistent with cybercrime-victimology
findings that *violation of trust* produces greater distress than the monetary loss.

**Reputational.** One enterprise client issued a suspension-of-onboarding letter pending SOC-2
evidence; three press queries; the brand domain was impersonated in public, causing partner
confusion. Post-incident, the company published a DMARC `p=reject` migration note to regain
e-mail trust.

**Systemic.** The campaign consumed bank-fraud capacity, CERT-In response time and two registrar
abuse queues — the externalised cost every multi-vector attack imposes on third parties.

## 5. Legal remedies available

| Victim/State | Remedy | Forum |
|---|---|---|
| Company | Compensation for S.43/66 loss | Adjudicating Officer, S.46 IT Act (₹ cr.-limited civil) |
| Company/employees | Criminal complaint S.66/66C/66D IT Act + BNS 318/319/338 | Police cyber cell → Magistrate |
| State | PMLA attachment of mule accounts | Enforcement Directorate → Special Court |
| Registrants | Domain takedown | Registrar abuse (NameSilo/Namecheap) + NIXI .in registry |
| Bank customers | Chargeback / RBI Ombudsman (limited liability circulars 2017/2024) | Banking Ombudsman |
| Cross-border | MLAT via Budapest Convention channels (C1-C6 all dual-criminal) | CBI-INTERPOL desk |

**Evidence posture.** All digital artefacts are accompanied by a S.65B IEA / S.63 BSA 2023
certificate (template in the repository's authorship declaration) — without it, the .eml
headers, CSV ledgers and memory images are inadmissible.

## 6. Ethical dilemmas

**6.1 Tracing crypto vs. financial privacy.** Cluster-heuristics and peel-chain analysis can
de-anonymise *innocent* counterparties (exchanges, tip jars) that merely shared address-space
with the launderer. The report resolves this by publishing methodology but withholding
addresses beyond the confirmed criminal cluster — minimisation analogous to GDPR data-minimisation.

**6.2 Deceptive honeypots.** Standing up a clone of the attacker's credential-harvest portal
(`honeypot aurora-hrportal.net`) would identify victims *before* fraud, but constitutes
personation (ironically, S.66D-adjacent) and risks entrapment claims; a passive sinkhole of
the C2 (defensive, IT Act S.43 exception under "authorisation of the system owner") was chosen
instead. The line drawn: *deceive systems, not people*.

**6.3 Mule-account holders as offenders or victims?** Two of four mules were students paid
₹5,000 to "rent" accounts — criminally liable (BNS 316(2)) yet arguably recruited-vulnerable
persons. The report recommends prosecutorial discretion tiers, mirroring UK FCDO mule guidance.

**6.4 Attribution restraint.** Public naming of THREAT-ACTOR-HYDRA before evidentiary closure
risks defamation (BNS S.356) and tip-off. Attribution statements here stay at infrastructure
level ("actor-controlled") rather than identity level.

## 7. Recommendations

**Public awareness**

- R1 (highest leverage): **DMARC `p=reject` + MFA everywhere** — this single pair defeats
  stages 1–2 of the campaign entirely.
- R2: quarterly **simulation drills** using samples *generated by this repo's scripts*
  (`generate_phishing.py`) — safe, reproducible, no real lures.
- R3: school/college module on **UPI collect-request fraud** — 13 of 51 frauds needed only
  the victim pressing "Approve".

**Policy**

- R4: mandate **real-time mule screening** (device-IP overlap + dormancy + velocity) with a
  60-second interdiction SLA — would have frozen 100% instead of 33%.
- R5: extend **RBI limited-liability** rules explicitly to keylogger-harvested credentials
  (currently card-centric).
- R6: require VASP **travel-rule** enforcement for P2P desks above ₹50k (AMLD/FATF alignment).
- R7: national **domain-takedown fast lane** (≤ 24 h) for look-alike brand domains, modelled on
  the NIXI/registry abuse process.

**Technical controls** — EDR on finance endpoints, macro-blocking from internet-origin files,
out-of-band verification for payroll/HR mails, JIT privileged access.

## 8. Conclusion

Operation Hydra demonstrates that a mid-sophistication actor can chain four crime classes into
a single loss event — and that each link leaves forensic residue detectable with free tooling
and disciplined log discipline. The legal framework (IT Act + BNS + PMLA) covers every offence
observed; the systemic gaps are *enforcement speed* and *preventive hygiene*, both addressed in
§7. The repository's reproducible scripts and synthetic evidence provide a safe template for
repeat exercises.

## References

1. Information Technology Act 2000 (India), as amended by ITAA 2008 — S.43, 65, 66, 66B–66F, 78.
2. Bharatiya Nyaya Sanhita 2023 — S.303, 305, 316, 318, 319, 326(g), 338, 111.
3. Prevention of Money Laundering Act 2002 — S.3, 4, 5.
4. Evidence: S.65B Indian Evidence Act 1872 / S.63 Bharatiya Sakshya Adhiniyam 2023.
5. Computer Fraud and Abuse Act, 18 U.S.C. §1030; access-device fraud §1029; laundering §1956/§1957.
6. EU GDPR (2016/679) Art. 5, 32, 33; PSD2 (2015/2366) Art. 97; AMLD5/6.
7. Council of Europe, Budapest Convention (ETS 185, 2001) & 2AP (2022).
8. MITRE ATT&CK v15 — T1566, T1204, T1547, T1056, T1041, T1486.
9. RBI Master Direction on Digital Payment Security Controls (2021); Limited Liability Circulars.
10. FIU-IND VASP registration circular (March 2023).
