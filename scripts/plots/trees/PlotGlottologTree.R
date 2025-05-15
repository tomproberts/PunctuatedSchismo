library(treeio)
library(ggtree)
library(tidytree)

GLOTTOLOG.DIR <- "data/glottolog/"

# names|ascii|glottocodes|id
TYPE <- "names"
FAMILY <- "UtoAztecan"

glottolog.tree <- read.newick(paste0(GLOTTOLOG.DIR, TYPE, ".", FAMILY, ".newick"))
if (TYPE == "names") {
  glottolog.tree$tip.label <-
    gsub('^.|.$', '', glottolog.tree$tip.label)
}

ggtree(glottolog.tree) +
  geom_tiplab(as_ylab = TRUE, size = 12)
