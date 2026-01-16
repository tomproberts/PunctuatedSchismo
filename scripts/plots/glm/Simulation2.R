# Simulation for response variable uncertainty

require(ggplot2)

set.seed(42)
NUMBER <- 20
SLOPE <- 0.5
SPREAD <- 2.5
NOISE <- 2
xs <- runif(NUMBER, 5, 20)
df <- data.frame(xs)
df$sd <- rexp(NUMBER, 5) * SPREAD

df$ys <- xs * SLOPE
df$ys_lower <- df$ys - df$sd
df$ys_upper <- df$ys + df$sd

df$zs <- rnorm(NUMBER, df$ys, df$sd) + rnorm(NUMBER, 0, NOISE)
df$zs_lower <- df$zs - df$sd
df$zs_upper <- df$zs + df$sd

ggplot(df, aes(x = xs, y = zs)) +
  geom_point(colour="red") +
  # geom_point(aes(y=ys), colour="blue") +
  # geom_errorbar(aes(ymin=ys_lower, ymax=ys_upper), colour="blue") +
  geom_errorbar(aes(ymin=zs_lower, ymax=zs_upper), colour="red") +
  geom_smooth(method = 'lm', formula = df$zs ~ x, colour="red") +
  geom_smooth(method = 'lm', formula = df$ys ~ x, colour="blue") +
  theme_classic()