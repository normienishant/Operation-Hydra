#!/usr/bin/env python3
"""Build docs/report/Operation_Hydra_Report.docx and .pdf from the analysis outputs.

Priority: DOCX via python-docx; PDF via fpdf2. If a library is missing, the script
prints the missing dependency and exits non-zero so CI surfaces it.
"""
from __future__ import annotations

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUTDIR = os.path.join(ROOT, "docs", "report")

MD_DOCS = [
    ("docs/impact_ethics_report.md", "Legal-Technical Impact Report"),
    ("docs/cybercrime_mapping.md", "Cybercrime Decomposition & Legal Mapping"),
    ("docs/phishing_investigation.md", "Phishing & Spoofing Investigation"),
    ("docs/malware_analysis.md", "Malware Payload Analysis"),
    ("docs/financial_fraud.md", "Financial Fraud Tracing"),
]

EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F900-\U0001F9FF\u2190-\u21ff\u2500-\u257f\u2580-\u259f\u25a0-\u25ff\u2713\u2714\u2717\u2718]"
)

# Common typographic Unicode -> ASCII (fpdf2 core fonts are latin-1 only)
TRANSLIT = {
    "\u2014": " -- ",   # em dash
    "\u2013": " - ",    # en dash
    "\u2018": "'", "\u2019": "'",
    "\u201c": '"', "\u201d": '"',
    "\u2026": "...",
    "\u00b7": "*",
    "\u20b9": "Rs.",   # rupee sign
    "\u2260": "!=",
    "\u2264": "<=", "\u2265": ">=",
    "\u00d7": "x",
    "\u2192": "->", "\u2190": "<-",
    "\u2194": "<->",
    "\u2022": "-",
    # box-drawing / geometric shapes used in ASCII diagrams
    "\u2500": "-", "\u2502": "|", "\u250c": "+", "\u2510": "+",
    "\u2514": "+", "\u2518": "+", "\u251c": "+", "\u2524": "+",
    "\u252c": "+", "\u2534": "+", "\u253c": "+",
    "\u25b2": "^", "\u25bc": "v", "\u25ba": ">", "\u25c4": "<",
    "\u2705": "[OK]", "\u274c": "[X]", "\u26a0": "[!]",
    "\u00a0": " ", "\u200b": "",
}


def clean(text: str) -> str:
    """Strip markdown emphasis/links and transliterate to latin-1-safe text."""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)          # images
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)      # links -> text
    text = re.sub(r"[*_`]{1,3}", "", text)                    # emphasis/backticks
    for src, dst in TRANSLIT.items():
        text = text.replace(src, dst)
    text = EMOJI_RE.sub("", text)                             # remaining emoji/arrows
    # final safety net: core PDF fonts are latin-1 only
    text = text.encode("latin-1", errors="replace").decode("latin-1")
    return text


def fit(text: str, max_token: int = 70) -> str:
    """Break unbreakable tokens (base64 blobs, long URLs) so fpdf2 can wrap them."""
    out = []
    for tok in text.split(" "):
        while len(tok) > max_token:
            out.append(tok[:max_token])
            tok = tok[max_token:]
        out.append(tok)
    return " ".join(out)


def md_blocks(md: str) -> list[tuple[str, str]]:
    """Very small markdown-block iterator -> (kind, text) tuples."""
    blocks: list[tuple[str, str]] = []
    in_code = False
    code: list[str] = []
    for line in md.splitlines():
        if line.startswith("```"):
            if in_code:
                blocks.append(("code", "\n".join(code)))
                code = []
            in_code = not in_code
            continue
        if in_code:
            code.append(line)
            continue
        if line.startswith("|") and line.rstrip().endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                continue  # separator row
            blocks.append(("row", cells))
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            blocks.append((f"h{min(len(m.group(1)), 3)}", m.group(2)))
            continue
        if line.startswith("- "):
            blocks.append(("li", line[2:]))
            continue
        if line.startswith("> "):
            blocks.append(("quote", line[2:]))
            continue
        if not line.strip():
            continue
        blocks.append(("p", line))
    return blocks


def load_analysis_summary() -> str:
    """Pull headline figures out of the generated logs to append to the report."""
    logs = os.path.join(ROOT, "analysis", "logs")
    parts = []

    hdr = os.path.join(logs, "02_headers.json")
    if os.path.exists(hdr):
        with open(hdr, encoding="utf-8") as fh:
            data = json.load(fh)
        n = len(data)
        spoofed = sum(1 for r in data if r["verdict"] == "PHISHING/SPOOFED")
        parts.append(f"Header analysis: {spoofed}/{n} samples classified PHISHING/SPOOFED.")

    funds = os.path.join(logs, "06_funds.log")
    if os.path.exists(funds):
        with open(funds, encoding="utf-8") as fh:
            txt = fh.read()
        for pat in (r"Card-not-present \(CNP\).*", r"UPI collect-request.*"):
            m = re.search(pat, txt)
            if m:
                parts.append(clean(m.group(0)))

    return " ".join(parts) or "Analysis logs not yet generated - run analysis/scripts/run_all.py first."


def build_docx(path: str) -> None:
    from docx import Document
    from docx.shared import Pt

    doc = Document()
    doc.add_heading("Operation Hydra - Unraveling a Multi-Vector Cyber Crime", 0)
    doc.add_paragraph(
        "Assignment 2, Unit 2: Types of Cyber Crimes. Simulated multi-vector campaign "
        "(phishing, spoofing, malware injection, financial fraud). All entities fictional."
    )
    doc.add_paragraph(load_analysis_summary())

    for rel, _title in MD_DOCS:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
            md = fh.read()
        doc.add_page_break()
        doc.add_heading(rel, 1)
        for kind, payload in md_blocks(md):
            if kind.startswith("h"):
                doc.add_heading(clean(payload), int(kind[1]))
            elif kind == "p":
                doc.add_paragraph(clean(payload))
            elif kind == "li":
                doc.add_paragraph(clean(payload), style="List Bullet")
            elif kind == "quote":
                p = doc.add_paragraph(clean(payload))
                p.runs[0].italic = True if p.runs else None
            elif kind == "code":
                p = doc.add_paragraph()
                run = p.add_run(payload)
                run.font.name = "Courier New"
                run.font.size = Pt(8)
            elif kind == "row":
                # tables are appended as pipe-separated lines for portability
                doc.add_paragraph(" | ".join(clean(c) for c in payload))

    doc.save(path)


def build_pdf(path: str) -> None:
    from fpdf import FPDF, XPos, YPos

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, "Operation Hydra - Multi-Vector Cyber Crime Investigation", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(0, 5, clean(
        "Assignment 2, Unit 2: Types of Cyber Crimes. Simulated campaign: phishing, spoofing, "
        "malware injection, financial fraud. All entities fictional. Case OH-2026-0314."
    ))
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 8)
    pdf.multi_cell(0, 4.5, clean(load_analysis_summary()), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    for rel, _ in MD_DOCS:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
            md = fh.read()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 12)
        pdf.multi_cell(0, 7, clean(rel), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1)
        pdf.set_font("Helvetica", "", 8.5)
        for kind, payload in md_blocks(md):
            if kind.startswith("h"):
                pdf.set_font("Helvetica", "B", 11)
                pdf.multi_cell(0, 5, clean(payload), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.set_font("Helvetica", "", 8.5)
            elif kind in ("p", "quote"):
                pdf.multi_cell(0, 4, fit(clean(payload)), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            elif kind == "li":
                pdf.multi_cell(0, 4, "  - " + fit(clean(payload)), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            elif kind == "code":
                pdf.set_font("Courier", "", 7)
                pdf.multi_cell(0, 3.2, fit(clean(payload), 95), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.set_font("Helvetica", "", 8.5)
            elif kind == "row":
                pdf.multi_cell(0, 4, fit(" | ".join(clean(c) for c in payload)), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.output(path)


def main() -> None:
    os.makedirs(OUTDIR, exist_ok=True)
    docx_path = os.path.join(OUTDIR, "Operation_Hydra_Report.docx")
    pdf_path = os.path.join(OUTDIR, "Operation_Hydra_Report.pdf")

    try:
        build_docx(docx_path)
        print(f"DOCX written: {os.path.relpath(docx_path, ROOT)}")
    except ImportError as e:
        print(f"python-docx missing ({e}); install with: pip install python-docx")

    try:
        build_pdf(pdf_path)
        print(f"PDF written : {os.path.relpath(pdf_path, ROOT)}")
    except ImportError as e:
        print(f"fpdf2 missing ({e}); install with: pip install fpdf2")

    if not (os.path.exists(docx_path) and os.path.exists(pdf_path)):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
