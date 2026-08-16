#!/usr/bin/env python3
"""Build a static HTML site for GitHub Pages from repo READMEs + optional book bundle."""
from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public"

CHAPTERS = [
    ("ch01-git", "1장 · Git"),
    ("ch02-cli", "2장 · CLI / CLAUDE.md"),
    ("ch03-desc-table", "3장 · desc-table 스킬"),
    ("ch03-examples", "3장 · 예시(읽기 전용)"),
    ("ch04-writer-critic", "4장 · writer–critic"),
    ("ch05-eval-harness", "5장 · eval harness"),
    ("ch06-rag", "6장 · RAG 추출 연습"),
    ("ch07-annotation", "7장 · annotation 연습"),
]

CSS = """
:root { --ink:#1a1a1a; --muted:#5c5c5c; --bg:#fafafa; --card:#fff; --accent:#9E1B32; --line:#e6e6e6; }
* { box-sizing: border-box; }
body { margin:0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color:var(--ink); background:var(--bg); line-height:1.65; }
header { background:#111; color:#fff; padding:1.25rem 1.5rem; }
header a { color:#fff; text-decoration:none; }
header .sub { color:#ccc; font-size:.95rem; margin-top:.35rem; }
nav { background:#fff; border-bottom:1px solid var(--line); padding:.75rem 1.5rem; display:flex; gap:1rem; flex-wrap:wrap; }
nav a { color:var(--accent); text-decoration:none; font-weight:600; }
main { max-width:920px; margin:0 auto; padding:1.5rem; }
.card { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:1rem 1.15rem; margin:0 0 1rem; }
.card h2 { margin:.2rem 0 .4rem; font-size:1.15rem; }
.card p { margin:.25rem 0; color:var(--muted); }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:.85rem; }
pre, code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
pre { background:#f4f4f5; padding:1rem; overflow:auto; border-radius:8px; }
article.markdown h1 { font-size:1.7rem; }
article.markdown h2 { margin-top:1.6rem; border-bottom:1px solid var(--line); padding-bottom:.25rem; }
article.markdown table { border-collapse:collapse; width:100%; margin:1rem 0; }
article.markdown th, article.markdown td { border:1px solid var(--line); padding:.45rem .6rem; text-align:left; vertical-align:top; }
footer { max-width:920px; margin:2rem auto; padding:0 1.5rem 2rem; color:var(--muted); font-size:.9rem; }
.badge { display:inline-block; background:#eee; border-radius:999px; padding:.1rem .55rem; font-size:.8rem; color:#333; }
"""


def md_inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    in_code = False
    in_ul = False
    in_table = False

    def close_ul() -> None:
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def close_table() -> None:
        nonlocal in_table
        if in_table:
            out.append("</tbody></table>")
            in_table = False

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            close_ul(); close_table()
            if not in_code:
                in_code = True
                lang = html.escape(line[3:].strip())
                out.append(f'<pre><code class="language-{lang}">')
            else:
                in_code = False
                out.append("</code></pre>")
            i += 1
            continue
        if in_code:
            out.append(html.escape(line) + "\n")
            i += 1
            continue
        if re.match(r"^\|.*\|$", line) and i + 1 < len(lines) and re.match(r"^\|\s*[-: ]+\|", lines[i + 1]):
            close_ul()
            headers = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            out.append("<table><thead><tr>" + "".join(f"<th>{md_inline(h)}</th>" for h in headers) + "</tr></thead><tbody>")
            in_table = True
            while i < len(lines) and re.match(r"^\|.*\|$", lines[i]):
                cols = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                out.append("<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in cols) + "</tr>")
                i += 1
            close_table()
            continue
        if line.startswith("# "):
            close_ul(); close_table(); out.append(f"<h1>{md_inline(line[2:])}</h1>")
        elif line.startswith("## "):
            close_ul(); close_table(); out.append(f"<h2>{md_inline(line[3:])}</h2>")
        elif line.startswith("### "):
            close_ul(); close_table(); out.append(f"<h3>{md_inline(line[4:])}</h3>")
        elif re.match(r"^[-*] ", line):
            close_table()
            if not in_ul:
                out.append("<ul>"); in_ul = True
            out.append(f"<li>{md_inline(line[2:])}</li>")
        elif line.strip() == "":
            close_ul(); close_table()
        else:
            close_ul(); close_table()
            out.append(f"<p>{md_inline(line)}</p>")
        i += 1
    close_ul(); close_table()
    return "\n".join(out)


def page(title: str, body: str, rel_prefix: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html.escape(title)}</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <div><a href="{rel_prefix}index.html"><strong>AI 사회과학 연구 · 실습</strong></a></div>
  <div class="sub">ai-socsci-code · core edition labs</div>
</header>
<nav>
  <a href="{rel_prefix}index.html">홈</a>
  <a href="{rel_prefix}setup.html">설치</a>
  <a href="{rel_prefix}about.html">저장소 안내</a>
  <a href="{rel_prefix}book/index.html">책 HTML</a>
  <a href="https://github.com/woochangkang/ai-socsci-code">GitHub</a>
</nav>
<main>
{body}
</main>
<footer>
  MIT (코드·합성 데이터). 책 HTML 미리보기는 핵심편 배포본이며 원고 저장소는 private다.
</footer>
</body>
</html>
"""


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    cards = []
    for folder, label in CHAPTERS:
        readme = ROOT / folder / "README.md"
        blurb = "실습 폴더"
        if readme.exists():
            for ln in readme.read_text(encoding="utf-8").splitlines():
                s = ln.strip()
                if s and not s.startswith("#"):
                    blurb = s[:160]
                    break
        cards.append(
            f'<div class="card"><h2><a href="labs/{html.escape(folder)}.html">{html.escape(label)}</a></h2>'
            f'<p>{html.escape(blurb)}</p><p><span class="badge">{html.escape(folder)}</span></p></div>'
        )

    home_body = f"""
<article>
  <h1>실습 자료 사이트</h1>
  <p>『AI를 이용한 사회과학 연구』 핵심편 실습 문서 허브입니다. 소스·데이터는 GitHub에 두고,
  여기서는 장별 안내와 책 HTML 미리보기를 제공합니다.</p>
  <p><a href="setup.html">설치 가이드</a> ·
     <a href="book/index.html"><strong>책 HTML (핵심편)</strong></a> ·
     <a href="https://github.com/woochangkang/ai-socsci-code">저장소</a></p>
  <h2>장별 실습</h2>
  <div class="grid">{''.join(cards)}</div>
</article>
"""
    (OUT / "index.html").write_text(page("AI 사회과학 연구 · 실습", home_body), encoding="utf-8")

    setup_md = (ROOT / "SETUP.md").read_text(encoding="utf-8")
    (OUT / "setup.html").write_text(
        page("설치", f'<article class="markdown">{md_to_html(setup_md)}</article>'),
        encoding="utf-8",
    )

    root_md = (ROOT / "README.md").read_text(encoding="utf-8")
    (OUT / "about.html").write_text(
        page("저장소 안내", f'<article class="markdown">{md_to_html(root_md)}</article>'),
        encoding="utf-8",
    )

    labs = OUT / "labs"
    labs.mkdir()
    for folder, label in CHAPTERS:
        readme = ROOT / folder / "README.md"
        md = readme.read_text(encoding="utf-8") if readme.exists() else f"# {label}\n\nREADME 없음.\n"
        body = (
            f'<article class="markdown">{md_to_html(md)}'
            f'<p><a href="https://github.com/woochangkang/ai-socsci-code/tree/main/{folder}">소스 폴더 열기</a></p>'
            f"</article>"
        )
        (labs / f"{folder}.html").write_text(page(label, body, rel_prefix="../"), encoding="utf-8")

    # Embed Quarto book if present
    src_book = ROOT / "site" / "book"
    dst_book = OUT / "book"
    if src_book.exists() and (src_book / "index.html").exists():
        shutil.copytree(src_book, dst_book)
        print(f"embedded book from {src_book}")
    else:
        dst_book.mkdir(parents=True)
        (dst_book / "index.html").write_text(
            page(
                "책 HTML",
                """
<article>
  <h1>책 HTML 미리보기</h1>
  <p>책 빌드 산출물이 아직 포함되지 않았습니다.</p>
  <p><a href="../index.html">실습 홈</a></p>
</article>
""",
                rel_prefix="../",
            ),
            encoding="utf-8",
        )
        print("book placeholder written")

    print(f"wrote site to {OUT}")


if __name__ == "__main__":
    main()
