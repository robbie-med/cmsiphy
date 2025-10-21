#!/usr/bin/env python3
"""
context_flags.py
----------------------------------------------------------
Detects contextual or certainty qualifiers in documentation:
suspected, probable, ruled out, denied, unclear, etc.
Used to flag diagnostic certainty for CMS-compliant phrasing.
"""

import re

CONTEXT_PATTERNS = {
    # --- Uncertainty / Probability ---
    "possible": [
        r"\bpossible\b",
        r"\bprobable\b",
        r"\blikely\b",
        r"\bsusp(ect|ected|icion of)\b",
        r"\bconsider(ing|ed)?\b",
        r"\brule[- ]?in\b",
        r"\bawaiting confirmation\b",
    ],
    # --- Ruled Out / Negative Findings ---
    "ruled_out": [
        r"\bruled out\b",
        r"\bno evidence of\b",
        r"\bnot consistent with\b",
        r"\bnegative for\b",
        r"\bworkup negative\b",
        r"\bdenies\b",
        r"\bwithout (signs|evidence) of\b",
    ],
    # --- Confirmed / Established ---
    "confirmed": [
        r"\bconfirmed\b",
        r"\bproven\b",
        r"\bdocumented\b",
        r"\bdiagnosed\b",
        r"\bverified\b",
        r"\bclear evidence of\b",
        r"\bpositive for\b",
    ],
    # --- Differential / Working Diagnoses ---
    "differential": [
        r"\bdifferential includes\b",
        r"\bdiff dx\b",
        r"\brule[- ]?out list\b",
        r"\bconsider\b.*(versus|vs)\b",
    ],
    # --- Pending Evaluation ---
    "pending": [
        r"\bpending\b",
        r"\bawaiting results\b",
        r"\bresults pending\b",
        r"\bto be determined\b",
        r"\bawaiting (labs|imaging|pathology)\b",
    ],
    # --- Inadequate Documentation / Unclear ---
    "insufficient_data": [
        r"\bunclear\b",
        r"\bnot specified\b",
        r"\bunspecified\b",
        r"\binsufficient\b",
        r"\bnot documented\b",
        r"\bunknown\b",
        r"\bTBD\b",
    ],
    # --- Historical / Resolved Context ---
    "historical": [
        r"\bhx of\b",
        r"\bhistory of\b",
        r"\bpreviously had\b",
        r"\bresolved\b",
        r"\btreated\b",
        r"\bpast\b",
    ],
    # --- Relational Context (Attribution) ---
    "secondary_condition": [
        r"\bsecondary condition\b",
        r"\bcomorbid\b",
        r"\bco-existing\b",
    ],
}

CONTEXT_PRIORITY = [
    "confirmed",
    "possible",
    "ruled_out",
    "pending",
    "differential",
    "insufficient_data",
    "historical",
    "secondary_condition",
]


def detect_context(text: str) -> str:
    """
    Scans text for context or certainty indicators.
    Returns one of: confirmed, possible, ruled_out, pending,
    differential, insufficient_data, historical, or unspecified.
    """
    text = text.lower()
    for key in CONTEXT_PRIORITY:
        for pattern in CONTEXT_PATTERNS[key]:
            if re.search(pattern, text):
                return key
    return "unspecified"


if __name__ == "__main__":
    test_cases = [
        "Possible pneumonia, will obtain CXR",
        "Rule out PE",
        "Sepsis confirmed by blood cultures",
        "UTI pending culture results",
        "Workup negative for DVT",
        "Differential includes pneumonia versus CHF",
        "Unclear etiology of AKI",
        "History of asthma, currently resolved",
        "Comorbid diabetes mellitus",
    ]

    print("\nContext flag detection test run:\n" + "-" * 55)
    for t in test_cases:
        print(f"{t:<70} → {detect_context(t)}")
