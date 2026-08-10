library(tidyr)
source("scripts/families/LanguageFamilies.R")
source("scripts/phylo/FullPosterior.R")

set.seed(42)
GAMMASPIKE <- FALSE
LOG.FILE <- "data/phylo/relaxed/full/indoeuropean_1785842680219.log"
# LOG.FILE <- "data/phylo/gammaspike/full/IndoEuropean.log"
BURN.IN <- 1500
N.SAMPLES <- 200

translation <- get_translation(INDO.EUROPEAN)
cat(paste0("Reading ", LOG.FILE, "...\n"))
l <- read.csv(LOG.FILE, sep = "\t", comment.char = "#")  # takes 10-30 seconds
all.samples <- l$Sample

# only select branch rate columns
indices <- unname(translation)
if (GAMMASPIKE) { rate.param <- "weightedSpikes"; indices <- indices - 1 } else { rate.param <- "branchRates" }
rate.cols <- paste(rate.param, indices, sep = ".")
l <- l[, rate.cols]

# select subset of samples
selected.rows <- sort(BURN.IN + sample(nrow(l) - BURN.IN, N.SAMPLES))
l <- l[selected.rows,]

# relabel rows, round to 6 digits
if (GAMMASPIKE) { new.param <- "burst" } else { new.param <- "rate" }
rownames(l) <- paste(new.param, all.samples[selected.rows], sep = "_")
l <- format(l, digits = 6, scientific = FALSE)

# transpose, label rows
df <- data.frame(t(l))
df$lang <- names(translation)
df <- df[, c(ncol(df), 1:(ncol(df) - 1))]

# write out
if (GAMMASPIKE) { dir <- "gammaspike" } else { dir <- "relaxed" }
file.out <- paste0("data/phylo/", dir, "/full/IndoEuropean.csv")
write.csv(df, file.out, quote = FALSE, row.names = FALSE)
cat(paste("Wrote out", N.SAMPLES, "log samples to", file.out, "\n"))
