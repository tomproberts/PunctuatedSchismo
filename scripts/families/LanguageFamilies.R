ITALIC <- "Italic"
INDO.EUROPEAN <- "IndoEuropean"
DRAVIDIAN <- "Dravidian"
URALIC <- "Uralic"

get_n_sites <- function(family) {
  if (family == ITALIC || family == INDO.EUROPEAN) return (4958)
  if (family == DRAVIDIAN) return (877)
  if (family == URALIC) return (3655)
}