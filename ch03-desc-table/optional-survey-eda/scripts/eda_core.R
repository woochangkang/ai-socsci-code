# 검증된 계산 부품. 에이전트는 이 함수를 호출만 한다.
# survey-eda 스킬의 SKILL.md가 "새로 구현하지 않는다"고 지시하는 대상이 이 파일이다.

# 가중 기술통계 — 가중치가 없으면 wt = NULL 로 두면 무가중이 된다.
w_desc_cont <- function(df, vars, wt = NULL) {
  w <- if (is.null(wt)) rep(1, nrow(df)) else df[[wt]]
  do.call(rbind, lapply(vars, function(v) {
    x  <- df[[v]]; ok <- !is.na(x) & !is.na(w)
    xi <- x[ok];   wi <- w[ok]
    m  <- sum(wi * xi) / sum(wi)
    data.frame(변수 = v, n = length(xi),
               평균 = round(m, 2),
               표준편차 = round(sqrt(sum(wi * (xi - m)^2) / sum(wi)), 2),
               최소 = min(xi), 최대 = max(xi))
  }))
}

# 변수별 결측률 표 — 30% 초과는 경고 대상으로 표시한다.
tab_missing <- function(df) {
  r <- vapply(df, function(x) mean(is.na(x)) * 100, numeric(1))
  data.frame(변수 = names(r), 결측률 = round(unname(r), 1),
             경고 = ifelse(unname(r) > 30, "!", ""))
}

# 결측 패턴 그림 — 만든 파일의 경로를 반환한다.
plot_missing <- function(df, path = "output/figures/missing.png") {
  r <- sort(vapply(df, function(x) mean(is.na(x)) * 100, numeric(1)))
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)
  png(path, width = 900, height = 140 + 30 * length(r), res = 130, type = "quartz")
  # 한글 라벨은 par(family=)로 지정해야 한다. png(family=)로는 적용되지 않는다.
  op <- par(mar = c(4, 7, 1, 2), family = "AppleGothic")
  barplot(r, horiz = TRUE, las = 1, xlab = "결측률 (%)", border = NA,
          col = ifelse(r > 30, "#9E1B32", "#9CA3AF"), xlim = c(0, 100))
  abline(v = 30, lty = 2)          # tab_missing()의 경고 기준과 같은 선
  par(op); dev.off()
  path
}
