# Read data
df <- read.csv("data/datasets/chirila/concepts.csv")
df[order(df$n_cognates), "rank"] <- 1:200

# Assign classes
df[(df$rank > 0 & df$rank <= 25), "rate.class"] <- "A"
df[(df$rank > 25 & df$rank <= 50), "rate.class"] <- "B"
df[(df$rank > 50 & df$rank <= 75), "rate.class"] <- "C"
df[(df$rank > 75 & df$rank <= 100), "rate.class"] <- "D"
df[(df$rank > 100 & df$rank <= 125), "rate.class"] <- "E"
df[(df$rank > 125 & df$rank <= 144), "rate.class"] <- "F"
df[(df$rank > 144 & df$rank <= 165), "rate.class"] <- "G"
df[(df$rank > 165 & df$rank <= 175), "rate.class"] <- "H"
df[(df$rank > 175 & df$rank <= 192), "rate.class"] <- "I"
df[(df$rank > 192 & df$rank <= 200), "rate.class"] <- "J"
ggplot(df, aes(x = rank, y = n_cognates)) + geom_bar(stat = "identity", aes(fill = rate.class))

# Filter
df$range <- paste(df$starts, df$ends, sep = "-")
cat("\n\n--------------\nRate classes and their sites\n\n--------------")
for (c in unique(df[order(df$rank), "rate.class"])) {
  cat("\n----\nrate"); cat(c); cat(":\n")
  cat(paste(df[df$rate.class == c,]$range, sep = ",", collapse = ","))
}
