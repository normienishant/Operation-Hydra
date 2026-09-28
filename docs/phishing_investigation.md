# 🎣 Phishing & Spoofing Investigation

**Assignment sub-problem 2.** Analysis of the five synthetic samples in
[`evidence/phishing/`](../evidence/phishing/). Tool equivalents: MXToolbox header analyzer,
VirusTotal URL scanner, AbuseIPDB, WHOIS. All header/SPF/DKIM/DMARC parsing in this doc was
produced by `analysis/scripts/analyze_headers.py`; raw log in `analysis/logs/02_headers.log`.

---

## 1. Sample inventory

| Sample | From (displayed) | Return-Path | Subject | Attachments/URLs | Verdict |
|---|---|---|---|---|---|
| hydra01.eml | "Aurora HR" `<hr@auroralogistics.in>` | `bounce@hydrapey.net` | Urgent: Pilot Leave Roster | `http://aurora-hrportal.net/login` | **phishing** |
| hydra02.eml | "IT Helpdesk" `<support@auroralogistics-support.com>` | same | Password expires in 24h | `/sso/reset` | **phishing** |
| hydra03.eml | "Payroll Team" `<payroll@auroralogistics.in>` | same | Revised salary slip — Mar 2026 | `.html` attachment (credential form) | **phishing** |
| hydra04.eml | "Travel Desk" `<travel@auroralogistics.in>` | same | Pilot duty change — confirm | `bit.ly/3hydraX` (open redirect) | **phishing** |
| hydra05.eml | "Nodal Officer" `<compliance@auroralogistics.in>` | same | KYC re-verification before 31 Mar | `auroralogistics-support.com/kyc` | **phishing** |

## 2. Header forensics (full `Received` chain — hydra01)

```
Received: from mail.hydrapey.net (45.142.213.107)  ← true origin (NL, AS208475)
          by mx.auroralogistics.in with ESMTPS id 8f2a…
Received-SPF: fail (domain owner discourages this sender)  ← hard fail (-all)
Authentication-Results: mx.auroralogistics.in;
        spf=fail smtp.mailfrom=auroralogistics.in;
        dkim=none; dmarc=fail (p=none, disposition=none)  ← DMARC policy weak!
Reply-To: hr.verify@aurora-hrportal.net  ← REAL reply destination (different domain)
X-Mailer: PHPMailer 6.8.0 (classic kit fingerprint)
```

**Tells**

1. `Return-Path` domain ≠ `From` domain (bounce laundering via hydrapey.net).
2. SPF **hard fail**: real `auroralogistics.in` publishes `v=spf1 include:_spf.google.com -all`.
3. DKIM **none** → no signature from the claimed domain.
4. DMARC `p=none` → policy exists but takes no action; this is *why* the mail reached inboxes.
5. `Reply-To` points to the attacker-controlled clone domain — a dead giveaway.
6. `X-Mailer: PHPMailer` + missing `Message-ID` from the real domain → scripted mass-mailer.

## 3. SPF / DKIM / DMARC records (recreated via `dig TXT`)

```zone
auroralogistics.in.            TXT "v=spf1 include:_spf.google.com -all"
_dmarc.auroralogistics.in.     TXT "v=DMARC1; p=none; rua=mailto:dmarc@auroralogistics.in"
aurora-hrportal.net.           TXT "v=spf1 +all"           ← allows anything (kit host)
hydrapey.net.                  TXT "v=spf1 ip4:45.142.213.0/24 +all"
; selector checks: google._domainkey.auroralogistics.in EXISTS; s1._domainkey absent
```

**Fix recommended in report:** move DMARC to `p=reject` with `rua` aggregation before T+30 days.

## 4. WHOIS intelligence (`analysis/logs/04_whois.log`)

| Domain | Created | Registrar | Age at attack | Red flag |
|---|---|---|---|---|
| auroralogistics.in | 2011-06-02 | GoDaddy | 14.8 y | genuine |
| **aurora-hrportal.net** | **2026-03-08** | NameSilo (PrivacyGuard) | **6 days** | brand-new + privacy |
| **auroralogistics-support.com** | **2026-03-05** | Namecheap (WhoisGuard) | **9 days** | brand-new + privacy |
| **hydrapey.net** | 2026-01-11 | Njalla (privacy shell) | 2 mo | stager/bounce infra |

## 5. IP intelligence (AbuseIPDB-style scoring — `analysis/logs/03_iptrace.log`)

| IP | rDNS | ASN / Country | Abuse score | Notes |
|---|---|---|---|---|
| 45.142.213.107 | mail.hydrapey.net | AS208475 / NL | **96/100** | phishing relay, 311 reports/90 d |
| 185.220.101.47 | tor-exit-47.hydrapey.net | AS205100 / RO | **88/100** | C2 + Tor exit (dual use) |
| 103.87.12.90 | ns1.aurora-hrportal.net | AS135318 / IN | **74/100** | clone-hosting (Pune VPS) |
| 91.215.85.21 | cdn.auroralogistics-support.com | AS204601 / UA | **81/100** | kit CDN, TLS via Let's Encrypt |

## 6. VirusTotal-style URL verdicts (`evidence/tool_outputs/virustotal_verdict.md`)

| URL | Engines flagging / total | Categories |
|---|---|---|
| `aurora-hrportal.net/login` | 18/93 | phishing, credential theft |
| `auroralogistics-support.com/sso/reset` | 15/93 | phishing |
| `bit.ly/3hydraX` → `aurora-hrportal.net/duty` | 11/93 (redirect resolved) | phishing, open-redirect chain |

## 7. Conclusion

The spoofing chain is fully mapped: **`hydrapey.net` (bounce/relay, NL) → spoofed From: of
`auroralogistics.in` → clone portals on `aurora-hrportal.net` (IN) / `auroralogistics-support.com` (UA)**,
with every hop corroborated by header analysis, DNS authentication results, WHOIS age, and
abuse scoring. Remedy: DMARC `p=reject`, MFA, and takedown notices to the two registrars
(template in `docs/impact_ethics_report.md`).
