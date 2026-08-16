# ch07 — annotation 연습

책 7장의 **문법**(코드북·골든셋·κ·혼동행렬)을 소표본으로 연습한다.

## 중요
- `sample/bills_sample.csv`는 합성·예시 라벨이다.
- 본문 7.7의 실측 수치를 이 파일로 "재현"했다고 쓰지 말 것.
- 실제 의안 전수·RA 골든셋은 공개 repo에 포함하지 않았다.

## 실행
```bash
cd ch07-annotation
Rscript scripts/agreement_demo.R
# figures (optional; needs book figures pipeline inputs — script may be illustrative)
# Rscript make_figures.R
```

예상 시간: 90분(코드북 작성 포함 시 반나절).
