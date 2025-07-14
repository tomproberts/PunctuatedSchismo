library(ggplot2)
library(ggtree)
library(treeio)
source("scripts/families/LanguageFamilies.R")

# Think about how number of taxa affects gammaShape etc.
FAMILY <- SINO.TIBETAN
SCALESTUBS <- TRUE

summary.tree <- paste0("data/gammaspike/summarytree/", FAMILY, ".nex")
tree <- read.beast(summary.tree)
df <- as_tibble(tree)
df$scaled_spikes <- df$weightedSpikes_median * get_n_sites(FAMILY) / 2

aesthetics <- if (SCALESTUBS)
  aes(color = weightedSpikes_median / (nstubs_median + 1)) else
  aes(color = weightedSpikes_median)

ggtree(tree, aesthetics, size = 2,) +
  # theme_tree2() +  # enable axis
  scale_color_continuous(low = 'black', high = '#00bfc4') +
  geom_tiplab(color = 'black', align = TRUE, as_ylab = TRUE, size = 16) +
  geom_label2(aes(subset = nstubs_median > 0, x = branch, label = nstubs_median), fill = 'black', color = 'white', alpha = .5) +
  geom_label2(aes(subset = posterior < 1, label = round(posterior, 2)), fill = 'white', color = 'black', alpha = .8) +
  theme(legend.position = "none")
