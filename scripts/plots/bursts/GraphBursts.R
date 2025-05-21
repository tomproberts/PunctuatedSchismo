library(ggplot2)
library(ggdist)
library(HDInterval)
source("scripts/gammaspike/SummaryTree.R")

FAMILY <- DRAVIDIAN
BURN.IN <- 2000

df <- read.csv(paste0("data/gammaspike/full/", FAMILY, ".log"), sep = "\t", comment.char = "#")
df <- df[(BURN.IN + 1):nrow(df),]

cherries <- get_summary_cherries(FAMILY)

get_translation <- function(family) {
  t <- read.csv(paste0("data/gammaspike/translations/", family, ".translation"))
  translation <- t$node
  names(translation) <- t$ascii_name
  return(translation)
}

translation <- get_translation(FAMILY)

cherry <- cherries[[1]]
l1 <- translation[[cherry[1]]]
l2 <- translation[[cherry[2]]]

p1 <- paste0("weightedSpikes.", l1)
bursts.1 <- df[, p1]
bursts.2 <- df[, paste0("weightedSpikes.", l2)]

# hdi.int <- hdi(bursts.1, credMass = 0.95)
# bursts.1 <- bursts.1[bursts.1 > hdi.int["lower"] & bursts.1 < hdi.int["upper"]]
# hdi.int <- hdi(bursts.2, credMass = 0.95)
# bursts.2 <- bursts.2[bursts.2 > hdi.int["lower"] & bursts.2 < hdi.int["upper"]]
name <- paste0(cherry[1], '×\n', cherry[2])
df2 <- data.frame(burst = bursts.1, name = cherry[1], g = name, s = "left")
df3 <- data.frame(burst = bursts.2, name = cherry[2], g = name, s = "right")
df2 <- rbind(df2, df3)

ggplot(df2) +
  theme_light() +
  theme(legend.position = "none",
        axis.text = element_text(size = 11),
        axis.title = element_text(size = 14)) +
  aes(x = g, y = burst, fill = s, side = s) +  #
  stat_halfeye()
