#!/usr/bin/env python3
"""Minimal eval harness with offline mock scorer."""
from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def mock_predict(text: str) -> str:
    if re.search(r"선포|동의|표결|속기록|의사일정|정회", text):
        return "절차"
    if re.search(r"규탄|위선|무능|왜곡|비판|공격|발목", text):
        return "정쟁"
    return "정책"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--golden", type=Path, default=ROOT / "golden" / "dev_20.csv")
    ap.add_argument("--prompt", type=Path, default=ROOT / "prompts" / "classify_v1.md")
    args = ap.parse_args()
    prompt = args.prompt.read_text(encoding="utf-8")
    rows = list(csv.DictReader(args.golden.open(encoding="utf-8")))
    out_rows = []
    ok = 0
    conf = Counter()
    for r in rows:
        pred = mock_predict(r["text"])
        correct = pred == r["human_label"]
        ok += int(correct)
        conf[(r["human_label"], pred)] += 1
        out_rows.append({**r, "model_label": pred, "correct": correct})
    n = len(rows)
    print(f"N={n}  accuracy={ok/n:.3f}  (mock keyword model)")
    print("confusion human->model:", dict(conf))
    out = ROOT / "output" / "eval_dev20_mock.csv"
    out.parent.mkdir(exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)
    print("wrote", out)
    print("prompt head:", prompt[:60].replace("\n", " "), "...")


if __name__ == "__main__":
    main()
