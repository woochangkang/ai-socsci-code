#!/usr/bin/env Rscript
# csv-descriptives 고정 계산 스크립트
# CSV의 수치형 변수별 n, 평균, 표준편차, 최소, 최대를 계산해
# 마크다운 표를 stdout으로 출력한다. --out 지정 시 CSV로도 저장.
#
# 사용법:
#   Rscript descriptives.R <input.csv> [--out=<output.csv>] [--digits=2] [--encoding=UTF-8]
#
# 옵션:
#   --out=PATH       결과 표를 CSV로 저장 (기본: 저장 안 함)
#   --digits=N       소수점 자릿수 (기본 2)
#   --encoding=ENC   입력 파일 인코딩 (기본 UTF-8, 한글 깨짐 시 CP949)

args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 1) {
  stop("사용법: Rscript descriptives.R <input.csv> [--out=...] [--digits=2] [--encoding=UTF-8]",
       call. = FALSE)
}

input    <- args[1]
opts     <- args[-1]
get_opt  <- function(key, default) {
  hit <- grep(paste0("^--", key, "="), opts, value = TRUE)
  if (length(hit) == 0) default else sub(paste0("^--", key, "="), "", hit[1])
}
out_path <- get_opt("out", NA_character_)
digits   <- as.integer(get_opt("digits", "2"))
encoding <- get_opt("encoding", "UTF-8")

if (!file.exists(input)) {
  stop("입력 파일을 찾을 수 없음: ", input, call. = FALSE)
}

df <- read.csv(input, fileEncoding = encoding, check.names = FALSE,
               stringsAsFactors = FALSE)

is_num  <- vapply(df, is.numeric, logical(1))
num_df  <- df[is_num]
skipped <- names(df)[!is_num]

if (ncol(num_df) == 0) {
  stop("수치형 변수가 없음. 인코딩 문제라면 --encoding=CP949 를 시도할 것.", call. = FALSE)
}

stat_row <- function(x, name) {
  x_ok <- x[!is.na(x)]
  data.frame(
    variable = name,
    n        = length(x_ok),
    mean     = mean(x_ok),
    sd       = sd(x_ok),
    min      = min(x_ok),
    max      = max(x_ok),
    stringsAsFactors = FALSE
  )
}

res <- do.call(rbind, Map(stat_row, num_df, names(num_df)))
rownames(res) <- NULL

fmt <- function(v) formatC(v, format = "f", digits = digits)

cat("| variable | n | mean | sd | min | max |\n")
cat("|---|---:|---:|---:|---:|---:|\n")
for (i in seq_len(nrow(res))) {
  cat(sprintf("| %s | %d | %s | %s | %s | %s |\n",
              res$variable[i], res$n[i],
              fmt(res$mean[i]), fmt(res$sd[i]),
              fmt(res$min[i]),  fmt(res$max[i])))
}

if (length(skipped) > 0) {
  cat("\n제외된 비수치형 변수:", paste(skipped, collapse = ", "), "\n")
}

if (!is.na(out_path)) {
  res_out <- res
  res_out[c("mean", "sd", "min", "max")] <-
    lapply(res_out[c("mean", "sd", "min", "max")], round, digits = digits)
  write.csv(res_out, out_path, row.names = FALSE, fileEncoding = "UTF-8")
  cat("\n저장됨:", out_path, "\n")
}
