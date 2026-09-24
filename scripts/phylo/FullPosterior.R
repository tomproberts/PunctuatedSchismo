get_burn_in <- function(family, gammaspike = TRUE) {
  if (family == INDO.EUROPEAN) return(1000)
  if (family == DRAVIDIAN) return(1500)
  if (family == URALIC) return(350)
  if (family == SINO.TIBETAN) return(500)
  return(0)
}

get_translation <- function(family, gammaspike = TRUE) {
  type <- if (gammaspike) "gammaspike" else "relaxed"
  t <- read.csv(paste0("data/phylo/", type, "/translations/", family, ".translation"))
  translation <- t$node
  names(translation) <- t$ascii_name
  return(translation)
}

get_full_log <- function(family, gammaspike = TRUE) {
  type <- if (gammaspike) "gammaspike" else "relaxed"
  df <- read.csv(paste0("data/phylo/", type, "/full/", family, ".log"), sep = "\t", comment.char = "#")
  return(df[(get_burn_in(family, gammaspike) + 1):nrow(df),])
}
