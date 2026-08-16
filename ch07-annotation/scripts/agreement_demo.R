#!/usr/bin/env Rscript
# Cohen's kappa between human_label and a silly keyword model (teaching only).
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})
if (!requireNamespace("irr", quietly = TRUE)) {
  message("Optional: install.packages('irr') for cohen.kappa; falling back to accuracy only")
}
d <- read_csv("sample/bills_sample.csv", show_col_types = FALSE)
pred <- ifelse(grepl("여성|여군|성폭력|성희롱|출산|산모|한부모|육아|생리|남녀|모자|친권", d$text), 3L,
          ifelse(grepl("돌봄|보육|가족", d$text), 1L, 0L))
# map rough
acc <- mean(pred == d$human_label)
cat(sprintf("mock accuracy vs sample labels: %.3f\n", acc))
print(table(human = d$human_label, mock = pred))
if (requireNamespace("irr", quietly = TRUE)) {
  print(irr::kappa2(data.frame(d$human_label, pred)))
}
