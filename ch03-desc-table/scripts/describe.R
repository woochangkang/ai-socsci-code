# 변수별 기술통계 표 — 같은 파일이면 언제나 같은 표.
# 사용법: Rscript describe.R <파일.csv>
args <- commandArgs(trailingOnly = TRUE)
df  <- read.csv(args[1])
num <- df[sapply(df, is.numeric)]

cat("| 변수 | n | 평균 | 표준편차 | 최소 | 최대 |\n|---|---|---|---|---|---|\n")
for (v in names(num)) {
  x <- num[[v]]
  cat(sprintf("| %s | %d | %.2f | %.2f | %g | %g |\n",
              v, length(x), mean(x), sd(x), min(x), max(x)))
}

빠진열 <- setdiff(names(df), names(num))
if (length(빠진열)) cat(sprintf("\n수치형이 아니라 제외한 열: %s\n",
                                paste(빠진열, collapse = ", ")))
