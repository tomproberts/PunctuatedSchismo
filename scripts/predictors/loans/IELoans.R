library(dplyr)
library(stringr)

# Read in IE-CoR languages and lexeme×cognateset mapping
languages <- read.csv("data/datasets/ie-cor/languages.csv")[, c("ID", "Name", "ascii_name")]
cognates <- read.csv("data/datasets/ie-cor/cognates.csv")[, c("Form_ID", "Cognateset_ID")]

# Read in all loan events, excluding parallel ones
loans <- read.csv("data/datasets/ie-cor/loans.csv")
loans <- loans[loans$Parallel_loan_event == "false", c("Cognateset_ID", "Comment")]

# Work out which cognate sets contain multiple lexemes in multiple languages
loans <- merge(loans, cognates, by = "Cognateset_ID")

# Count lexemes per cognate set, filter to unique borrowing events
n.lexemes <- count(loans, Cognateset_ID)
n.lexemes <- n.lexemes[n.lexemes$n == 1,]
loans <- merge(n.lexemes, loans, by = "Cognateset_ID")

# Extract language ID
loans$lang_id <- sapply(loans$Form_ID, function(x) str_split(x, "-")[[1]][1])

# Count loans per language, listing the sets
df <- loans %>%
  group_by(lang_id) %>%
  summarise(
    n_loans = n_distinct(Cognateset_ID),
    cognate_sets = paste(unique(Cognateset_ID), collapse = ";")
  )

# Include language name, tidy up
df <- merge(languages, df, by.y = "lang_id", by.x = "ID")
df <- df %>% rename(lang = ascii_name, name = Name) %>% select(!ID)

write.csv(df, "data/predictors/loans/IndoEuropean.csv", row.names = FALSE, quote = FALSE)
