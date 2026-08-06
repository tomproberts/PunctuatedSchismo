library(tidyr)
source("scripts/families/LanguageFamilies.R")
source("scripts/phylo/FullPosterior.R")

set.seed(42)

translation <- get_translation(INDO.EUROPEAN)
# takes 10-30 seconds
l <- read.csv("data/phylo/relaxed/full/indoeuropean_1785842680219.log", sep = "\t", comment.char = "#")
all.samples <- l$Sample

# only select branch rate columns
rate.cols <- paste("branchRates", unname(translation), sep = ".")
l <- l[, rate.cols]

# select subset of samples
BURN.IN <- 1500
selected.rows <- sort(BURN.IN + sample(nrow(l) - BURN.IN, 100))
l <- l[selected.rows,]

# relabel rows, round to 6 digits
rownames(l) <- paste("rate", all.samples[selected.rows], sep = "_")
l <- format(l, digits = 6)

# transpose, label rows
df <- data.frame(t(l))
df$lang <- names(translation)
df <- df[, c(ncol(df), 1:(ncol(df) - 1))]

# write out
write.csv(df, "data/phylo/relaxed/full/IndoEuropean.csv", quote = FALSE, row.names = FALSE)
