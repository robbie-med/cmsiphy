#!/usr/bin/env python3
"""
severity_stage.py
CMSifier severity, stage, and class detection library
-----------------------------------------------------
Detects disease stage, severity, or class qualifiers
(e.g., CKD stages, NYHA class, COPD GOLD stage, anemia severity, etc.)
Version: 1.0
"""

import re

# ---------------------------------------------------------------------
# PATTERNS
# ---------------------------------------------------------------------

STAGING_PATTERNS = {
    # --- Chronic Kidney Disease ---
    "ckd_stage": [
        r"\bckd stage ?([1-5])\b",
        r"\bchronic kidney disease stage ?([1-5])\b",
        r"\bstage ?([1-5]) ?ckd\b",
    ],
    # --- Heart Failure NYHA Class ---
    "heart_failure_nyha": [
        r"\bnyha class ?(i{1,4}|\d)\b",
        r"\bclass ?(i{1,4}|\d) ?nyha\b",
    ],
    # --- COPD GOLD Stage ---
    "copd_gold": [
        r"\bgold (stage|class)? ?[A-D]\b",
        r"\bGOLD ?[A-D]\b",
    ],
    # --- Cancer Staging ---
    "cancer_stage": [
        r"\bstage ?[I|V|X]+[ABCD]?\b",
        r"\bT\d+[A-C]?\b",
        r"\bN\d+[A-C]?\b",
        r"\bM\d+[A-C]?\b",
    ],
    # --- Liver Disease ---
    "child_pugh": [
        r"\bchild[- ]pugh (class|score)? ?[A-C]\b",
    ],
    "meld_score": [
        r"\bmeld ?(score)? ?\d+\b",
    ],
    # --- Anemia Severity ---
    "anemia_severity": [
        r"\bmild anemia\b",
        r"\bmoderate anemia\b",
        r"\bsevere anemia\b",
    ],
    # --- Hypertension ---
    "hypertension_stage": [
        r"\bstage ?1 hypertension\b",
        r"\bstage ?2 hypertension\b",
        r"\bhypertensive (urgency|emergency)\b",
    ],
    # --- Obesity (BMI / Class) ---
    "obesity_class": [
        r"\bobesit(y|ic)\b",
        r"\bobese\b",
        r"\bBMI ?(\d{2,3}\.?\d*)\b",
        r"\bclass ?(1|2|3) obesity\b",
    ],
    # --- Pain Severity ---
    "pain_severity": [
        r"\bmild pain\b",
        r"\bmoderate pain\b",
        r"\bsevere pain\b",
        r"\b10/10 pain\b",
    ],
    # --- COPD Severity (Non-GOLD) ---
    "copd_severity": [
        r"\bmild COPD\b",
        r"\bmoderate COPD\b",
        r"\bsevere COPD\b",
    ],
    # --- Pressure Ulcer Stages ---
    "pressure_ulcer_stage": [
        r"\b(stage ?[1-4]) pressure ulcer\b",
        r"\bpressure ulcer, stage ?[1-4]\b",
        r"\bdeep tissue injury\b",
        r"\bunstageable pressure injury\b",
    ],
    # --- Liver Fibrosis (Metavir) ---
    "fibrosis_stage": [
        r"\bfibrosis stage ?[0-4]\b",
        r"\bmetavir ?(score|stage)? ?[0-4]\b",
    ],
}

# ---------------------------------------------------------------------
# PRIORITY ORDER
# ---------------------------------------------------------------------

STAGING_PRIORITY = [
    "ckd_stage",
    "heart_failure_nyha",
    "copd_gold",
    "cancer_stage",
    "child_pugh",
    "meld_score",
    "pressure_ulcer_stage",
    "fibrosis_stage",
    "anemia_severity",
    "hypertension_stage",
    "obesity_class",
    "copd_severity",
    "pain_severity",
]

# ---------------------------------------------------------------------
# DETECTION FUNCTION
# ---------------------------------------------------------------------

def detect_stage_or_severity(text: str) -> str:
    """
    Scans input text for stage, severity, or class indicators.
    Returns the best-matching label string or 'unspecified'.
    """
    text = text.lower()
    for key in STAGING_PRIORITY:
        for pattern in STAGING_PATTERNS[key]:
            if re.search(pattern, text):
                return key.replace("_", " ")
    return "unspecified"

# ---------------------------------------------------------------------
# TEST HARNESS
# ---------------------------------------------------------------------

if __name__ == "__main__":
    test_cases = [
        "CKD stage 3b",
        "NYHA class II heart failure",
        "GOLD B COPD",
        "Stage IVB breast carcinoma",
        "Child-Pugh B cirrhosis",
        "MELD score 23",
        "Moderate anemia",
        "Hypertensive urgency",
        "BMI 34 class 1 obesity",
        "Severe pain 10/10",
        "Stage 2 pressure ulcer on heel",
        "Fibrosis stage 3 (Metavir F3)",
    ]

    print("\nSeverity/staging detection test run:\n" + "-" * 50)
    for t in test_cases:
        print(f"{t:<70} → {detect_stage_or_severity(t)}")
