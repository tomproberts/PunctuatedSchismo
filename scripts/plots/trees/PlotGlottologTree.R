library(treeio)
library(ggtree)
library(tidytree)

GLOTTOLOG.NAMES <- "data/glottolog/names/"
GLOTTOLOG.CODES <- "data/glottolog/glottocodes/"

glottolog.tree <- read.newick(paste0(GLOTTOLOG.CODES, "Italic", ".newick"))

ggtree(glottolog.tree) +
  geom_tiplab(as_ylab = TRUE, size = 12)
