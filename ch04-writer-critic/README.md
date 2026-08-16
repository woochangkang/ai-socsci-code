# ch04 — writer-critic 루프

책 4.4절의 작성자–비판자 2-역할 루프 최소 구현.

## 필요 도구
- Python 3.10+
- (선택) `pip install anthropic` + `ANTHROPIC_API_KEY` — `--live` 모드

## 성공 기준
1. `output/round1_critique.md`가 생긴다
2. 게이트 파일에 `[수용]`/`[기각: 사유]`를 표시한다
3. `output/round1_revision.md`가 생긴다
4. (권장) 2라운드까지 반복하고 v0와 최종본을 한 단락으로 비교한다

## 빠른 시작 (모의, API 불필요)
```bash
cd ch04-writer-critic
python3 scripts/run_loop.py --round 1
# output/round1_gate.md 를 편집한 뒤
python3 scripts/run_loop.py --round 1 --gate-file output/round1_gate.md
```

예상 시간: 45–90분(자기 서론 초안 사용 시).
