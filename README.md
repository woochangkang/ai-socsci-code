# ai-socsci-code

『AI를 이용한 사회과학 연구』(핵심편) 실습 코드·연습 데이터.

책 원고: 별도 저장소([ai-socsci-book](https://github.com/woochangkang/ai-socsci-book), private). 본문의 코드는 발췌이며, **실행 전문은 여기** 둔다.

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
- **Site**: <https://woochangkang.github.io/ai-socsci-code/>
- **책 HTML 미리보기**: <https://woochangkang.github.io/ai-socsci-code/book/>
- **Actions**: <https://github.com/woochangkang/ai-socsci-code/actions/workflows/pages.yml>

### 사이트 지도 (내비게이션)
허브 상단 메뉴(모든 허브 페이지 공통):

| 메뉴 | 경로 |
|---|---|
| 홈 | `/` · `/index.html` |
| 설치 | `/setup.html` |
| 저장소 안내 | `/about.html` |
| 책 HTML | `/book/` · `/book/index.html` |
| GitHub | 저장소 루트 |

장별 실습 카드 → `/labs/<folder>.html` (예: `/labs/ch01-git.html`).  
책 HTML은 Quarto book 사이드바/목차로 서장·1–7장·종장(8장)을 이동합니다.

### 내비게이션 검증 (2026-08-16)
라이브 사이트 크롤 결과:

- 시드 페이지 11개 전부 HTTP **200**
- 허브 내부 링크 22개 **전부 200** (실패 0)
- 허브 `nav` 5항목 상대경로 정합 (`labs/*`에서는 `../` 접두)
- 책 목차 링크: `chapters/00-intro.html` … `08-close.html` 존재

재검증 예:

```bash
for u in \
  https://woochangkang.github.io/ai-socsci-code/ \
  https://woochangkang.github.io/ai-socsci-code/setup.html \
  https://woochangkang.github.io/ai-socsci-code/book/ \
  https://woochangkang.github.io/ai-socsci-code/labs/ch01-git.html
 do curl -s -o /dev/null -w "%{http_code}  $u\n" -L "$u"; done
```

## 배포 절차 (GitHub Pages)

이 저장소가 **공개 문서·책 HTML 미러의 호스트**다. (`ai-socsci-book`은 private라 free 플랜에서 Pages 직접 호스팅 불가.)

### 구성 요소
| 경로 | 역할 |
|---|---|
| `scripts/build_pages_site.py` | README→정적 HTML 허브 생성, `site/book` 임베드 |
| `site/book/` | 원고 저장소 `quarto render` 산출물(`_book/`) 동기 번들 |
| `site/book/.nojekyll` | Jekyll이 `_` 디렉터리(`site_libs` 등)를 숨기지 않게 함 |
| `.github/workflows/pages.yml` | `main` push 시 build→Pages deploy |
| `public/` | 빌드 출력 (**gitignore**, CI 아티팩트만 사용) |

### 자동 배포 (기본)
1. `main`에 push (또는 Actions에서 **Deploy GitHub Pages** → Run workflow)
2. 워크플로가 `python3 scripts/build_pages_site.py` 실행
3. `public/`을 GitHub Pages에 배포
4. 수 분 후 <https://woochangkang.github.io/ai-socsci-code/> 갱신

Pages 설정: **Settings → Pages → Build and deployment → GitHub Actions**  
(`build_type: workflow`로 이미 활성화됨.)

### 로컬에서 사이트만 미리보기
```bash
python3 scripts/build_pages_site.py
# macOS
open public/index.html
# or
python3 -m http.server -d public 8000
# http://127.0.0.1:8000/
```

### 책 HTML 번들 갱신 (원고 변경 후)
원고 저장소에서 렌더한 뒤 이 저장소의 `site/book/`를 덮어쓴다.

```bash
# 1) 원고 저장소
cd ../ai-socsci-book
quarto render

# 2) 실습 저장소로 번들 복사
rsync -a --delete ../ai-socsci-book/_book/ ./site/book/
touch ./site/book/.nojekyll

# 3) 커밋·푸시 → Pages 자동 배포
git add site/book
git commit -m "Refresh core-edition book HTML bundle"
git push origin main
```

장 안내 문구만 바뀌면 해당 `ch*/README.md` 수정 후 push하면 허브 페이지가 다시 빌드된다.

### 장애 점검
- Actions 실패: workflow 로그에서 `build_pages_site.py` / `upload-pages-artifact` / `deploy-pages` 단계 확인
- 200이 아닌 경로: 위의 curl 루프로 재확인; 캐시면 몇 분 대기
- 책 스타일/검색 깨짐: `site/book/site_libs/`와 `.nojekyll` 존재 여부 확인
- 구 경로 북마크: 허브는 `/labs/…`, 책은 `/book/chapters/…` 고정

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

