# ============================================================
# 7장 데이터 그림 생성
# ============================================================
# fig7-2_three_agreements.png — 안정성·수렴·타당도 세 지표 비교
#
# 여기 박힌 수치는 모두 실측이며, 출처는 아래와 같다. 임의로 고치지 말 것.
#
#   [수렴] 이종 모델 교차 — Opus 4.7 vs Sonnet 4.6, 22대 gold 198건
#     Data_Korea/National Assembly/bills/gender_classification/
#       gold_sample/gold_198_dual_20260423.csv  에서 직접 산출
#     unweighted κ = 0.877 / quadratic-weighted κ = 0.957 / 완전일치 95.5%
#
#   [타당도] LLM vs 인간 최종코드 — a_basis 층화 표본 200건
#     Data_Korea/National Assembly/human_validation/02_bill_gender_a_basis/
#       reconciliation/final_codes_20260530.csv + input/gender_sample_250_master.csv
#     κ = 0.686
#
#   [인간 기준선] RA 3인 pairwise κ 평균 — 같은 층화 표본 200건
#     responses/bill_gender_{A,B,C}_2026-05-*.csv  에서 직접 산출
#     κ = 0.641  (250건 전체로는 Fleiss κ = 0.608)
#
# 주의: [수렴]과 나머지 둘은 표본·대수가 다르다(198건 22대 vs 200건 a_basis).
#       같은 축에 그리는 것은 '무엇을 재는가'의 대비를 보이기 위함이며,
#       수치의 직접 뺄셈을 뜻하지 않는다. 캡션과 본문에 이 단서를 반드시 유지할 것.
#
# 실행: Rscript make_figures.R
# 출력: ../../figures/fig7-2_three_agreements.png
# ============================================================

library(ggplot2)

KRFONT <- "AppleGothic"   # 한글 두부(□□□) 방지 — CLAUDE.md 전역 규칙

d <- data.frame(
  what = factor(
    c("안정성·수렴\n(모델 간)", "타당도\n(LLM–인간)", "[참고] 인간 기준선\n(코더 간)"),
    levels = c("안정성·수렴\n(모델 간)", "타당도\n(LLM–인간)", "[참고] 인간 기준선\n(코더 간)")
  ),
  kappa = c(0.957, 0.686, 0.641),
  kind  = c("모델끼리", "사람과 대조", "사람끼리")
)

p <- ggplot(d, aes(x = what, y = kappa, fill = kind)) +
  geom_col(width = 0.58) +
  geom_text(aes(label = sprintf("%.3f", kappa)),
            vjust = -0.5, size = 4.4, family = KRFONT) +
  scale_y_continuous(limits = c(0, 1.08), breaks = seq(0, 1, 0.2),
                     expand = expansion(mult = c(0, 0.02))) +
  scale_fill_manual(values = c("모델끼리" = "#6B7280",
                               "사람과 대조" = "#9E1B32",
                               "사람끼리" = "#C9CCD1")) +
  labs(x = NULL, y = "Cohen's κ", fill = NULL) +
  theme_minimal(base_family = KRFONT) +   # 완전 테마는 base_family를 되돌리므로 여기서도 지정
  theme(
    legend.position = "none",
    panel.grid.major.x = element_blank(),
    axis.text.x = element_text(size = 10.5, lineheight = 1.15),
    plot.margin = margin(10, 14, 6, 6)
  )

outdir <- file.path("..", "..", "figures")
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
ggsave(file.path(outdir, "fig7-2_three_agreements.png"), p,
       width = 6.6, height = 3.6, dpi = 200, bg = "white")

cat("생성: figures/fig7-2_three_agreements.png\n")
