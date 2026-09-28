# Screenshot log — how each tool step was captured

> These are **simulated runs** of open tools (assignment permits simulation). Each entry records
> the exact command a real analyst would run and where the parsed result lives in this repo.
> Replace the `.md` notes with real PNGs when running against live services.

| Step | Tool | Real command (run manually) | Saved output here |
|------|------|------------------------------|-------------------|
| 1 | MXToolbox Header Analyzer | `MXToolbox → Deliverability → Message Header → paste hydra01.eml headers` | `mxtoolbox_header.md` |
| 2 | VirusTotal | `vt url aurora-hrportal.net/login` or web UI submit | `virustotal_verdict.md` |
| 3 | AbuseIPDB | `curl -H "Key: $ABUSEIPDB_KEY" "https://api.abuseipdb.com/api/v2/check?ipAddress=45.142.213.107"` | `abuseipdb_ipintel.md` |
| 4 | WHOIS | `whois hydrapey.net` | `whois_records.json` (offline db) |
| 5 | CyberChef | recipe: `From Base64 → XOR {key:0x5A}` on `specimen.hydra.json → encoded_payload_b64` | `analysis/logs/05_malware.log` |
| 6 | dig | `dig TXT auroralogistics.in +short` | `phishing_investigation.md §3` |
| 7 | Wireshark | capture filter `host 185.220.101.47` (sandbox) | `malware_analysis.md §3` |
| 8 | RE-tool | `python analysis/scripts/malware_decoder.py --hash` | `analysis/logs/05_malware.log` |

## In-repo simulated equivalents (deterministic, offline)

```bash
python analysis/scripts/analyze_headers.py     # = MXToolbox step 1
python analysis/scripts/ip_trace.py            # = AbuseIPDB step 3
python analysis/scripts/whois_lookup.py        # = WHOIS step 4
python analysis/scripts/malware_decoder.py     # = CyberChef step 5
python analysis/scripts/trace_funds.py         # = ledger analytics step
```

Each script prints a header block noting the real-world tool it emulates so screenshots of the
console output can stand in for tool UI screenshots in the viva.
