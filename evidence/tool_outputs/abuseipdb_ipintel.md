# AbuseIPDB — simulated IP intel (checked 2026-03-16)

> Real command:
> `curl -s -H "Key: $ABUSEIPDB_KEY" -H "Accept: application/json" \
>   "https://api.abuseipdb.com/api/v2/check?ipAddress=45.142.213.107&maxAgeInDays=90"`
> Offline equivalent: `python analysis/scripts/ip_trace.py --ip 45.142.213.107`

| ipAddress | abuseConfidenceScore | totalReports | lastReportedAt | countryCode | isp | usageType | domainOfIP |
|---|---|---|---|---|---|---|---|
| 45.142.213.107 | **96** | 311 | 2026-03-16T02:52Z | NL | HydraNet Hosting B.V. | data center/hosting | mail.hydrapey.net |
| 185.220.101.47 | **88** | 214 | 2026-03-16T05:10Z | RO | HydraTor Transit | data center | tor-exit-47.hydrapey.net |
| 103.87.12.90 | **74** | 96 | 2026-03-15T19:44Z | IN | PuneHost Cloud | hosting | ns1.aurora-hrportal.net |
| 91.215.85.21 | **81** | 142 | 2026-03-16T01:03Z | UA | DniproHost LLC | hosting | cdn.auroralogistics-support.com |

Report categories (90-day window, all four IPs):

```
18 = brute force · 22 = SSH · 15 = phishing · 21 = web app attack ·
9 = open proxy · 14 = port scan · 20 = bad web bot
```

**Investigative note:** the two hosting ASNs used for the clone portals (IN + UA) never appear
in the mail path — separate procurement from the mail relay (NL), i.e., deliberate
infrastructure separation typical of kit operators. All four IPs are in the repo's IOC set
(`evidence/malware/iocs.json` → `ips`).
