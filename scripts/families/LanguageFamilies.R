ITALIC <- "Italic"
DOUGLAS <- "Douglas"
INDO.EUROPEAN <- "IndoEuropean"
DRAVIDIAN <- "Dravidian"
URALIC <- "Uralic"

get_n_sites <- function(family) {
  family <- check_indoeuropean(family)
  if (family == INDO.EUROPEAN) return(4958)
  if (family == DOUGLAS) return(4990)
  if (family == DRAVIDIAN) return(877)
  if (family == URALIC) return(3655)
}

check_indoeuropean <- function(family) {
  if (family == ITALIC) return(INDO.EUROPEAN)
  return(family)
}
