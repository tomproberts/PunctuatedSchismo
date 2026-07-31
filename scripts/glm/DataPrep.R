library(collapse)
source("scripts/gammaspike/SummaryTree.R")
source("scripts/glm/GLMUtils.R")

FAMILY <- INDO.EUROPEAN

distances <- read.csv(paste0("data/predictors/contact/", FAMILY, ".contact.500.csv"))
areas <- read.csv(paste0("data/predictors/area/", FAMILY, ".geodesic.csv"))
water <- read.csv(paste0("data/predictors/water/", FAMILY, ".water.polygons.50.csv"))
loans <- read.csv("data/predictors/loans/IndoEuropean.csv")

cherries <- get_summary_cherries(FAMILY)
lang1 <- sapply(cherries, function(e) return(e[1]))
lang2 <- sapply(cherries, function(e) return(e[2]))

# Init df
df <- data.frame(matrix(ncol = 0, nrow = (2 * length(cherries))))
df$lang <- append(lang1, lang2)
df$lang_sister <- append(lang2, lang1)
df$cherry <- factor(append(seq_along(lang1), seq_along(lang2)))

# Exclude sampled ancestors
if (FAMILY == INDO.EUROPEAN) {
  to.remove <- c("Portuguese", "LateCornish", "Icelandic", "English", "MiddleWelsh")
  df <- df[df$cherry %!in% sapply(to.remove, function(l) return(df[df$lang == l,]$cherry)),]
}

# Loans
df <- merge(df, loans[, c("lang", "n_loans")], by.x = "lang", by.y = "lang", all.x = TRUE)
df[is.na(df$n_loans),]$n_loans <- 0

# Areas
df <- merge(df, areas, by.x = "lang", by.y = "lang")

# Contact
df <- merge(df, distances, by.x = c("lang", "lang_sister"), by.y = c("language_1", "language_2"))
df$median_distance[df$median_distance < 1] <- 1  # for some EPSILON=1

# Water
df <- merge(df, water, by.x = "lang", by.y = "lang", suffixes = c("", "_water"), all.x = TRUE)
df$mean_distance_water[is.na(df$mean_distance_water)] <- 100000
df$median_distance_water[is.na(df$median_distance_water)] <- 100000

# Sisters
df <- merge(df, df[, c("lang", "area", "median_distance", "median_distance_water")],
            by.x = "lang_sister", by.y = "lang", suffixes = c("", "_sister"))

# Area ratio
df$area_ratio <- log(df$area / df$area_sister)

# Write out dataframe
write.prepared.df(df, FAMILY)
