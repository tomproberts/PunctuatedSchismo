DOUGLAS <- "Douglas"
INDO.EUROPEAN <- "IndoEuropean"
DRAVIDIAN <- "Dravidian"
URALIC <- "Uralic"
SINO.TIBETAN <- "SinoTibetan"
UTO.AZTECAN <- "UtoAztecan"
PAMA.NYUNGAN <- "PamaNyungan"

get_n_sites <- function(family) {
  if (family == INDO.EUROPEAN) return(4958)
  if (family == DRAVIDIAN) return(877)
  if (family == URALIC) return(800)
  if (family == SINO.TIBETAN) return(3784)
  if (family == UTO.AZTECAN) return(1560)
  if (family == PAMA.NYUNGAN) return(18438)

  stop(paste0("get_n_sites called for unrecognised family '", family, "'"))
}

get_n_concepts <- function(family) {
  if (family == INDO.EUROPEAN) return(170)
  if (family == DRAVIDIAN) return(100)
  if (family == URALIC) return(101)
  if (family == SINO.TIBETAN) return(180)
  if (family == UTO.AZTECAN) return(121)
  if (family == PAMA.NYUNGAN) return(200)

  stop(paste0("get_n_concepts called for unrecognised family '", family, "'"))
}
