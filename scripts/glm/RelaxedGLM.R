library(brms)
library(marginaleffects)
library(ggplot2)
library(bayesplot)
library(collapse)
source("scripts/gammaspike/SummaryTree.R")

FAMILY <- PAMA.MARIC
rates <- read.csv(paste0("data/relaxed/", FAMILY, ".csv"))
areas <- read.csv(paste0("data/predictors/area/", FAMILY, ".geodesic.csv"))
distances <- read.csv(paste0("data/predictors/contact/", FAMILY, ".contact.500.csv"))
water <- read.csv(paste0("data/predictors/water/", FAMILY, ".water.all.50.csv"))
loans <- read.csv("data/datasets/chirila/LoanStats.csv")

cherries <- get_summary_cherries(FAMILY)
lang1 <- sapply(cherries, function(e) return(e[1]))
lang2 <- sapply(cherries, function(e) return(e[2]))

# Init df
df <- data.frame(matrix(ncol = 0, nrow = (2 * length(cherries))))
df$lang <- append(lang1, lang2)
df$lang_sister <- append(lang2, lang1)
df$cherry <- append(seq_along(lang1), seq_along(lang2))

# Rates
df <- merge(df, rates, by.x = "lang", by.y = "label")

# Areas
df <- merge(df, areas, by.x = "lang", by.y = "lang")

# Contact
df <- merge(df, distances, by.x = c("lang", "lang_sister"), by.y = c("language_1", "language_2"))

# Water
df <- merge(df, water, by.x = "lang", by.y = "lang", suffixes = c("", "_water"), all.x = TRUE)
df$mean_distance_water[is.na(df$mean_distance_water)] <- 100000
df$median_distance_water[is.na(df$median_distance_water)] <- 100000

# Loans
df <- merge(df, loans[, c("NameNoSpaces", "NumLoans", "NumHapax", "NumTotalLoans", "numberofforms")], by.x = "lang", by.y = "NameNoSpaces", all.x = TRUE)
if (nrow(df[is.na(df$NumLoans),]) > 0) df[is.na(df$NumLoans),]$NumLoans <- 0
if (nrow(df[is.na(df$numberofforms),]) > 0) df[is.na(df$numberofforms),]$numberofforms <- 1
df$n_loans <- df$NumLoans
df$p_loans <- 100 * df$NumLoans / df$numberofforms

# Sisters
df <- merge(df, df[, c("lang", "rate_median", "area", "median_distance", "median_distance_water", "n_loans", "p_loans")],
            by.x = "lang_sister", by.y = "lang", suffixes = c("", "_sister"))

EPSILON <- 1
df$area_ratio <- log(df$area / df$area_sister)
df <- df[df$median_distance != 0,]
df$median_distance[df$median_distance < EPSILON] <- EPSILON
df$log_median_distance <- log(df$median_distance)
df$normalised_rate <- df$rate / mean(df$rate)

if (FALSE) {
  ggplot(df, aes(x = log(area), y = log(area_sister))) +
    geom_text(data = df, aes(label = name), size = 4) +
    geom_smooth(method = "lm", formula = y ~ x) +
    # ylim(1, 200) +
    theme_classic()
}

# Fit the model
if (TRUE) {
  fit <- brm(formula = normalised_rate ~
    n_loans +
    log(median_distance_water) +
      log(median_distance) +
      log(median_distance_water_sister),
             family = gaussian(link = "log"),
             data = df,
             iter = 4000)
  # Save model output
  filename <- paste0("data/glm/", FAMILY, "Relaxed.RData")
  save(fit, file = filename)
  cat(paste("Wrote out fit to", filename, "\n"))
}

if (FALSE) {
  plot_predictions(fit, condition = "area_sister", allow_new_levels = TRUE) +
    # geom_text(aes(x = median_distance_km, y = response, label = Name), position = position_nudge(y = -0.08), data = df, size = 4) +
    # geom_point(aes(x = median_distance_km, y = response), data = df, size = 1) +
    xlab("Area of sibling [~km^2]") +
    ylab("Normalised branch rate") +
    ggtitle("normalised_rate ~ area_sister") +
    # xlim(0, 300000) +
    theme_classic() +
    theme(axis.title = element_text(size = 14))
}

