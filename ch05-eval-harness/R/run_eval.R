#!/usr/bin/env Rscript
# Minimal eval harness (offline mock scorer).
# For live LLM scoring, replace mock_predict() with your API wrapper.

args <- commandArgs(trailingOnly = TRUE)
golden_path <- if (length(args) >= 1) args[[1]] else "golden/dev_20.csv"
prompt_path <- if (length(args) >= 2) args[[2]] else "prompts/classify_v1.md"

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

golden <- read_csv(golden_path, show_col_types = FALSE)
prompt <- paste(readLines(prompt_path, warn = FALSE), collapse = "\n")

# Deterministic mock: keyword rules (NOT a real model). For teaching the harness loop.
mock_predict <- function(text) {
  t <- text
  if (grepl("선포|동의|표결|속기록|의사일정|정회", t)) return("절차")
  if (grepl("규탄|위선|무능|왜곡|비판|공격|발목", t)) return("정쟁")
  "정책"
}

pred <- golden %>%
  mutate(
    model_label = vapply(text, mock_predict, character(1)),
    correct = model_label == human_label
  )

acc <- mean(pred$correct)
cat(sprintf("N=%d  accuracy=%.3f  (mock keyword model)\n", nrow(pred), acc))
cat("Confusion (human x model):\n")
print(table(human = pred$human_label, model = pred$model_label))

dir.create("output", showWarnings = FALSE)
out <- file.path("output", "eval_dev20_mock.csv")
write_csv(pred, out)
cat("wrote", out, "\n")
cat("Prompt fingerprint (first 60 chars):", substr(prompt, 1, 60), "...\n")
