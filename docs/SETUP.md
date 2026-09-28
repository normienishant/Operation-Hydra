# ⚙️ Setup Instructions

## 1. Requirements

- **Python 3.11+** (3.13 tested). Analysis scripts use the **standard library only** —
  no pip packages are needed to run the investigation suite.
- Optional (report deliverables only): `python-docx` and `fpdf2`.

## 2. Clone

```bash
git clone https://github.com/normienishant/Operation-Hydra.git
cd Operation-Hydra
```

## 3. Run the analysis suite

```bash
python analysis/scripts/run_all.py
```

This executes, in order:

| Step | Script | Produces |
|---|---|---|
| 01 | `generate_phishing.py` | `evidence/phishing/hydra01–05.eml` |
| 02 | `analyze_headers.py` | `analysis/logs/02_headers.log` (+ `.json`) |
| 03 | `ip_trace.py` | `analysis/logs/03_iptrace.log` (+ `.json`) |
| 04 | `whois_lookup.py` | `analysis/logs/04_whois.log` |
| 05 | `malware_decoder.py` | `analysis/logs/05_malware.log`, `evidence/malware/iocs.json` |
| 06 | `generate_transactions.py` | `evidence/transactions/hydra_transactions.csv` |
| 07 | `trace_funds.py` | `analysis/logs/06_funds.log` |

The run is **deterministic** (fixed random seed, fixed fixtures): re-running reproduces
byte-identical evidence, which is what the CI workflow asserts.

## 4. Build the report deliverables

```bash
pip install python-docx fpdf2
python builder/build_report.py
# -> docs/report/Operation_Hydra_Report.docx
# -> docs/report/Operation_Hydra_Report.pdf
```

## 5. Verify repository integrity

```bash
python analysis/scripts/check_structure.py   # all deliverables present?
```

## 6. CI (GitHub Actions)

- `markdown-lint` — `markdownlint-cli2` over all Markdown using `.markdownlint.yml`.
- `repo-check` — runs `check_structure.py`, then the full suite on Python 3.11 & 3.13,
  compiles all scripts, and builds the PDF report to prove reproducibility.

## 7. Safety

Everything in this repository is synthetic. Do **not** scan, ping, resolve or attempt
logins against any domain/IP/account that appears in the text — they are fictional and
connecting to the real registrants of adjacent names would be unlawful.
