library(ggdist)

load("data/glm/basic.RData")

draws <- as.data.frame(fit)

draws.df <- data.frame(coefficient="log(area_cartesian)", value=draws$b_log_area_cartesian)

ggplot(draws.df, aes(x = value, y = coefficient)) +
  theme_light() +
  theme(legend.position = "none",
        axis.text = element_text(size = 12),
        axis.title = element_text(size = 18)) +
  stat_interval(aes(interval_alpha = after_stat(level)),
                .width = c(0.5, 0.89, 1),
                interval_colour="#00bfc4",linewidth=6) +
  geom_vline(xintercept=0, linetype="dashed", color = "darkgrey") +
  ylab("") +
  ggtitle("Indo-European")
