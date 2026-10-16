library(ggplot2)
source("scripts/families/LanguageFamilies.R")
source("scripts/glm/GLMUtils.R")

FAMILY <- PAMA.NYUNGAN
df <- read.prepared.df(FAMILY)

x <- log(df$area)
x.label <- "log(area)"
y <- log(df$water_availability)
y.label <- "log(water availability)"

r <- cor(x, y, method = 'pearson')
TITLE <- paste0("Pama-Nyungan, r = ", sprintf("%.3f", r))

ggplot() +
  theme_light() +
  theme(
    legend.position = "none",
    text = element_text(family = "Linux Biolinum"),
    # axis.text.x=element_blank(),
    axis.text = element_text(size = 17),
    axis.title = element_text(size = 15),
    plot.title = element_text(size = 15),
    plot.margin = margin(t = 5, r = 10, b = 2, l = 2)
  ) +
  geom_point(
    aes(x = x, y = y),
    colour = "#00bfc4"
    # shape = 4,
    # size = 3
  ) +
  coord_cartesian(xlim = c(5, 13.6), ylim = c(-12, -4), expand = 1) +
  ggtitle(TITLE) +
  xlab("log(area)") +
  ylab("log(water availability)")

ggsave('./data/predictors/correlation-pn.pdf', device = cairo_pdf, width = 10, height = 10, units = "cm", dpi = 300)
