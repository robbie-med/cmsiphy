#!/usr/bin/env python3
"""
cms_output_rules.py
----------------------------------------------------------
Combines and prioritizes all modifier, complication, stage,
and contextual elements into a structured, CMS-compliant
diagnostic phrase hierarchy for output formatting.
"""

def assemble_cms_phrase(
    base_diagnosis: str,
    modifier: str = "unspecified",
    complication: str = "unspecified",
    stage: str = "unspecified",
    temporal: str = "unspecified",
    laterality: str = "unspecified",
    location: str = "unspecified",
    etiology: str = "unspecified",
    context: str = "unspecified",
    severity: str = "unspecified",
    supporting_data: str = "",
) -> str:
    """
    Assembles a single CMS-style diagnostic phrase with ordered elements.
    Each field is optional; 'unspecified' values are suppressed from output.
    """

    # -------------------------------
    # Helper function for conditional join
    # -------------------------------
    def add_if_present(label):
        return None if not label or label == "unspecified" else label

    parts = []

    # 1. Temporal / Modifier first (e.g. "acute", "chronic", "resolving")
    temporal_part = add_if_present(temporal) or add_if_present(modifier)
    if temporal_part:
        parts.append(temporal_part)

    # 2. Base diagnosis (core condition)
    parts.append(base_diagnosis.strip())

    # 3. Stage / Severity
    for piece in (add_if_present(stage), add_if_present(severity)):
        if piece and piece not in parts:
            parts.append(piece)

    # 4. Complication / Manifestation
    if add_if_present(complication):
        parts.append(f"with {complication}")

    # 5. Etiology / Context
    if add_if_present(etiology):
        if not etiology.startswith("with") and etiology not in ("unspecified", "none"):
            parts.append(f"due to {etiology}")

    # 6. Laterality + Location
    spatial = []
    if add_if_present(laterality):
        spatial.append(laterality)
    if add_if_present(location):
        spatial.append(location)
    if spatial:
        parts.append(" ".join(spatial))

    # 7. Context qualifiers
    if add_if_present(context) and context not in ("unspecified", "none"):
        parts.append(f"({context})")

    # 8. Join all descriptive parts
    diagnosis_phrase = " ".join(parts).strip()
    diagnosis_phrase = diagnosis_phrase[0].upper() + diagnosis_phrase[1:]

    # 9. Append supporting data if available
    if supporting_data:
        diagnosis_phrase += f" — {supporting_data}"

    return diagnosis_phrase


def build_cms_problem_list(problem_objects):
    """
    Takes a list of dicts, each containing problem components,
    and returns a formatted numbered CMS problem list string.
    Example item structure:
        {
            'diagnosis': 'pneumonia',
            'modifier': 'acute',
            'complication': 'sepsis',
            'stage': 'unspecified',
            'temporal': 'new onset',
            'laterality': 'right',
            'location': 'lung',
            'etiology': 'bacterial',
            'context': 'confirmed',
            'severity': 'moderate',
            'supporting_data': 'WBC 16.3, Temp 38.2C'
        }
    """
    lines = ["# CMS-Ready Problem List"]
    for idx, p in enumerate(problem_objects, start=1):
        phrase = assemble_cms_phrase(
            base_diagnosis=p.get("diagnosis", "unspecified"),
            modifier=p.get("modifier", "unspecified"),
            complication=p.get("complication", "unspecified"),
            stage=p.get("stage", "unspecified"),
            temporal=p.get("temporal", "unspecified"),
            laterality=p.get("laterality", "unspecified"),
            location=p.get("location", "unspecified"),
            etiology=p.get("etiology", "unspecified"),
            context=p.get("context", "unspecified"),
            severity=p.get("severity", "unspecified"),
            supporting_data=p.get("supporting_data", ""),
        )
        lines.append(f"{idx}. {phrase}")
    return "\n".join(lines)


if __name__ == "__main__":
    problems = [
        {
            "diagnosis": "pneumonia",
            "modifier": "acute",
            "complication": "sepsis",
            "stage": "unspecified",
            "temporal": "new onset",
            "laterality": "right",
            "location": "lung",
            "etiology": "bacterial",
            "context": "confirmed",
            "severity": "moderate",
            "supporting_data": "WBC 16.3, Temp 38.2C, on ceftriaxone",
        },
        {
            "diagnosis": "chronic kidney disease",
            "modifier": "chronic",
            "stage": "ckd stage 3",
            "complication": "unspecified",
            "temporal": "chronic stable",
            "laterality": "unspecified",
            "location": "renal",
            "etiology": "diabetic",
            "severity": "moderate",
            "supporting_data": "Cr 2.1, eGFR 36",
        },
        {
            "diagnosis": "heart failure",
            "modifier": "acute on chronic",
            "stage": "nyha class II",
            "severity": "moderate",
            "temporal": "acute exacerbation",
            "location": "heart",
            "complication": "unspecified",
            "etiology": "ischemic",
            "supporting_data": "BNP 480, O2 sat 90% on 2L",
        },
    ]

    print("\nCMS output assembly test run:\n" + "-" * 55)
    print(build_cms_problem_list(problems))
