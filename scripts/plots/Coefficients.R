library(ggplot2)
library(ggdist)
library(tidyr)
library(dplyr)
library(stringr)
library(brms)
library(systemfonts)
library(patchwork)

FIT <- "../../data/glm/glm-iepunc-loans.RData"
fit <- readRDS(FIT)

set.seed(42)

r2 <- bayes_R2(fit, probs = c(0.055, 0.945))
TITLE <- paste0("Indo-European, R² = ", sprintf("%.3f", r2[1]), " (", sprintf("%.3f", r2[3]), ", ", sprintf("%.3f", r2[4]), ")")
X.LABEL <- "effect on punctuated change"

par.names <- rev(c(
  "number of loans" = "b_n_loans",
  "sister’s number of loans" = "b_n_loans_sister",
  "proportion of loans" = "b_p_loans",
  "sister’s loan proportion" = "b_p_loans_sister",
  "log(area)" = "b_logarea",
  "log(sister’s area)" = "b_logarea_sister",
  "log(distance to water)" = "b_logmedian_distance_water",
  "log(sister’s distance to water)" = "b_logmedian_distance_water_sister",
  "log(distance from sister)" = "b_logmedian_distance",
  "log(water availability)" = "b_logwater_availability",
  "log(sister’s water availability)" = "b_logwater_availability_sister",
  "log(area/area of sister)" = "b_area_ratio"
))

exclude <- c(
  "b_Intercept"
)

fit <- readRDS(FIT)
draws <- as.data.frame(fit)
pars <- colnames(draws)
pars <- pars[startsWith(pars, "b_") & !(pars %in% exclude)]

draws <- draws[, pars]
if (length(pars) == 1) {
  draws <- sample(draws, min(10000, length(draws)))
  draws.df <- data.frame(value = draws, coefficient = names(par.names)[par.names == pars])
} else {
  draws <- sample_n(draws, min(10000, nrow(draws)))
  draws.df <- pivot_longer(rename(draws, any_of(par.names)), cols = everything(), names_to = "coefficient", values_to = "value")
}
draws.df$coefficient <- factor(draws.df$coefficient, levels = names(par.names))

#ie <-
ggplot(draws.df, aes(x = value, y = coefficient)) +
  theme_light() +
  theme(
    legend.position = "none",
    text = element_text(family = "Linux Biolinum"),
    # axis.text.x=element_blank(),
    axis.text = element_text(size = 17),
    axis.title = element_text(size = 15),
    plot.title = element_text(size = 15),
    plot.margin = margin(t = 5, r = 5, b = 2, l = -10)
  ) +
  stat_interval(aes(interval_alpha = after_stat(level)),
                .width = c(0.5, 0.89, 0.99),
                interval_colour = "#00bfc4", linewidth = 7) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "darkgrey") +
  # xlim(-0.11, 0.13) +  # for area in IE
  # xlim(-0.22, 0.26) +  # for water in PN
  ggtitle(TITLE) +
  xlab(X.LABEL) +
  ylab("")

# Save as pdfs
ggsave(
  filename = str_replace_all(FIT, ".RData", ".pdf"),
  device = cairo_pdf,
  width = 25, height = 2.6 + 0.85 * length(pars),
  units = "cm", dpi = 300
)

# ie / pn + plot_annotation(theme = theme(plot.margin = margin(l = -10)))
# ggsave('./glm-both-main.pdf', device = cairo_pdf, width = 25, height = 11, units = "cm", dpi = 300)
