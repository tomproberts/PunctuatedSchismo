# Load loan and language information
languages <- read.csv("data/datasets/chirila/languages.csv")
loans <- read.csv("data/datasets/chirila/LoanStats.csv")

# Check languages are there
loan.langs <- loans$NameNoSpaces
missing <- list()
for (lang in languages$Name) {
  if (!(lang %in% loan.langs)) {
    missing <- c(missing, lang)
  }
}
cat(paste0("\nMissing: ", paste(missing, collapse = ', '), ".\n"))
