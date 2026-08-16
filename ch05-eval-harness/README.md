# ch05 — eval harness

책 5.3절 평가 하니스의 최소 구현. 기본은 **모의 분류기**(키워드)로 루프만 연습한다. 실제 LLM 연결은 과제.

## 필요 도구
- R + tidyverse **또는** Python 3.10+
- (심화) LLM API

## 성공 기준
1. `golden/dev_20.csv`에 대해 accuracy와 혼동표를 출력한다
2. `output/eval_*.csv`에 건별 예측이 남는다
3. (심화) `prompts/classify_v1.md`를 고쳐 v2를 만들고 표로 비교한다

## 실행
```bash
cd ch05-eval-harness
python3 python/run_eval.py
# 또는
Rscript R/run_eval.R
```

**주의:** 이 골든셋은 학습용 합성 발화다. 7장 의안 젠더 실측 수치와 연결하지 말 것.

예상 시간: 60–90분.
