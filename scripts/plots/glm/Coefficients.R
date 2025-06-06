library(ggplot2)
library(ggdist)
library(tidyr)
library(dplyr)

load("data/glm/basic.RData")

pars <- c(
  "b_log_area_cartesian_sister",
  "b_log_area_cartesian",
  "b_log_total_pages",
  "b_logmedian_distance_km"
)

draws <- as.data.frame(fit)
draws <- draws[, pars]

draws <- rename(draws,
                "log(median distance)" = b_logmedian_distance_km,
                "log(area)" = b_log_area_cartesian,
                "log(area of sister)" = b_log_area_cartesian_sister,
                "log(total pages)" = b_log_total_pages,
)

draws.df <- pivot_longer(draws, cols = everything(), names_to = "coefficient", values_to = "value")

ggplot(draws.df, aes(x = value, y = coefficient)) +
  theme_light() +
  theme(legend.position = "none",
        axis.text = element_text(size = 12),
        axis.title = element_text(size = 18)) +
  stat_interval(aes(interval_alpha = after_stat(level)),
                .width = c(0.5, 0.89, 1),
                interval_colour = "#00bfc4", linewidth = 6) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "darkgrey") +
  ylab("")

# mcmc_areas(fit, prob = 0.89, pars = pars)

# pp_check(fit, type = "dens_overlay", ndraws = 100)
