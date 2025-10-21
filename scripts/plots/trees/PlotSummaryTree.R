library(ggplot2)
library(ggtree)
library(treeio)
source("scripts/families/LanguageFamilies.R")

FAMILY <- UTO.AZTECAN
GAMMASPIKE <- TRUE
SCALESTUBS <- TRUE

summary.tree <- paste0("data/", if (GAMMASPIKE) "gammaspike/summarytree/" else "relaxed/", FAMILY, ".nex")
tree <- read.beast(summary.tree)
df <- as_tibble(tree)

aesthetics <- if (GAMMASPIKE) (if (SCALESTUBS)
  aes(color = weightedSpikes_median / (nstubs_median + 1)) else
  aes(color = weightedSpikes_median)) else
  aes(color = log(rate_median))

ggtree(tree, aesthetics, size = 2,) +
  # theme_tree2() +  # enable axis
  scale_color_continuous(low = "black", high = if (GAMMASPIKE) "#00bfc4" else "#8494ff") +
  geom_tiplab(color = "black", align = TRUE, as_ylab = TRUE, size = 16) +
  (if (GAMMASPIKE) geom_label2(aes(subset = nstubs_median > 0, x = branch, label = nstubs_median), fill = "black", color = "white", alpha = .5)) +
  geom_label2(aes(subset = posterior < 1, label = round(posterior, 2)), fill = "white", color = "black", alpha = .8) +
  theme(legend.position = "none")
