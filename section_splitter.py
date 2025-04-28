# section_splitter.py
import re
import os
from typing import Dict
from pdf_extractor import extract_text_from_pdf

# Define valid regex group names (underscored)
SECTION_PATTERNS = {
    "business_overview": r"(Item\s+1\.\s+Business|Business\s+Overview)",
    "business_segment_overview": r"(Segment\s+(Results|Information|Overview))",
    "geographical_breakdown": r"(Geographic\s+(Information|Performance|Breakdown))",
    "swot_analysis": r"(SWOT\s+Analysis)",
    "risk_factors": r"(Item\s+1A\.\s+Risk\s+Factors)",
    "credit_rating": r"(Credit\s+Rating|Rating\s+Change|Outlook\s+Change)"
}

def split_sections(text: str) -> Dict[str, str]:
    sections = {}
    pattern = "|".join(f"(?P<{key}>{regex})" for key, regex in SECTION_PATTERNS.items())
    matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section_key = next((key for key in match.groupdict() if match.group(key)), None)
        if section_key:
            sections[section_key] = text[start:end].strip()

    return sections

if __name__ == "__main__":
    folder_path = "./data/input_reports"
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".pdf"):
            print(f"\nProcessing: {file_name}")
            full_path = os.path.join(folder_path, file_name)
            text = extract_text_from_pdf(full_path)
            split = split_sections(text)

            for section, content in split.items():
                print(f"\n=== {section.replace('_', ' ').title()} ===")
                print(content[:500])  # Preview first 500 characters
