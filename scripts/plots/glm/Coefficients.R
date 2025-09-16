library(ggplot2)
library(ggdist)
library(tidyr)
library(dplyr)

load("data/glm/IndoEuropean.RData")

par.names <- c(
  "log(median distance)" = "b_logmedian_distance",
  "log(area)" = "b_log_area_geodesic",
  "log(area of sister)" = "b_log_area_geodesic_sister",
  "log(total pages)" = "b_log_total_pages",
  "number of loans" = "b_n_loans"
)

draws <- as.data.frame(fit)
pars <- colnames(draws)
pars <- pars[sapply(pars, function(n) return(startsWith(n, "b_") & n != "b_Intercept"))]

draws <- draws[, pars]
draws.df <- pivot_longer(rename(draws, any_of(par.names)), cols = everything(), names_to = "coefficient", values_to = "value")

ggplot(draws.df, aes(x = value, y = coefficient)) +
  theme_light() +
  theme(legend.position = "none",
        axis.text = element_text(size = 10),
        axis.title = element_text(size = 12)) +
  stat_interval(aes(interval_alpha = after_stat(level)),
                .width = c(0.5, 0.89, 1),
                interval_colour = "#00bfc4", linewidth = 6) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "darkgrey") +
  ylab("")

# mcmc_areas(fit, prob = 0.89, pars = pars)

# pp_check(fit, type = "dens_overlay", ndraws = 100)
