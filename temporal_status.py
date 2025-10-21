#!/usr/bin/env python3
"""
temporal_status.py
----------------------------------------------------------
Detects temporal course or status descriptors in clinical text,
such as new onset, recurrent, resolving, history of, or chronic flare.
"""

import re

TEMPORAL_PATTERNS = {
    # --- New / Initial Onset ---
    "new_onset": [
        r"\bnew( onset)?\b",
        r"\bfirst episode\b",
        r"\binitial presentation\b",
        r"\brecent onset\b",
        r"\bnewly diagnosed\b",
    ],
    # --- Recurrent / Relapsing ---
    "recurrent": [
        r"\brecurr(ing|ent)\b",
        r"\brelaps(e|ing|ed)\b",
        r"\bflare(-up)?\b",
        r"\bbouts?\b",
        r"\brepeat episode\b",
    ],
    # --- Chronic Stable ---
    "chronic_stable": [
        r"\bchronic\b.*\bstable\b",
        r"\bstable chronic\b",
        r"\bat baseline\b",
        r"\bunchanged\b",
    ],
    # --- Resolving / Improving ---
    "resolving": [
        r"\bimprov(ing|ed)\b",
        r"\bresolv(ing|ed)\b",
        r"\brecover(ing|ed|y)\b",
        r"\bconvalescen(ce|t)\b",
    ],
    # --- Persistent / Unremitting ---
    "persistent": [
        r"\bpersistent\b",
        r"\bcontinu(ing|ous)\b",
        r"\bnon[- ]resolving\b",
        r"\bchronic active\b",
    ],
    # --- Exacerbation / Flare ---
    "acute_exacerbation": [
        r"\bacute exacerbation\b",
        r"\bflare\b",
        r"\bworsen(ing|ed)\b",
        r"\baggravat(ed|ion)\b",
        r"\bdecompensated\b",
    ],
    # --- Remission ---
    "remission": [
        r"\bin remission\b",
        r"\bno active disease\b",
        r"\bdisease free\b",
    ],
    # --- Relapse After Remission ---
    "relapse": [
        r"\brelaps(e|ed|ing)\b",
        r"\brecurr(ence|ent)\b after remission",
    ],
    # --- History / Past Episodes ---
    "history_of": [
        r"\bhx of\b",
        r"\bhistory of\b",
        r"\bprior\b",
        r"\bprevious episode\b",
        r"\bknown\b",
    ],
    # --- Post-Treatment or Post-Event ---
    "post_event": [
        r"\bpost[- ](MI|stroke|infection|surgery|procedure|partum|partum hemorrhage)\b",
        r"\bafter\b.*(event|illness|episode)\b",
    ],
}

TEMPORAL_PRIORITY = [
    "acute_exacerbation",
    "new_onset",
    "recurrent",
    "relapse",
    "resolving",
    "persistent",
    "chronic_stable",
    "remission",
    "post_event",
    "history_of",
]

def detect_temporal_status(text: str) -> str:
    """
    Scans input text for temporal or course descriptors.
    Returns the most specific label, or 'unspecified' if none found.
    """
    text = text.lower()
    for key in TEMPORAL_PRIORITY:
        for pattern in TEMPORAL_PATTERNS[key]:
            if re.search(pattern, text):
                return key.replace("_", " ")
    return "unspecified"


if __name__ == "__main__":
    test_cases = [
        "New onset atrial fibrillation",
        "Recurrent pneumonia with multiple prior episodes",
        "Chronic COPD, stable at baseline",
        "Resolving AKI with improving creatinine",
        "Persistent cough for 3 months",
        "Acute exacerbation of asthma",
        "In remission from ulcerative colitis",
        "Relapse of nephrotic syndrome after remission",
        "History of myocardial infarction",
        "Post-stroke dysphagia",
    ]

    print("\nTemporal status detection test run:\n" + "-" * 50)
    for t in test_cases:
        print(f"{t:<70} → {detect_temporal_status(t)}")
