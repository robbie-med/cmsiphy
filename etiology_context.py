#!/usr/bin/env python3
"""
etiology_context.py
CMSifier etiology and causal relationship detection library
------------------------------------------------------------
Detects etiologic or contextual qualifiers in clinical text,
including “due to,” “secondary to,” “iatrogenic,” “alcohol-related,”
“postoperative,” “drug-induced,” etc.
Version: 1.0
"""

import re

ETIOLOGY_PATTERNS = {
    # General causal phrases
    "secondary_to": [
        r"\bsecondary to\b",
        r"\bdue to\b",
        r"\bcaused by\b",
        r"\bresult(ing)? from\b",
        r"\bfollowing\b",
        r"\bassociated with\b",
    ],
    # Post-procedural / iatrogenic
    "postoperative": [
        r"\bpost[- ]?op(erative)?\b",
        r"\bafter surgery\b",
        r"\bfollowing procedure\b",
        r"\bpost[- ]?(surgical|laparotomy|cholecystectomy|hysterectomy|appendectomy|delivery)\b",
    ],
    "iatrogenic": [
        r"\biatrogenic\b",
        r"\bprocedure[- ]related\b",
        r"\bdevice[- ]related\b",
        r"\bPICC[- ]related\b",
        r"\bcatheter[- ]associated\b",
        r"\binfusion[- ]related\b",
    ],
    # Substance-related
    "alcohol_related": [
        r"\balcohol( use| abuse| related| dependence)?\b",
        r"\betalcoholic (hepatitis|cirrhosis|neuropathy|cardiomyopathy)\b",
    ],
    "drug_induced": [
        r"\bdrug[- ]induced\b",
        r"\bmedication[- ]induced\b",
        r"\bNSAID[- ]related\b",
        r"\bopioid[- ]induced\b",
        r"\bsteroid[- ]induced\b",
        r"\bACE[- ]inhibitor[- ]induced\b",
        r"\bamiodarone[- ]induced\b",
        r"\bchemo(therapy)?[- ]induced\b",
    ],
    "radiation_induced": [
        r"\bradiation[- ]induced\b",
        r"\bpost[- ]radiation\b",
        r"\bafter radiation\b",
    ],
    "ischemic": [
        r"\bischemic\b",
        r"\bdue to ischemia\b",
        r"\bvascular\b",
        r"\bthrombo(tic|embolic)\b",
        r"\bembol(ic|ism)\b",
    ],
    "autoimmune": [
        r"\bautoimmune\b",
        r"\bimmune[- ]mediated\b",
        r"\blupus\b",
        r"\bSLE\b",
        r"\bRA\b",
        r"\bscleroderma\b",
        r"\bvasculitis\b",
    ],
    "infectious": [
        r"\binfect(ed|ion)\b",
        r"\bviral\b",
        r"\bbacterial\b",
        r"\bfungal\b",
        r"\bseptic\b",
        r"\bpost[- ]infectious\b",
    ],
    "metabolic": [
        r"\bmetabolic\b",
        r"\bdiabetic\b",
        r"\bketoacidosis\b",
        r"\bhyperglycemia\b",
        r"\bhyperkalemia\b",
        r"\bhypokalemia\b",
        r"\bhypoglycemia\b",
    ],
    "obstetric": [
        r"\bpostpartum\b",
        r"\bperipartum\b",
        r"\bantepartum\b",
        r"\bpregnancy[- ]related\b",
        r"\bpreeclampsia\b",
    ],
    "traumatic": [
        r"\btraumatic\b",
        r"\bpost[- ]traumatic\b",
        r"\bMVC\b",
        r"\bfall\b",
        r"\bblunt\b",
        r"\bGSW\b",
        r"\bstab\b",
    ],
    "hereditary": [
        r"\bgenetic\b",
        r"\bhereditary\b",
        r"\bfamilial\b",
        r"\binherited\b",
    ],
    "neoplastic": [
        r"\bneoplas(tic|m)\b",
        r"\bmalignan(t|cy)\b",
        r"\btumor\b",
        r"\bcarcinoma\b",
        r"\bsarcoma\b",
        r"\blymphoma\b",
    ],
    "idiopathic": [
        r"\bidiopathic\b",
        r"\bunknown cause\b",
        r"\bno identifiable cause\b",
        r"\bprimary\b(?! hypertension)",
    ],
    "congenital": [
        r"\bcongenital\b",
        r"\bbirth defect\b",
        r"\bfrom birth\b",
    ],
}

ETIOLOGY_PRIORITY = [
    "secondary_to",
    "iatrogenic",
    "postoperative",
    "drug_induced",
    "radiation_induced",
    "alcohol_related",
    "autoimmune",
    "infectious",
    "metabolic",
    "ischemic",
    "traumatic",
    "obstetric",
    "neoplastic",
    "hereditary",
    "congenital",
    "idiopathic",
]

def detect_etiology(text: str) -> str:
    """
    Scans text for etiologic or contextual qualifiers.
    Returns the most specific label, or 'unspecified' if none found.
    """
    text = text.lower()
    for key in ETIOLOGY_PRIORITY:
        for pattern in ETIOLOGY_PATTERNS[key]:
            if re.search(pattern, text):
                return key.replace("_", " ")
    return "unspecified"


if __name__ == "__main__":
    test_cases = [
        "Pneumonia secondary to aspiration",
        "Postoperative ileus after cholecystectomy",
        "Iatrogenic pneumothorax following central line",
        "Alcoholic hepatitis due to chronic alcohol use",
        "Steroid-induced hyperglycemia",
        "Radiation-induced dermatitis",
        "Ischemic stroke due to thromboembolism",
        "Autoimmune hemolytic anemia",
        "Postpartum thyroiditis",
        "Blunt abdominal trauma with splenic laceration",
        "Familial hypercholesterolemia",
        "Malignant neoplasm of colon",
        "Idiopathic pulmonary fibrosis",
        "Congenital heart defect",
    ]

    print("\nEtiology/context detection test run:\n" + "-" * 50)
    for t in test_cases:
        print(f"{t:<70} → {detect_etiology(t)}")
