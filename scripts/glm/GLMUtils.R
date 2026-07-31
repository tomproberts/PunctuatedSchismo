library(brms)

fit.glm <- function(family, formula, punctuated = FALSE, relaxed = FALSE, output = "data/glm/out.RData") {
  # Sanitise input
  if (punctuated && relaxed || !punctuated && !relaxed)
    stop("Either punctuated or relaxed must be set to TRUE, but not both")
  if (punctuated && formula[[2]] != "burst")
    stop("Predictor for punctuated must be 'burst'")
  if (relaxed && formula[[2]] != "rate")
    stop("Predictor for relaxed must be 'rate'")

  # Load prepared data
  cat(paste0("Setting up a GLM for ", family, " [", format(formula),  "]...\n"))
  df <- read.prepared.df(family)

  # Config
  if (punctuated) {
    exp.family <- Gamma(link = "log")
    df$burst <- 1.0
    params <- ""
  }
  if (relaxed) {
    exp.family <- gaussian(link = "log")
    df$rate <- 1.0
    params <- "relaxed"
  }

  # Pre-compile model if necessary
  c <- get.cached(family, params, strict = FALSE)
  if (is.null(c) || !(c$formula == formula)[[1]]) {
    c <- brm(formula = formula, data = df, family = exp.family, chains = 0, iter = 1000)
    cache.compiled(c, family, params)
  }

  # Fit model for summary results
  if (punctuated) {
    df <- merge(df, get.summary.bursts(family), by.x = "lang", by.y = "label")
    df$burst <- df$weightedSpikes_median
  }
  if (relaxed) {
    df <- merge(df, get.summary.rates(family), by.x = "lang", by.y = "label")
    df$rate <- df$rate_median
  }
  fit <- update(c, chains = 4, iter = 4000, newdata = df)

  # Save model output
  save.fit(fit, output)
}

write.prepared.df <- function(df, family) {
  write.csv(df, paste0("data/glm/data.", family, ".csv"), quote = FALSE, row.names = FALSE)
}

read.prepared.df <- function(family) {
  file.name <- paste0("data/glm/data.", family, ".csv")
  if (!file.exists(file.name))
    stop(paste0("Could not find prepared '", file.name, "', have you run DataPrep.R?"))
  return(read.csv(file.name))
}

params.to.string <- function (params) {
  if (!is.null(params) && params == "") params <- NULL
  return (paste("", params, sep = ".", collapse = "", recycle0 = TRUE))
}

cache.compiled <- function(compiled, family, params = NULL) {
  filename <- paste0("data/glm/compiled.", family, params.to.string(params), ".RData")
  save(compiled, file = filename)
  cat(paste0("Saved pre-compiled object to '", filename, "'\n"))
}

get.cached <- function(family, params = "", strict = TRUE) {
  filename <- paste0("data/glm/compiled.", family, params.to.string(params), ".RData")
  if (file.exists(filename)) {
    load(filename)
    cat(paste0("Retrieved pre-compiled object from '", filename, "'\n"))
    return(compiled)
  }
  if (strict) stop(paste0("Could not find cached model '", filename, "'"))

  return(NULL)
}

get.summary.bursts <- function(family) {
  return(read.csv(paste0("data/phylo/gammaspike/summary/", family, ".csv")))
}

get.summary.rates <- function(family) {
  return(read.csv(paste0("data/phylo/relaxed/summary/", family, ".csv")))
}

save.fit <- function(fit, file.name) {
  save(fit, file = file.name)
  cat(paste0("Wrote out fit to '", file.name, "'\n"))
}
