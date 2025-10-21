#!/usr/bin/env python3
"""
complications.py
CMSifier complication and manifestation detection library
----------------------------------------------------------
Detects diagnostic qualifiers indicating complications,
manifestations, or systemic involvement, e.g.:
    - "with nephropathy", "with retinopathy"
    - "with sepsis", "with ascites"
    - "with ulcer", "with anemia"
    - "without complication"
Version: 1.0
"""

import re

# ---------------------------------------------------------------------
# COMPLICATION PATTERN DICTIONARY
# ---------------------------------------------------------------------
# Keys are conceptual complication types; values are lists of regex patterns
# that match natural clinical language expressions.

COMPLICATION_PATTERNS = {
    # ---------------- Diabetes-related ----------------
    "diabetic_nephropathy": [
        r"\bwith\b.*\bnephropathy\b",
        r"\bdiabetic nephropathy\b",
        r"\bproteinur(ia|ic)\b",
        r"\bmicroalbuminur(ia|ic)\b",
    ],
    "diabetic_retinopathy": [
        r"\bwith\b.*\bretinopathy\b",
        r"\bdiabetic retinopathy\b",
        r"\bmacular edema\b",
        r"\bbackground retinopathy\b",
    ],
    "diabetic_neuropathy": [
        r"\bwith\b.*\bneuropath(y|ic)\b",
        r"\bdiabetic neuropathy\b",
        r"\bpolyneuropathy\b",
        r"\bparesthesia(s)?\b",
    ],
    "diabetic_foot_ulcer": [
        r"\bfoot ulcer\b",
        r"\bulcer(ation)? of (toe|foot|heel|ankle)\b",
        r"\bwith\b.*\bulcer\b",
    ],
    "diabetic_angio": [
        r"\bangiopath(y|ic)\b",
        r"\bperipheral vascular disease\b",
        r"\bPVD\b",
    ],
    # ---------------- Infection / sepsis ----------------
    "infection": [
        r"\bwith infection\b",
        r"\binfect(ed|ion)\b",
        r"\bcellulitis\b",
        r"\bosteomyelitis\b",
    ],
    "sepsis": [
        r"\bsepsis\b",
        r"\bseptic\b",
        r"\bbacteremia\b",
        r"\burosepsis\b",
    ],
    # ---------------- Systemic / organ complications ----------------
    "cardiac": [
        r"\bwith (CHF|heart failure|cardiomyopath(y|ic))\b",
        r"\bischemic\b",
        r"\bcoronary\b",
    ],
    "renal": [
        r"\bAKI\b",
        r"\brenal failure\b",
        r"\bESRD\b",
        r"\bdialysis\b",
    ],
    "hepatic": [
        r"\bwith (cirrhosis|ascites|encephalopathy|jaundice)\b",
        r"\bhepatic\b",
        r"\bliver (failure|disease)\b",
    ],
    "respiratory": [
        r"\bwith (pneumonia|ARDS|bronchospasm|asthma)\b",
        r"\brespiratory failure\b",
    ],
    "hematologic": [
        r"\banemia\b",
        r"\bleukopenia\b",
        r"\bthrombocytopenia\b",
        r"\bcoagulopathy\b",
    ],
    "neurologic": [
        r"\bencephalopath(y|ic)\b",
        r"\bseizure(s)?\b",
        r"\bstroke\b",
        r"\bCVA\b",
        r"\bTIA\b",
    ],
    "dermatologic": [
        r"\bpressure ulcer\b",
        r"\bskin breakdown\b",
        r"\bcellulitis\b",
        r"\bgangrene\b",
    ],
    # ---------------- Pregnancy / OB ----------------
    "pregnancy_related": [
        r"\bpreeclampsia\b",
        r"\bHELLP\b",
        r"\bpostpartum hemorrhage\b",
        r"\bchorioamnionitis\b",
    ],
    # ---------------- Generic complication markers ----------------
    "with_complication": [
        r"\bwith complication(s)?\b",
        r"\bcomplicat(ed|ion)\b",
    ],
    "without_complication": [
        r"\bwithout complication(s)?\b",
        r"\bno complication(s)?\b",
        r"\bwithout manifestation(s)?\b",
        r"\bno evidence of complication\b",
    ],
    # ---------------- Metabolic / endocrine ----------------
    "metabolic": [
        r"\bketoacidosis\b",
        r"\bhyperosmolar\b",
        r"\bhypoglycemia\b",
        r"\bhyperglycemia\b",
        r"\belectrolyte (imbalance|abnormalit(y|ies))\b",
    ],
}

# ---------------------------------------------------------------------
# PRIORITY ORDER
# ---------------------------------------------------------------------
# More specific matches are checked first.
COMPLICATION_PRIORITY = [
    "diabetic_nephropathy",
    "diabetic_retinopathy",
    "diabetic_neuropathy",
    "diabetic_foot_ulcer",
    "diabetic_angio",
    "infection",
    "sepsis",
    "cardiac",
    "renal",
    "hepatic",
    "respiratory",
    "hematologic",
    "neurologic",
    "dermatologic",
    "pregnancy_related",
    "metabolic",
    "with_complication",
    "without_complication",
]

# ---------------------------------------------------------------------
# DETECTION FUNCTION
# ---------------------------------------------------------------------

def detect_complication(text: str) -> str:
    """
    Scans input text and returns a complication label string.
    Returns 'unspecified' if none detected.
    """
    text = text.lower()
    for key in COMPLICATION_PRIORITY:
        for pattern in COMPLICATION_PATTERNS[key]:
            if re.search(pattern, text):
                # Pretty-format output
                return key.replace("_", " ")
    return "unspecified"

# ---------------------------------------------------------------------
# TEST HARNESS
# ---------------------------------------------------------------------

if __name__ == "__main__":
    test_cases = [
        "Type 2 diabetes with nephropathy and microalbuminuria",
        "Type 2 diabetes with retinopathy",
        "Diabetic foot ulcer on right heel",
        "Sepsis secondary to UTI",
        "Hypertension with heart failure",
        "Cirrhosis with ascites",
        "AKI with metabolic acidosis",
        "Type 2 diabetes without complication",
        "COPD with pneumonia",
        "Anemia unspecified",
        "HELLP syndrome postpartum",
        "DKA with hyperglycemia",
        "Pressure ulcer on coccyx",
    ]

    print("\nComplication detection test run:\n" + "-" * 45)
    for t in test_cases:
        print(f"{t:<60} → {detect_complication(t)}")
