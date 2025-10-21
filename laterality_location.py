#!/usr/bin/env python3
"""
laterality_location.py
----------------------------------------------------------
Detects laterality (right/left/bilateral) and anatomical
location/site references from clinical text to enhance
diagnostic specificity.
"""

import re

LATERALITY_PATTERNS = {
    "right": [
        r"\bright\b",
        r"\brt\b",
        r"\br[- ]sided\b",
        r"\br-hand(ed)?\b",
    ],
    "left": [
        r"\bleft\b",
        r"\blt\b",
        r"\bl[- ]sided\b",
        r"\bl-hand(ed)?\b",
    ],
    "bilateral": [
        r"\bbilateral\b",
        r"\bbilat(eral)?\b",
        r"\bboth\b",
        r"\btwo[- ]sided\b",
    ],
    "midline": [
        r"\bmidline\b",
        r"\bcentral\b",
        r"\btracheal midline\b",
    ],
    "unspecified": [
        r"\bunspecified side\b",
        r"\bnot specified\b",
        r"\bunclear side\b",
    ],
}

LOCATION_PATTERNS = {
    "head_neck": [
        r"\bhead\b",
        r"\bneck\b",
        r"\bthroat\b",
        r"\bface\b",
        r"\bscalp\b",
    ],
    "chest_lung": [
        r"\bchest\b",
        r"\blung(s)?\b",
        r"\bpulmon(ar|ic)\b",
        r"\bpleur(a|al)\b",
    ],
    "heart_cardiac": [
        r"\bheart\b",
        r"\bcardiac\b",
        r"\bmyocard(ial|ium)\b",
        r"\bpericard(itis|ium)\b",
    ],
    "abdomen_gi": [
        r"\babdomen\b",
        r"\babdominal\b",
        r"\bliver\b",
        r"\bhepatic\b",
        r"\bspleen\b",
        r"\bpancreas\b",
        r"\bstomach\b",
        r"\bgallbladder\b",
        r"\bcolon\b",
        r"\bintestin(al|e)\b",
    ],
    "renal_genitourinary": [
        r"\bkidney(s)?\b",
        r"\brenal\b",
        r"\bureter(s)?\b",
        r"\bbladder\b",
        r"\burethra\b",
        r"\btest(icle|is|es)\b",
        r"\bovary|ovarian\b",
        r"\buter(us|ine)\b",
        r"\bprostat(e|ic)\b",
    ],
    "extremities": [
        r"\barm(s)?\b",
        r"\bleg(s)?\b",
        r"\bextremit(y|ies)\b",
        r"\bupper limb\b",
        r"\blower limb\b",
    ],
    "upper_extremity": [
        r"\bshoulder\b",
        r"\belbow\b",
        r"\bforearm\b",
        r"\bhand(s)?\b",
        r"\bwrist\b",
        r"\bfinger(s)?\b",
    ],
    "lower_extremity": [
        r"\bhip\b",
        r"\bthigh\b",
        r"\bknee\b",
        r"\bleg\b",
        r"\bcalf\b",
        r"\bfoot\b",
        r"\btoe(s)?\b",
        r"\bheel\b",
        r"\bankle\b",
    ],
    "spine": [
        r"\bspine\b",
        r"\bspinal\b",
        r"\bcervical\b",
        r"\bthoracic\b",
        r"\blumbar\b",
        r"\bsacral\b",
    ],
    "skin_soft_tissue": [
        r"\bskin\b",
        r"\bsoft tissue\b",
        r"\bsubcutaneous\b",
        r"\bdermal\b",
        r"\bcutaneous\b",
    ],
    "neuro_cns": [
        r"\bbrain\b",
        r"\bcerebr(al|um)\b",
        r"\bcerebellum\b",
        r"\bmening(es|itis)\b",
        r"\bCNS\b",
        r"\bspinal cord\b",
    ],
    "vascular": [
        r"\barter(y|ies)\b",
        r"\bvein(s)?\b",
        r"\bvascular\b",
        r"\bAV\b",
        r"\baort(a|ic)\b",
        r"\bcarotid\b",
        r"\bfemoral\b",
        r"\bpopliteal\b",
    ],
    "musculoskeletal": [
        r"\bmuscle(s)?\b",
        r"\btendon(s)?\b",
        r"\bbone(s)?\b",
        r"\bjoint(s)?\b",
        r"\bskeletal\b",
        r"\bosseous\b",
    ],
}

LATERALITY_PRIORITY = ["bilateral", "right", "left", "midline", "unspecified"]
LOCATION_PRIORITY = [
    "head_neck",
    "chest_lung",
    "heart_cardiac",
    "abdomen_gi",
    "renal_genitourinary",
    "upper_extremity",
    "lower_extremity",
    "extremities",
    "spine",
    "skin_soft_tissue",
    "neuro_cns",
    "vascular",
    "musculoskeletal",
]

def detect_laterality(text: str) -> str:
    """
    Detects laterality markers in text.
    Returns 'unspecified' if none found.
    """
    text = text.lower()
    for key in LATERALITY_PRIORITY:
        for pattern in LATERALITY_PATTERNS[key]:
            if re.search(pattern, text):
                return key
    return "unspecified"


def detect_location(text: str) -> str:
    """
    Detects anatomical site/location terms.
    Returns 'unspecified' if none found.
    """
    text = text.lower()
    for key in LOCATION_PRIORITY:
        for pattern in LOCATION_PATTERNS[key]:
            if re.search(pattern, text):
                return key.replace("_", " ")
    return "unspecified"


if __name__ == "__main__":
    test_cases = [
        "Right lower lobe pneumonia",
        "Left knee osteoarthritis",
        "Bilateral lower extremity edema",
        "Midline neck mass",
        "Thoracic spine pain",
        "Right arm cellulitis",
        "Chronic kidney disease of left kidney",
        "Fracture of right femur",
        "Bilateral pleural effusions",
        "Skin ulcer on left heel",
    ]

    print("\nLaterality/location detection test run:\n" + "-" * 55)
    for t in test_cases:
        print(f"{t:<70} → Laterality: {detect_laterality(t):<12} | Location: {detect_location(t)}")
