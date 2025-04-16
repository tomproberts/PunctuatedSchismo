ITALIC <- "Italic"
INDO.EUROPEAN <- "IndoEuropean"
DRAVIDIAN <- "Dravidian"

get_n_taxa <- function(family) {
  if (family == ITALIC || family == INDO.EUROPEAN) 4958
  if (family == DRAVIDIAN) 877
}