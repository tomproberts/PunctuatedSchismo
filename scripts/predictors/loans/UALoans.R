library(dplyr)
library(stringr)

languages <- read.csv("data/datasets/utoaztecan/languages.csv")
df <- read.csv("data/datasets/utoaztecan/forms.csv")

### fix different language names
df[df$Language_ID == "PimaDeOnavas",]$Language_ID <- "PimadeOnavas"
df[df$Language_ID == "ShoshoniGosiute",]$Language_ID <- "ShoshoniGosiuteDialect"

languages$key_name <- str_replace_all(languages$Name, "_", "")
languages$key_name <- sapply(languages$key_name, function (x) str_split(x, "-")[[1]][1])

forms.langs <- unique(df$Language_ID)
ua.langs <- unique(languages$key_name)
for (lang in ua.langs) {
  if (!(lang %in% forms.langs)) warning(paste(lang, "not found in 'forms.csv' data!"))
}
###

df.2 <- df[!str_ends(df$ID, "-1"),]

n.lexemes <- count(df.2, Language_ID)
n.lexemes <- n.lexemes[n.lexemes$Language_ID %in% ua.langs,]
