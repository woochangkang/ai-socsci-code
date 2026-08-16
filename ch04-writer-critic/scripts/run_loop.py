#!/usr/bin/env python3
"""Minimal writer-critic loop scaffold.

Default mode is --mock (no API). With --live, requires ANTHROPIC_API_KEY
and the `anthropic` package.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def mock_critique(draft: str) -> str:
    return (
        "① 인과 방향의 가정이 정당화되지 않음 — 역방향(참여→신뢰) 문헌 미언급.\n"
        "② '하락'은 종단 술어인데 설계 서술이 횡단면으로 읽힘.\n"
        "③ 사례(2026 한국)의 이론적 이점이 없음.\n"
        "④ 첫 문단에 퍼즐(통념과 어긋나는 관찰)이 없음.\n"
    )


def mock_revise(draft: str, accepted: str) -> str:
    return (
        draft.rstrip()
        + "\n\n<!-- 개정 반영(모의) -->\n"
        + "횡단면 자료의 한계상 본 연구가 식별하는 것은 신뢰와 참여 의향의 "
        + "연관이며, 인과 방향에 대한 경쟁 가설은 2절에서 검토한다. "
        + "2026년 한국 사례는 [이 자리를 자신의 이론적 이점으로 채울 것].\n"
        + f"\n<!-- 수용된 반론 메모 -->\n{accepted}\n"
    )


def parse_gate(text: str) -> str:
    """Return lines marked accepted."""
    lines = []
    for line in text.splitlines():
        if re.search(r"\[수용\]", line):
            lines.append(line)
    return "\n".join(lines) if lines else text


def live_call(system: str, user: str) -> str:
    try:
        import anthropic
    except ImportError as e:
        raise SystemExit("live mode needs: pip install anthropic") from e
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return msg.content[0].text


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", type=Path, default=ROOT / "sample" / "intro_v0.md")
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--live", action="store_true")
    ap.add_argument(
        "--gate-file",
        type=Path,
        help="Human gate file with [수용]/[기각: 사유] marks. If omitted, all critique lines are treated as accepted in mock mode only.",
    )
    args = ap.parse_args()
    out = ROOT / "output"
    draft = read(args.draft)
    critic_sys = read(ROOT / "prompts" / "critic.md")
    writer_sys = read(ROOT / "prompts" / "writer.md")

    if args.live:
        critique = live_call(critic_sys, draft)
    else:
        critique = mock_critique(draft)
    cpath = out / f"round{args.round}_critique.md"
    write(cpath, critique)
    print(f"wrote {cpath}")

    if args.gate_file and args.gate_file.exists():
        accepted = parse_gate(read(args.gate_file))
    else:
        # template gate file for human
        gpath = out / f"round{args.round}_gate.md"
        gate_tmpl = critique + "\n\n# 인간 게이트\n# 각 항목 끝에 [수용] 또는 [기각: 사유]를 적고 --gate-file 로 다시 실행하라.\n"
        write(gpath, gate_tmpl)
        print(f"wrote gate template {gpath}")
        print("Edit the gate file, then rerun with --gate-file and same --round to revise.")
        if not args.live:
            # still produce a demo revision for mock walkthrough
            accepted = critique
        else:
            return

    if args.live:
        user = f"원고:\n{draft}\n\n수용된 반론:\n{accepted}"
        revised = live_call(writer_sys, user)
    else:
        revised = mock_revise(draft, accepted)
    rpath = out / f"round{args.round}_revision.md"
    write(rpath, revised)
    print(f"wrote {rpath}")


if __name__ == "__main__":
    main()
