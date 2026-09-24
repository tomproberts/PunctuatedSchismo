library(ggplot2)
library(ggdist)
library(systemfonts)
source("scripts/phylo/SummaryTree.R")
source("scripts/phylo/FullPosterior.R")

FAMILY <- PAMA.NYUNGAN
GAMMASPIKE <- FALSE
df <- get_full_log(FAMILY, GAMMASPIKE)

cherries <- get_manual_cherries(FAMILY)
translation <- get_translation(FAMILY, GAMMASPIKE)

#df <- df[1:500,]
clock.rates <- df$clockRate
result.df <- data.frame(matrix(ncol = 4, nrow = 0))
names(result.df) <- c("response", "name", "cherry", "side")
for (cherry in cherries) {
  l1 <- translation[[cherry[1]]]
  l2 <- translation[[cherry[2]]]
  if (GAMMASPIKE) {
    normalise <- 1
    p1 <- paste0("weightedSpikes.", l1 - 1)
    p2 <- paste0("weightedSpikes.", l2 - 1)
  } else {
    normalise <- clock.rates
    if (FAMILY == PAMA.NYUNGAN) normalise <- normalise * 1000
    p1 <- paste0("branchRates.", l1)
    p2 <- paste0("branchRates.", l2)
  }
  responses.1 <- df[, p1] * normalise
  responses.2 <- df[, p2] * normalise

  name <- paste0(cherry[1], ' ×\n', cherry[2])
  df2 <- data.frame(response = responses.1, name = cherry[1], cherry = name, side = "left")
  result.df <- rbind(result.df, df2)
  df3 <- data.frame(response = responses.2, name = cherry[2], cherry = name, side = "right")
  result.df <- rbind(result.df, df3)
}

response.to.percentage <- 0.5 * get_n_sites(FAMILY) / get_n_concepts(FAMILY) * 100
result.df$response <- result.df$response * response.to.percentage
#average.clockrate <- mean(normalise) * response.to.percentage  # should be around 7.84%?

y.label <- if (GAMMASPIKE) "punctuated change (% vocab)" else "branch rate (% vocab/Ka)"

ggplot(result.df) +
  theme_light() +
  theme(
    legend.position = "none",
    plot.margin = margin(t = 10, r = 5, b = -10, l = 5),
    text = element_text(family = "Linux Biolinum"),
    axis.text = element_text(size = 14),
    axis.title = element_text(size = 18)
  ) +
  aes(x = cherry, y = response, fill = side, side = side) +
  stat_slab(aes(fill_ramp = after_stat(level)),
            # .width = c(.5, .89, 1), scale = 1.1, width = 0.7, normalize = "xy", trim = FALSE
            .width = c(.5, .89, 1), scale = .6, width = 1, normalize = "groups",
  ) +
  # (if (!GAMMASPIKE) geom_hline(yintercept = average.clockrate, linetype = "dashed", color = "darkgrey"))+
  coord_cartesian(ylim = c(0, 40), expand = 0) +
  xlab("") +
  ylab(y.label)

# ggsave('./yortaRates.pdf', device = cairo_pdf, width = 89.3, height = 162.3, units = "mm")
