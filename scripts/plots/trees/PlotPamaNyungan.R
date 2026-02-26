library(ggplot2)
library(ggtree)
library(treeio)
library(phytools)
library(tidytree)

tree <- read.beast("data/relaxed/PamaNyungan.nex")
tree <- tree_subset(tree, "Yiningay", levels_back = 9)
# write.beast(tree, "data/relaxed/PamaMaric.nex", translate = FALSE, tree.name = "summary")
tree <- as.phylo(tree)

# Force all present day
tree <- force.ultrametric(tree, method = "nnls")
ggtree(tree) + geom_tiplab(as_ylab = TRUE)

lineages <- ltt(tree, plot = FALSE)
df <- data.frame(lineages = lineages$ltt, times = lineages$times)
df$times <- df$times - max(df$times)
df$log.lineages <- log(df$lineages)

ggplot(df, aes(x = times, y = log.lineages)) +
  geom_line() +
  theme_classic() +
  geom_vline(xintercept = 0, color = "darkgrey") +
  geom_vline(xintercept = -.160, linetype = "dashed", color = "darkgrey")

print(write.tree(tree, digits = 7))