library(brms)
library(marginaleffects)
library(ggplot2)
library(bayesplot)
library(collapse)
source("scripts/gammaspike/SummaryTree.R")

bursts <- read.csv("data/gammaspike/summarytree/Douglas.csv")
page.counts <- read.csv("data/predictors/grambank_pageCounts.csv")[, c("glcode", "total_pages")]
areas <- read.csv("data/predictors/area/IndoEuropean.geodesic.csv")
distances <- read.csv("data/predictors/contact/IndoEuropean.contact.geodesic.csv")

cherries <- get_summary_cherries(INDO.EUROPEAN)
lang1 <- sapply(cherries, function(e) return(e[1]))
lang2 <- sapply(cherries, function(e) return(e[2]))

# Init df
df <- data.frame(matrix(ncol = 0, nrow = (2 * length(cherries))))
df$lang <- append(lang1, lang2)
df$lang_sister <- append(lang2, lang1)
df$cherry <- append(seq_along(lang1), seq_along(lang2))

# Exclude ancestors
to.remove <- c("Portuguese", "LateCornish", "Icelandic", "English")
df <- df[df$cherry %!in% sapply(to.remove, function(l) return(df[df$lang == l,]$cherry)),]

# Burst
df <- merge(df, bursts, by.x = "lang", by.y = "label")

# Pages
df <- merge(df, page.counts, by.x = "Glottocode", by.y = "glcode", all.x = TRUE)
df[is.na(df$total_pages),]$total_pages <- 1

# Areas
df <- merge(df, areas, by.x = "Glottocode", by.y = "glottocode")

# Contact
df <- merge(df, distances, by.x = c("lang", "lang_sister"), by.y = c("language_1", "language_2"))

# Sisters TODO: Somehow removes Sardinian, Slovene is also duplicated?
df <- merge(df, df[, c("lang", "weightedSpikes_median", "total_pages", "area_geodesic", "median_distance")],
            by.x = "lang_sister", by.y = "lang", suffixes = c("", "_sister"))

EPSILON <- 1
df$burst <- log(df$weightedSpikes_median / df$weightedSpikes_median_sister)
df$area_ratio <- log(df$area_geodesic / df$area_geodesic_sister)
df$pages_ratio <- log(df$total_pages / df$total_pages_sister)
df$distance_diff <- df$median_distance - df$median_distance_sister
df$log_total_pages <- log(df$total_pages)
df$log_total_pages_sister <- log(df$total_pages_sister)
df$log_area_geodesic <- log(df$area_geodesic)
df$log_area_geodesic_sister <- log(df$area_geodesic_sister)
df$median_distance[df$median_distance < EPSILON] <- EPSILON
df$log_median_distance <- log(df$median_distance)
df$cherry <- factor(df$cherry)

if (FALSE) {
  ggplot(df, aes(x = log_median_distance, y = weightedSpikes_median)) +
    geom_text(data = df, aes(label = Name), size = 4) +
    geom_smooth(method = "glm", method.args = list(family = Gamma(link = "log")), formula = y ~ x) +
    # ylim(1, 200) +
    theme_classic()
}

# Fit the model
if (TRUE) {
  fit <- brm(formula = weightedSpikes_median ~
    # (1 | cherry) +
    # log_total_pages +
      log(median_distance) +
      log(area_geodesic) +
      log(area_geodesic_sister),
             family = Gamma(link = "log"),
             data = df,
             iter = 6000)
  save(fit, file = "data/glm/Douglas.RData")
}

# Graph brms
if (FALSE) {
  print(summary(fit))
  plot_predictions(fit, condition = "area_geodesic_sister", allow_new_levels = TRUE) +
    # geom_text(aes(x = median_distance_km, y = response, label = Name), position = position_nudge(y = -0.08), data = df, size = 4) +
    # geom_point(aes(x = median_distance_km, y = response), data = df, size = 1) +
    xlab("Area of sibling [~km^2]") +
    ylab("Expected punctuated change [# lexeme changes]") +
    ggtitle("Constrained spikes ~ median_distance") +
    xlim(0, 300000) +
    theme_classic() +
    theme(axis.title = element_text(size = 14))
}
