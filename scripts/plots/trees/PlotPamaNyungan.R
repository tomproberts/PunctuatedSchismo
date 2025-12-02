library(ggplot2)
library(ggtree)
library(treeio)
library(phytools)

tree <- read.beast("data/gammaspike/summarytree/PamaNyungan.nex")
tree <- as.phylo(tree)
# tree <- ape::read.tree(text = "((A:0.5, B:1):3, ((C:2, D:2):1, (E:1.5, F:0.75):1.5):1);")

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