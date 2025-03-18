library(treeio)
library(ggtree)
library(tidytree)

glottolog.tree <- read.newick("data/glottolog/names/italic.newick")
tibble <- as.data.frame(as_tibble(glottolog.tree))

ggtree(glottolog.tree) +
  geom_tiplab(as_ylab = TRUE, size = 12)
