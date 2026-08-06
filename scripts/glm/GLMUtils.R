library(brms)
library(rstan)

fit.glm <- function(family, formula, punctuated = FALSE, relaxed = FALSE, output = "data/glm/out.RData", full = FALSE, seed = NA, thin = 20) {
  # Sanitise input
  if (punctuated && relaxed || !punctuated && !relaxed)
    stop("Either punctuated or relaxed must be set to TRUE, but not both")
  resp <- format(formula[[2]])
  if (punctuated && resp != "burst")
    stop("Predictor for punctuated must be 'burst'")
  if (relaxed && resp != "rate")
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
    c <- brm(formula = formula, data = df, family = exp.family, chains = 0, iter = 1000, seed = seed)
    cache.compiled(c, family, params)
  }

  # Load rates/burst data
  if (full) {
    # Use full posterior (downsampled)
    cat("Preparing to sample fits from posterior draws...\n")
    if (punctuated) {
      resp.df <- get.posterior.bursts(family)
      response.cols <- names(resp.df)
      response.cols <- response.cols[startsWith(response.cols, "burst_")]
    }
    if (relaxed) {
      resp.df <- get.posterior.rates(family)
      response.cols <- names(resp.df)
      response.cols <- response.cols[startsWith(response.cols, "rate_")]
    }
  } else {
    # Use summary tree data
    cat("Preparing to sample fits from summary tree data...\n")
    if (punctuated) {
      resp.df <- get.summary.bursts(family)
      response.cols <- c("weightedSpikes_median")
    }
    if (relaxed) {
      resp.df <- get.summary.rates(family)
      response.cols <- c("rate_median")
    }
    thin <- 1
  }

  # Merge into one dataframe
  df <- merge(df, resp.df, by = "lang", suffixes = c("", "."))

  # Loop through data draws and fit model, adding to list of fits
  fits <- c()
  for (i in seq_along(response.cols)) {
    # Assign selected data to response (e.g. df$burst <- df$burst_170000) and fit the model
    df[resp] <- df[, response.cols[i]]
    fit <- update(c, chains = 4, iter = 4000, newdata = df, seed = seed, thin = thin)
    fits <- c(fits, fit$fit)

    # Progress
    cat("---------\n")
    cat(paste("Fit model", i, "of", length(response.cols), "!\n"))
    cat("---------\n")
  }

  # Combine fits together
  if (full && length(fits) > 1) {
    fit <- sflist2stanfit(fits)
  }
  else fit <- fits[[1]]

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

get.posterior.rates <- function(family) {
  return(read.csv(paste0("data/phylo/relaxed/full/", family, ".csv")))
}

get.posterior.bursts <- function(family) {
  return(read.csv(paste0("data/phylo/gammaspike/full/", family, ".csv")))
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
