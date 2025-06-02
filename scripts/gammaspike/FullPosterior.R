get_burn_in <- function(family) {
  family <- check_indoeuropean(family)
  if (family == INDO.EUROPEAN) return(600)
  if (family == DRAVIDIAN) return(1500)
  if (family == URALIC) return(200)
  return(0)
}

get_translation <- function(family) {
  family <- check_indoeuropean(family)
  t <- read.csv(paste0("data/gammaspike/translations/", family, ".translation"))
  translation <- t$node
  names(translation) <- t$ascii_name
  return(translation)
}

get_full_log <- function(family) {
  family <- check_indoeuropean(family)
  df <- read.csv(paste0("data/gammaspike/full/", family, ".log"), sep = "\t", comment.char = "#")
  return(df[(get_burn_in(family) + 1):nrow(df),])
}
