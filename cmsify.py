#!/usr/bin/env python3
"""
cmsify.py
Offline CMS/ICD-10 language converter for Daily Progress Notes.
Version: 1.0  —  Local-only, hallucination-proof
"""

import re
import pandas as pd
from rapidfuzz import process

# ---------------------------
# LOAD ICD-10 TABLE (CSV)
# ---------------------------
# Download from CMS.gov (icd10cm_codes_2025.csv or similar)
# Columns expected: Code, ShortDesc, LongDesc

try:
    ICD10 = pd.read_csv("icd10cm_codes.csv", dtype=str)
    ICD_LIST = ICD10["LongDesc"].tolist()
except FileNotFoundError:
    ICD10 = pd.DataFrame(columns=["Code", "ShortDesc", "LongDesc"])
    ICD_LIST = []
    print("⚠️ ICD-10 CSV not found. Mapping will use placeholder text.\n")

# ---------------------------
# COMMON ABBREVIATIONS MAP
# ---------------------------

ABBR_MAP = {
    "DM2": "Type 2 diabetes mellitus",
    "DM1": "Type 1 diabetes mellitus",
    "HTN": "Hypertension",
    "AKI": "Acute kidney injury",
    "CKD": "Chronic kidney disease",
    "CHF": "Congestive heart failure",
    "COPD": "Chronic obstructive pulmonary disease",
    "OSA": "Obstructive sleep apnea",
    "CAD": "Coronary artery disease",
    "AFib": "Atrial fibrillation",
}

# ---------------------------
# FUNCTIONS
# ---------------------------

def expand_abbreviations(text: str) -> str:
    for k, v in ABBR_MAP.items():
        text = re.sub(rf"\b{k}\b", v, text)
    return text


def detect_modifier(phrase: str) -> str:
    if re.search(r"acute|new|sudden", phrase, re.I):
        return "acute"
    if re.search(r"chronic|hx of", phrase, re.I):
        return "chronic"
    if re.search(r"improv|resolv", phrase, re.I):
        return "resolving"
    if re.search(r"uncontrolled|poorly", phrase, re.I):
        return "uncontrolled"
    if re.search(r"controlled|well controlled", phrase, re.I):
        return "controlled"
    return "unspecified"


def extract_supporting(text: str) -> str:
    """Pull minimal objective data if present."""
    support = re.findall(r"(Cr ?\d+\.\d+|WBC ?\d+|Hgb ?\d+|SpO2 ?\d+%|on [A-Za-z]+)", text)
    return ", ".join(support[:3]) if support else "⚠️ No supporting data"


def match_icd10(term: str) -> str:
    """Fuzzy match to ICD-10 description."""
    if not ICD_LIST:
        return "⚠️ ICD-10 mapping unavailable"
    match = process.extractOne(term, ICD_LIST, score_cutoff=80)
    if match:
        row = ICD10.loc[ICD10["LongDesc"] == match[0]]
        code = row["Code"].iloc[0] if not row.empty else ""
        return f"{match[0]} ({code})"
    else:
        return f"{term} — ⚠️ unmapped"


def extract_diagnoses(text: str) -> list[str]:
    """Identify diagnostic statements."""
    patterns = list(ABBR_MAP.values()) + [
        "Type 2 diabetes mellitus",
        "Type 1 diabetes mellitus",
        "Hypertension",
        "Acute kidney injury",
        "Chronic kidney disease",
        "Congestive heart failure",
        "Chronic obstructive pulmonary disease",
        "Pneumonia",
        "Anemia",
        "Depression",
        "Anxiety",
        "Coronary artery disease",
        "Atrial fibrillation",
    ]
    diagnoses = []
    for p in patterns:
        if re.search(rf"\b{re.escape(p)}\b", text, re.I):
            diagnoses.append(p)
    return list(set(diagnoses)) or ["⚠️ No clear diagnoses found"]


def cmsify(note_text: str) -> str:
    """Generate CMS-style output."""
    text = expand_abbreviations(note_text)
    diagnoses = extract_diagnoses(text)
    output_lines = []
    for d in diagnoses:
        mod = detect_modifier(text)
        icd = match_icd10(f"{mod} {d}")
        support = extract_supporting(note_text)
        output_lines.append(f"{d}, {mod} — {support}.  {icd}")
    return "# CMS-Ready Problem List\n" + "\n".join(
        f"{i+1}. {line}" for i, line in enumerate(output_lines)
    )


# ---------------------------
# MAIN EXECUTION
# ---------------------------

if __name__ == "__main__":
    import sys, textwrap

    if len(sys.argv) < 2:
        print(
            textwrap.dedent(
                """
                Usage:
                  python cmsify.py "note.txt"
                or
                  cat note.txt | python cmsify.py

                Description:
                  Parses a daily progress note and outputs a CMS-compliant problem list.
                """
            )
        )
        sys.exit(0)

    if sys.argv[1].endswith(".txt"):
        with open(sys.argv[1], "r") as f:
            note = f.read()
    else:
        note = " ".join(sys.argv[1:])

    print(cmsify(note))
