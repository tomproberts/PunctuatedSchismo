library(brms)
library(marginaleffects)
library(ggplot2)
library(bayesplot)

if (!exists("bursts")) {
  bursts <- read.csv("data/gammaspike/summarytree/Douglas.csv")
  page.counts <- read.csv("data/predictors/grambank_pageCounts.csv")
  page.counts <- page.counts[, c("glcode", "total_pages")]
  areas <- read.csv("data/predictors/area/IndoEuropean.geodesic.csv")
  distances <- read.csv("data/predictors/contact/IndoEuropean.contact.geodesic.csv")
}

lang1 <- c("gheg1238", "tsak1248", "capp1239", "nucl1235", "tokh1242", "fran1269", "stan1289", "olds1249", "port1283", "friu1240", "ital1282", "sout2614", "megl1237", "osca1245", "vann1244", "corn1251", "midd1363", "manx1243", "norw1259", "elfd1234", "icel1247", "dutc1256", "stan1295", "stan1293", "bela1254", "czec1258", "kash1274", "lowe1385", "sout3278", "slov1268", "east2282", "assa1263", "hind1269", "kala1373", "east2308", "khow1242", "digo1242", "sogd1245", "sari1246", "sout2645", "maza1291", "hawr1243", "feyl1238", "hitt1242")
lang2 <- c("alba1267", "prop1240", "pont1253", "homs1234", "tokh1243", "stan1290", "oldc1251", "stan1288", "braz1246", "ladi1250", "mila1243", "barb1262", "roma1327", "umbr1253", "treg1244", "midd1380", "nort2668", "scot1245", "norw1262", "swed1254", "oldn1244", "west2354", "swis1247", "olde1238", "ukra1253", "slov1269", "poli1260", "uppe1395", "sout3277", "lowe1384", "latv1249", "beng1280", "urdu1245", "ashr1238", "west2372", "nort2665", "iron1242", "yagn1238", "wakh1245", "lari1253", "take1255", "cent1972", "koly1245", "cune1239")

# Init df
df <- data.frame(matrix(ncol = 0, nrow = (2 * length(lang1))))
df$lang <- append(lang1, lang2)
df$lang_sister <- append(lang2, lang1)
df$cherry <- append(seq_along(lang1), seq_along(lang2))
df$cherry <- factor(df$cherry)

# Exclude ancestors
df <- df[df$cherry != 9,]
df <- df[df$cherry != 16,]
df <- df[df$cherry != 21,]
df <- df[df$cherry != 24,]

# Burst
df <- merge(df, bursts, by.x = "lang", by.y = "Glottocode")

# Pages
df <- merge(df, page.counts, by.x = "lang", by.y = "glcode", all.x = TRUE)
df[is.na(df$total_pages),]$total_pages <- 1

# Areas
df <- merge(df, areas, by.x = "lang", by.y = "glottocode")
df$area_geodesic <- df$area_geodesic

# Contact
df <- merge(df, distances, by.x = c("lang", "lang_sister"), by.y = c("language_1", "language_2"))
df$median_distance <- df$median_distance
df$mean_distance <- df$mean_distance

# Sisters
df <- merge(df, df[, c("lang", "weightedSpikes_median", "total_pages", "area_geodesic", "median_distance")],
            by.x = "lang_sister", by.y = "lang", suffixes = c("", "_sister"))

df$burst <- log(df$weightedSpikes_median / df$weightedSpikes_median_sister)
df$area_ratio <- log(df$area_geodesic / df$area_geodesic_sister) / 10
df$pages_ratio <- log(df$total_pages / df$total_pages_sister)
df$distance_diff <- df$median_distance - df$median_distance_sister
df$log_total_pages <- log(df$total_pages)
df$log_area_geodesic <- log(df$area_geodesic)
df$log_area_geodesic_sister <- log(df$area_geodesic_sister)
df$median_distance[df$median_distance < 0.1] <- 0.1
df$log_median_distance <- log(df$median_distance)

if (FALSE) {
  ggplot(df, aes(x = log_median_distance, y = weightedSpikes_median)) +
    geom_text(data = df, aes(label = Name), size = 4) +
    geom_smooth(method = "glm", method.args = list(family = Gamma(link = "log")), formula = y ~ x) +
    ylim(1, 10) +
    theme_classic()
}

# Fit the model
if (TRUE) {
  fit <- brm(formula = weightedSpikes_median ~
    # (1 | cherry) +
    log_total_pages +
      log(median_distance) +
      log_area_geodesic_sister +
      log_area_geodesic,
             family = Gamma(link = "log"),
             data = df)
  save(fit, file = "data/glm/basic.RData")
}

# Graph brms
if (exists("fit")) {
  print(summary(fit))
  plot_predictions(fit, condition = "median_distance", allow_new_levels = TRUE) +
    # geom_text(aes(x = median_distance_km, y = response, label = Name), position = position_nudge(y = -0.08), data = df, size = 4) +
    # geom_point(aes(x = median_distance_km, y = response), data = df, size = 1) +
    xlab("Median distance from sibling [~km]") +
    ylab("Expected punctuated change [# lexeme changes]") +
    ggtitle("Constrained spikes ~ median_distance") +
    # xlim(0, 100) +
    theme_classic() +
    theme(axis.title = element_text(size = 14))
}
