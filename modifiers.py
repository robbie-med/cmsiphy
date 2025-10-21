#!/usr/bin/env python3
"""
modifiers.py
CMSifier modifier detection library
-----------------------------------
Contains regex-based rules to detect problem modifiers, acuity, and control/status
from clinical text phrases.

Version: 1.0
"""

import re

# Each category below defines regex patterns that signal a CMS-relevant modifier.

# ---------------------------
# MODIFIER PATTERN DICTIONARIES
# ---------------------------

MODIFIER_PATTERNS = {
    "acute": [
        r"\bacute(?! on chronic)\b",
        r"\bsudden\b",
        r"\bnew( onset)?\b",
        r"\b(abrupt|rapid|recent) onset\b",
    ],
    "chronic": [
        r"\bchronic\b",
        r"\bhx of\b",
        r"\bhistory of\b",
        r"\blong[- ]standing\b",
        r"\bpersistent\b",
    ],
    "acute_on_chronic": [
        r"\bacute on chronic\b",
        r"\bacute[- ]and[- ]chronic\b",
        r"\bexacerbation of chronic\b",
    ],
    "resolving": [
        r"\bimprov(ing|ed)\b",
        r"\bresolv(ing|ed)\b",
        r"\brecover(ing|y)\b",
    ],
    "controlled": [
        r"\bwell[- ]?controlled\b",
        r"\badequately controlled\b",
        r"\bcontrolled\b",
        r"\bat goal\b",
    ],
    "uncontrolled": [
        r"\bpoorly controlled\b",
        r"\buncontrolled\b",
        r"\bsuboptimally controlled\b",
        r"\bout of control\b",
    ],
    "compensated": [
        r"\bcompensated\b",
        r"\bstable\b",
        r"\bbaseline\b",
    ],
    "decompensated": [
        r"\bdecompensated\b",
        r"\bexacerbation\b",
        r"\bworsen(ing|ed)\b",
        r"\bflare\b",
        r"\bdeteriorat(ing|ed|ion)\b",
    ],
    "infectious": [
        r"\binfect(ed|ion)\b",
        r"\bsepsis\b",
        r"\binflam(mation|ed)\b",
    ],
    "neoplastic": [
        r"\bcancer\b",
        r"\bmalignan(t|cy)\b",
        r"\btumor\b",
        r"\bmetasta(sis|tic)\b",
    ],
    "traumatic": [
        r"\btrauma\b",
        r"\bfracture\b",
        r"\blaceration\b",
        r"\bcontusion\b",
    ],
    "unspecified": [
        r"\bunspecified\b",
        r"\bnot specified\b",
        r"\bunknown\b",
        r"\bunclear\b",
    ],
}

# Priority order — if multiple modifiers match, this determines which one wins.
MODIFIER_PRIORITY = [
    "acute_on_chronic",
    "acute",
    "chronic",
    "decompensated",
    "controlled",
    "uncontrolled",
    "resolving",
    "compensated",
    "infectious",
    "neoplastic",
    "traumatic",
    "unspecified",
]

# ---------------------------
# DETECTION FUNCTION
# ---------------------------

def detect_modifier(text: str) -> str:
    """
    Scans input text and returns the highest-priority modifier label.
    Returns 'unspecified' if nothing matches.
    """
    text = text.lower()
    for key in MODIFIER_PRIORITY:
        for pattern in MODIFIER_PATTERNS[key]:
            if re.search(pattern, text):
                return key
    return "unspecified"


# ---------------------------
# TESTING BLOCK
# ---------------------------

if __name__ == "__main__":
    test_cases = [
        "acute kidney injury improving",
        "chronic hypertension at baseline",
        "acute on chronic systolic heart failure",
        "uncontrolled DM2 with hyperglycemia",
        "decompensated cirrhosis with ascites",
        "hx of COPD, stable",
        "pneumonia unspecified",
    ]

    for t in test_cases:
        print(f"{t:<60} → {detect_modifier(t)}")
