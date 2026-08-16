# ai-socsci-code

『AI를 이용한 사회과학 연구』(핵심편) 실습 코드·연습 데이터.

책 원고: 별도 저장소. 본문의 코드는 발췌이며, **실행 전문은 여기** 둔다.

## 책 장 ↔ 폴더

| 책 | 폴더 | 비고 |
|---|---|---|
| 1장 | `ch01-git/` | 합성 설문 CSV |
| 2장 | `ch02-cli/` | voter2026 + CLAUDE 예시 |
| 3장 | `ch03-desc-table/` | 튜토리얼 본선 |
| 3장 보조 | `ch03-examples/` | vibe-coded(읽기 전용), journal-review 샘플 |
| 4장 | `ch04-writer-critic/` | 작성자–비판자 루프 |
| 5장 | `ch05-eval-harness/` | 평가 하니스 (모의 기본) |
| 6장 | `ch06-rag/` | 추출 연습 (개인 Zotero 캡처 없음) |
| 7장 | `ch07-annotation/` | 합성 소표본 — **본문 실측과 별개** |
| — | `templates/` | 공개 진술·CLAUDE·점검표 |

## 웹 문서
- Site: <https://woochangkang.github.io/ai-socsci-code/>
- 책 HTML 미리보기: <https://woochangkang.github.io/ai-socsci-code/book/>

## 시작
```bash
git clone https://github.com/woochangkang/ai-socsci-code.git
cd ai-socsci-code
# SETUP.md 참고 후 장 폴더로
```

## 공개 감사 요약
- 개인 Zotero 라이브러리 덤프·절대 경로·API 키 없음
- 7장 실측 골든셋·RA 식별 정보 없음 (학습용 합성만)
- 제3자 논문 PDF는 재배포 허용 범위에서만

## 라이선스
코드·합성 데이터: MIT (`LICENSE`). 제3자 자료는 각 파일 고지.

## 사이트 소스
- `scripts/build_pages_site.py` — Pages 정적 사이트 생성
- `site/book/` — 핵심편 Quarto HTML 번들(원고 저장소 `_book` 동기본)
- `.github/workflows/pages.yml` — GitHub Pages 배포

