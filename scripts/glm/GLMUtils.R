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
  cat(paste0("Setting up a GLM for ", family, " [", format(formula), "]...\n"))
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
    df$burst <- df$weightedSpikes_median   # each a csv column, weightedSpikes_0, weightedSpikes_10000, etc.
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
  filename <- paste0("data/glm/data.", family, ".csv")
  write.csv(df, filename, quote = FALSE, row.names = FALSE)
  cat(paste0("Saved prepared data to '", filename, "'\n"))
}

read.prepared.df <- function(family) {
  file.name <- paste0("data/glm/data.", family, ".csv")
  if (!file.exists(file.name))
    stop(paste0("Could not find prepared '", file.name, "', have you run DataPrep.R?"))
  return(read.csv(file.name))
}

params.to.string <- function(params) {
  if (!is.null(params) && params == "") params <- NULL
  return(paste("", params, sep = ".", collapse = "", recycle0 = TRUE))
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

get.loans.df <- function(family) {
  loans.df <- NULL
  if (family == INDO.EUROPEAN) {
    loans.df <- read.csv("data/predictors/loans/IndoEuropean.csv")
    loans.df$p_loans <- 100 * loans.df$n_loans / 170
  } else if (family == PAMA.NYUNGAN) {
    loans.df <- read.csv("data/datasets/chirila/LoanStats.csv")
    loans.df$lang <- loans.df$NameNoSpaces
    loans.df$n_loans <- loans.df$NumLoans
    loans.df$p_loans <- 100 * loans.df$NumLoans / loans.df$numberofforms
  } else stop(paste0("get.loans called for unrecognised family '", family, "'"))

  # select number and proportion of loans
  loans.df <- loans.df[, c('lang', 'n_loans', 'p_loans')]
  return(loans.df)
}

get.water.csv <- function(family, sample.points = NULL, type = NULL) {
  # set defaults
  if (is.null(sample.points)) sample.points <- 50
  if (is.null(type)) {
    if (family == INDO.EUROPEAN) type <- "polygons"
    if (family == PAMA.NYUNGAN) type <- "all"
  }

  filename <- paste0("data/predictors/water/", family, ".water.", type, ".", sample.points, ".csv")
  return(filename)
}

get.areas.csv <- function(family) {
  filename <- paste0("data/predictors/area/", family, ".geodesic.csv")
  return(filename)
}

get.contact.csv <- function(family, sample.points = NULL, symmetric = NULL) {
  # set defaults
  if (is.null(symmetric)) symmetric <- FALSE
  if (is.null(sample.points)) {
    if (symmetric) sample.points <- 50
    else sample.points <- 500
  }
  if (symmetric) type <- "symmetric"
  else type <- "contact"

  filename <- paste0("data/predictors/contact/", family, ".", type, ".", sample.points, ".csv")
  return(filename)
}
