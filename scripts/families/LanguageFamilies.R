ITALIC <- "Italic"
INDO.EUROPEAN <- "IndoEuropean"
DRAVIDIAN <- "Dravidian"
URALIC <- "Uralic"

get_n_sites <- function(family) {
  if (family == ITALIC || family == INDO.EUROPEAN) 4958
  if (family == DRAVIDIAN) 877
  if (family == URALIC) 3655
}