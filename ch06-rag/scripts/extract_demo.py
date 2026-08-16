#!/usr/bin/env python3
"""Extract structured fields from the synthetic abstract (no API)."""
from pathlib import Path
import re
root = Path(__file__).resolve().parents[1]
text = (root / "sample_papers" / "fake_abstracts.md").read_text(encoding="utf-8")
n = re.search(r"(\d[\d,]*) respondents", text)
b = re.search(r"b = ([0-9.]+)", text)
se = re.search(r"SE = ([0-9.]+)", text)
print("extraction demo")
print("N:", n.group(1) if n else None)
print("b:", b.group(1) if b else None)
print("SE:", se.group(1) if se else None)
print("Next: open the real PDF for a paper you own and fill the same fields with page notes.")
