# cmsiphy
A local app to cmsify your notes 

⸻

🧰 How to Use It
	1.	Install dependencies (once):

pip install pandas rapidfuzz


	2.	Download ICD-10 codes (from CMS.gov):
	•	Go to https://www.cms.gov/medicare/icd-10/2025-icd-10-cm
	•	Extract the CSV (e.g., icd10cm_codes.csv) into the same folder as the script.
	3.	Run it:

python cmsify.py note.txt

or

cat note.txt | python cmsify.py



⸻

🧪 Example

note.txt

DM2 on metformin, sugars okay. Mild AKI likely prerenal. COPD stable on inhalers.

Output

# CMS-Ready Problem List
1. Type 2 diabetes mellitus, unspecified — on metformin, glucose stable.  Type 2 diabetes mellitus without complication (E11.9)
2. Acute kidney injury, unspecified — ⚠️ No supporting data.  Acute kidney failure, unspecified (N17.9)
3. Chronic obstructive pulmonary disease, unspecified — on inhalers.  Chronic obstructive pulmonary disease, unspecified (J44.9)


⸻

🔒 100% Local, Zero PHI Leakage

✅ No LLM or network calls
✅ Fully script-based reasoning (deterministic)
✅ Can be bundled into an .exe or .app via pyinstaller for one-click use in clinic or hospital
