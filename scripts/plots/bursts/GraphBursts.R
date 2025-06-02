library(ggplot2)
library(ggdist)
source("scripts/gammaspike/SummaryTree.R")
source("scripts/gammaspike/FullPosterior.R")

FAMILY <- ITALIC
df <- get_full_log(FAMILY)

cherries <- get_summary_cherries(FAMILY)

translation <- get_translation(FAMILY)

result.df <- setNames(data.frame(matrix(ncol = 4, nrow = 0)), c("burst", "name", "cherry", "s"))
for (cherry in cherries) {
  l1 <- translation[[cherry[1]]]
  l2 <- translation[[cherry[2]]]

  p1 <- paste0("weightedSpikes.", l1 - 1)
  p2 <- paste0("weightedSpikes.", l2 - 1)
  bursts.1 <- df[1:1000, p1]
  bursts.2 <- df[1:1000, p2]

  name <- paste0(cherry[1], ' ×\n', cherry[2])
  df2 <- data.frame(burst = bursts.1, name = cherry[1], cherry = name, s = "left")
  result.df <- rbind(result.df, df2)
  df3 <- data.frame(burst = bursts.2, name = cherry[2], cherry = name, s = "right")
  result.df <- rbind(result.df, df3)
}

ggplot(result.df) +
  theme_light() +
  theme(legend.position = "none",
        axis.text = element_text(size = 11),
        axis.title = element_text(size = 14)) +
  aes(x = cherry, y = burst, fill = s, side = s) +  #
  stat_slab(aes(fill_ramp = after_stat(level)),
            # .width = c(.5, .89, 1), scale = 1.1, width = 0.7, normalize = "xy", trim = FALSE
            .width = c(.5, .89, 1), scale = .18, width = 1, normalize = "groups",
  ) +
  coord_cartesian(ylim = c(0, 0.02))  # 0.3, 0.05
