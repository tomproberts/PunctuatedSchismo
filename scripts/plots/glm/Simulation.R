# Simulation for negatively correlated area and area-of-sister

require(ggplot2)
require(gridExtra)

set.seed(42)
NUMBER <- 20
SLOPE <- 0.2
as <- paste0("language", 1:NUMBER, ".a")
bs <- paste0("language", 1:NUMBER, ".b")
lang <- append(as, bs)
sibling <- append(bs, as)
area.as <- runif(NUMBER, 50, 200)
area.bs <- runif(NUMBER, 10, 160)
area <- append(area.as, area.bs)
NOISE <- 10
burst <- sapply(area, function(x) SLOPE * x + rnorm(1, 0, NOISE))

df <- data.frame(lang, area, burst, sibling)
df <- merge(df, df[, c("lang", "area")], by.x = "sibling", by.y = "lang", suffixes = c("", "_sister"))

plot1 <- ggplot(df, aes(x = area, y = burst)) +
  geom_smooth(method = 'lm', formula = y ~ x) +
  xlim(0, 200)

plot2 <- ggplot(df, aes(x = area_sister, y = burst)) +
  geom_smooth(method = 'lm', formula = y ~ x) +
  xlim(0, 200)

plot3 <- ggplot(df, aes(x = area, y = area_sister)) +
  geom_smooth(method = 'lm', formula = y ~ x) +
  xlim(0, 200) +
  ylim(0, 200)

grid.arrange(plot1, plot2, plot3, ncol=3)
