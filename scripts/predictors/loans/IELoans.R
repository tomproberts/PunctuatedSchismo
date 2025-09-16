library(dplyr)
library(stringr)

df <- read.csv("data/datasets/ie-cor/loans.csv")
df <- df[df$Parallel_loan_event == "false", c("Cognateset_ID", "Comment")]

cognates <- read.csv("data/datasets/ie-cor/cognates.csv")[, c("Form_ID", "Cognateset_ID")]
languages <- read.csv("data/datasets/ie-cor/languages.csv")[, c("ID", "Name", "ascii_name")]
df <- merge(df, cognates, by = "Cognateset_ID")

n.lexemes <- count(df, Cognateset_ID)
n.lexemes <- n.lexemes[n.lexemes$n == 1,]

df <- merge(n.lexemes, df, by = "Cognateset_ID")
df$lang_id <- sapply(df$Form_ID, function(x) str_split(x, "-")[[1]][1])

df <- count(df, lang_id)
df <- merge(languages, df, by.y = "lang_id", by.x = "ID")
df$n_loans <- df$n
df$lang <- df$ascii_name
df$name <- df$Name

df <- df[, c("lang", "name", "n_loans")]

write.csv(df, "data/predictors/loans/IndoEuropean.csv", row.names = FALSE, quote = FALSE)