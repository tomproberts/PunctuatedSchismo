library(tidyr)
source("scripts/families/LanguageFamilies.R")
source("scripts/phylo/FullPosterior.R")

set.seed(42)
GAMMASPIKE <- TRUE
# LOG.FILE <- "data/phylo/relaxed/full/indoeuropean_1785842680219.log"
LOG.FILE <- "data/phylo/gammaspike/full/IndoEuropean.log"
BURN.IN <- 1000

translation <- get_translation(INDO.EUROPEAN)
# takes 10-30 seconds
l <- read.csv(LOG.FILE, sep = "\t", comment.char = "#")
all.samples <- l$Sample

# only select branch rate columns
if (GAMMASPIKE) { rate.param <- "weightedSpikes" } else { rate.param <- "branchRates" }
rate.cols <- paste(rate.param, unname(translation), sep = ".")
l <- l[, rate.cols]

# select subset of samples
selected.rows <- sort(BURN.IN + sample(nrow(l) - BURN.IN, 100))
l <- l[selected.rows,]

# relabel rows, round to 6 digits
if (GAMMASPIKE) { new.param <- "burst" } else { new.param <- "rate" }
rownames(l) <- paste(new.param, all.samples[selected.rows], sep = "_")
l <- format(l, digits = 6)

# transpose, label rows
df <- data.frame(t(l))
df$lang <- names(translation)
df <- df[, c(ncol(df), 1:(ncol(df) - 1))]

# write out
if (GAMMASPIKE) { dir <- "gammaspike" } else { dir <- "relaxed" }
write.csv(df, paste0("data/phylo/", dir, "/full/IndoEuropean.csv"), quote = FALSE, row.names = FALSE)
