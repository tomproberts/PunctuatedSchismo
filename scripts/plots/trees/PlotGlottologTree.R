library(treeio)
library(ggtree)
library(tidytree)

GLOTTOLOG.NAMES <- "data/glottolog/names/"
GLOTTOLOG.ASCII <- "data/glottolog/ascii/"
GLOTTOLOG.CODES <- "data/glottolog/glottocodes/"

TYPE <- GLOTTOLOG.NAMES
FAMILY <- "IndoEuropean"

glottolog.tree <- read.newick(paste0(TYPE, FAMILY, ".newick"))
if (TYPE == GLOTTOLOG.NAMES) {
  glottolog.tree$tip.label <-
    gsub('^.|.$', '', glottolog.tree$tip.label)
}

ggtree(glottolog.tree) +
  geom_tiplab(as_ylab = TRUE, size = 12)
