#!/usr/bin/env python3
"""
supporting_data_rules.py
----------------------------------------------------------
Extracts minimal structured supporting data from clinical text:
labs, vitals, imaging references, or treatment markers that
objectively substantiate a diagnosis for CMS documentation.
"""

import re

# ---------------------------------------------------------------------
# PATTERN DICTIONARIES
# ---------------------------------------------------------------------

LAB_PATTERNS = {
    "renal": [
        r"\bCr( ?=|:)? ?\d+(\.\d+)?\b",
        r"\bcreatinine( level)?( ?=|:)? ?\d+(\.\d+)?\b",
        r"\bBUN( ?=|:)? ?\d+\b",
    ],
    "electrolytes": [
        r"\bNa( ?=|:)? ?\d+\b",
        r"\bK( ?=|:)? ?\d+\b",
        r"\bCl( ?=|:)? ?\d+\b",
        r"\bCO2( ?=|:)? ?\d+\b",
        r"\bbicarb( ?=|:)? ?\d+\b",
    ],
    "cbc": [
        r"\bWBC( ?=|:)? ?\d+(\.\d+)?\b",
        r"\bHgb( ?=|:)? ?\d+(\.\d+)?\b",
        r"\bHct( ?=|:)? ?\d+(\.\d+)?\b",
        r"\bplatelets?( ?=|:)? ?\d+\b",
    ],
    "liver": [
        r"\bAST( ?=|:)? ?\d+\b",
        r"\bALT( ?=|:)? ?\d+\b",
        r"\bbili(rubin)?( ?=|:)? ?\d+(\.\d+)?\b",
        r"\balk phos( ?=|:)? ?\d+\b",
    ],
    "glucose": [
        r"\bglucose( ?=|:)? ?\d+\b",
        r"\bblood sugar( ?=|:)? ?\d+\b",
    ],
    "infection_inflammation": [
        r"\bCRP( ?=|:)? ?\d+\b",
        r"\bESR( ?=|:)? ?\d+\b",
        r"\bprocalcitonin( ?=|:)? ?\d+(\.\d+)?\b",
        r"\blactate( ?=|:)? ?\d+(\.\d+)?\b",
    ],
    "coags": [
        r"\bINR( ?=|:)? ?\d+(\.\d+)?\b",
        r"\bPT( ?=|:)? ?\d+\b",
        r"\bPTT( ?=|:)? ?\d+\b",
    ],
}

VITAL_PATTERNS = {
    "temperature": [
        r"\bT( ?=|:)? ?\d+(\.\d+)?( ?[CF])?\b",
        r"\btemp(erature)?( ?=|:)? ?\d+(\.\d+)?\b",
    ],
    "blood_pressure": [
        r"\bBP( ?=|:)? ?\d{2,3}/\d{2,3}\b",
        r"\bblood pressure\b",
    ],
    "heart_rate": [
        r"\bHR( ?=|:)? ?\d+\b",
        r"\bpulse( ?=|:)? ?\d+\b",
    ],
    "resp_rate": [
        r"\bRR( ?=|:)? ?\d+\b",
        r"\bresp(iration| rate)?( ?=|:)? ?\d+\b",
    ],
    "oxygen": [
        r"\bSpO2( ?=|:)? ?\d+%?\b",
        r"\bO2 sat(uration)?( ?=|:)? ?\d+%?\b",
        r"\bon (room air|RA|oxygen|NC|nasal cannula)\b",
    ],
    "weight": [
        r"\bweight( ?=|:)? ?\d+(\.\d+)? ?(kg|lb|lbs)?\b",
    ],
}

IMAGING_PATTERNS = {
    "xray": [
        r"\bX[- ]?ray\b",
        r"\bradiograph\b",
    ],
    "ct": [
        r"\bCT( scan)?\b",
        r"\bcomputed tomography\b",
    ],
    "mri": [
        r"\bMRI\b",
        r"\bmagnetic resonance\b",
    ],
    "ultrasound": [
        r"\bultrasound\b",
        r"\bUS\b",
        r"\bsonogram\b",
    ],
    "echo": [
        r"\bechocardiogram\b",
        r"\becho\b",
    ],
    "cxr_findings": [
        r"\bpneumonia\b",
        r"\binfiltrate\b",
        r"\bconsolidation\b",
        r"\bpleural effusion\b",
    ],
}

TREATMENT_MARKERS = {
    "antibiotic": [
        r"\bon (ceftriaxone|zosyn|vanco(mycin)?|azithro(mycin)?|levofloxacin|augmentin|amox|penicillin|doxycycline)\b",
    ],
    "diuretic": [
        r"\bon (lasix|furosemide|torsemide|bumetanide)\b",
    ],
    "insulin": [
        r"\bon insulin\b",
        r"\binsulin (glargine|lispro|aspart|detemir|NPH)\b",
    ],
    "oxygen_therapy": [
        r"\bon (oxygen|O2|NC|nasal cannula|high[- ]flow)\b",
        r"\brequiring oxygen\b",
    ],
    "ventilation": [
        r"\bmechanical ventilation\b",
        r"\bintubated\b",
        r"\bon ventilator\b",
    ],
}

# ---------------------------------------------------------------------
# EXTRACTION FUNCTION
# ---------------------------------------------------------------------

def extract_supporting_data(text: str, max_items: int = 4) -> str:
    """
    Extracts minimal but objective supporting data from text.
    Returns a short comma-separated string.
    """
    text = text.lower()
    findings = set()

    for group in (LAB_PATTERNS, VITAL_PATTERNS, IMAGING_PATTERNS, TREATMENT_MARKERS):
        for category, patterns in group.items():
            for pattern in patterns:
                matches = re.findall(pattern, text)
                for m in matches:
                    val = m[0] if isinstance(m, tuple) else m
                    findings.add(val.strip())

    if not findings:
        return "⚠️ No supporting data"
    return ", ".join(sorted(list(findings))[:max_items])

# ---------------------------------------------------------------------
# TEST HARNESS
# ---------------------------------------------------------------------

if __name__ == "__main__":
    test_notes = [
        "Temp 38.2C, HR 110, BP 98/62, SpO2 92% on 2L NC. WBC 16.3, lactate 3.2, on ceftriaxone.",
        "Cr 2.1 from baseline 1.0, BUN 38. K 3.2. On lasix and torsemide.",
        "CT chest shows bilateral infiltrates. O2 sat 88% RA.",
        "MRI brain reveals ischemic infarct. INR 3.1.",
        "Glucose 340, on insulin glargine. Hgb 9.2. O2 sat 94% on RA.",
    ]

    print("\nSupporting data extraction test run:\n" + "-" * 55)
    for t in test_notes:
        print(f"{t:<90} → {extract_supporting_data(t)}")
