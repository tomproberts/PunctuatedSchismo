library(ggplot2)
library(ggdist)
library(tidyr)
library(dplyr)

FIT <- "data/glm/IndoEuropean.RData"

par.names <- c(
  "log(total pages)" = "b_log_total_pages",
  "log(area)" = "b_logarea",
  "log(sister's area)" = "b_logarea_sister",
  "log(area/area of sister)" = "b_area_ratio",
  "log(total pages of sister)" = "b_log_total_page_sister",
  "number of loans" = "b_n_loans",
  "log(distance to water)" = "b_logmedian_distance_water",
  "log(sister's distance to water)" = "b_logmedian_distance_water_sister",
  "log(distance from sister)" = "b_logmedian_distance"
)

exclude <- c(
  "b_Intercept"
)

load(FIT)
draws <- as.data.frame(fit)
pars <- colnames(draws)
pars <- pars[sapply(pars, function(n) return(startsWith(n, "b_") & !(n %in% exclude)))]

draws <- draws[, pars]
if (length(pars) == 1) {
  draws.df <- data.frame(value = draws, coefficient = names(par.names)[par.names == pars])
} else {
  draws.df <- pivot_longer(rename(draws, any_of(par.names)), cols = everything(), names_to = "coefficient", values_to = "value")
}
draws.df$coefficient <- factor(draws.df$coefficient, levels = names(par.names))

ggplot(draws.df, aes(x = value, y = coefficient)) +
  theme_light() +
  theme(legend.position = "none",
        axis.text = element_text(size = 16),
        axis.title = element_text(size = 12)) +
  stat_interval(aes(interval_alpha = after_stat(level)),
                .width = c(0.5, 0.89, 1),
                interval_colour = "#00bfc4", linewidth = 6) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "darkgrey") +
  xlim(-0.25, 0.25) +
  ggtitle(FIT) +
  xlab("effect on punctuated change") +
  ylab("")
