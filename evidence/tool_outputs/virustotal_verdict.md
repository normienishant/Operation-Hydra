# VirusTotal — simulated verdicts

> Real command: `vt url "aurora-hrportal.net/login"` (VT CLI) or submit at virustotal.com.
> Offline equivalent: `python analysis/scripts/malware_decoder.py --hash`

## File verdicts

| Indicator | SHA-256 | Detections | Top engine names |
|---|---|---|---|
| INVOICE_MAR2026.pdf.xlsm | `4f1f2a…d7e80` | **34/71** | Trojan.Agent/Maximus, HEUR:Trojan-RAT.Multi, Xlm Trojan Downloader |
| MsEdgeUpdate.exe (dropped) | `a1b2c3…8091` | **41/72** | Remcos.B, Trojan.Kryptik, Trojan-RAT.Win32.Hydra |

## URL verdicts

| URL | Detections | Categories |
|---|---|---|
| `http://aurora-hrportal.net/login` | 18/93 | phishing, malicious |
| `https://auroralogistics-support.com/sso/reset` | 15/93 | phishing |
| `https://auroralogistics-support.com/kyc` | 14/93 | phishing |
| `https://bit.ly/3hydraX` (→ aurora-hrportal.net/duty) | 11/93 | phishing, redirect |

## Behaviour tab (sandbox summary, simulated)

```
- Drops executable into %APPDATA% and adds Run key  → persistence
- Injects into explorer.exe (process hollowing flag)
- HTTPS beacon to 185.220.101.47:8443 (Tor-exit ASN listed)  → C2
- Global keyboard hook enumeration                  → keylogger
- Timer scheduled 72h; file-overwrite routine on mapped drives → logic bomb
```

Verdict consistency: matches the in-repo classification
**Trojan-RAT + keylogger + logic bomb** (`docs/malware_analysis.md`).
