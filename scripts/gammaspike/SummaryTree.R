library(treeio)
source("scripts/families/LanguageFamilies.R")

get_summary_cherries <- function(family) {
  summary.tree <- paste0("data/gammaspike/summarytree/", family, ".nex")
  df <- as_tibble(read.beast(summary.tree))
  df <- df[!is.na(df$label),]
  parents <- df$parent
  cherries <- parents[duplicated(parents)]
  df <- df[df$parent %in% cherries,]
  df <- df[order(df$parent),]

  cherries <- list()
  l1 <- ""
  i <- 1
  for (l in df$label) {
    if (l1 == "") { l1 <- l }
    else {
      # TODO: potentially order by spike size
      cherries[[i]] <- c(l1, l)
      l1 <- ""
      i <- i + 1
    }
  }

  return(cherries)
}

get_manual_cherries <- function(family) {
  if (family == INDO.EUROPEAN) return(list(
    # c("French", "FrancoProvencal"),
    # c("OldFrench", "AngloNorman"),
    # c("Ladin", "Friulian"),
    # c("Italian", "Neapolitan"),
    # c("SardinianNuoro", "SardinianLogudoro"),
    # c("Romanian", "MeglenoRomanian"),
    # c("Umbrian", "Oscan")
    c("KurdishSQorveh", "KurdishSElami"),
    c("KurdishCJafi", "KurdishNBahdini"),
    c("Tati", "Hawrami"),
    c("RajiBarzoki", "Mazanderani"),
    c("Yaghnobi", "Sogdian"),
    c("OsseticIron", "OsseticDigor"),
    c("Lari", "Delvari"),
    c("Bakhtiari", "Kumzari"),
    c("Wakhi", "Khotanese"),
    c("Magahi", "Bhojpuri"),
    c("Hindi", "Urdu"),
    c("Bengali", "Assamese"),
    c("Palula", "Gawri"),
    c("PashaiNorthWest", "Khowar"),
    c("KatavariKtivi", "KatavariEastern"),
    c("SanuviriWama", "KalasalaNiseigram")
  ))
  if (family == DOUGLAS) return(list(
    # c("French", "FrancoProvencal"),
    # c("Ladin", "Friulian"),
    # c("Italian", "Milanese"),
    # c("SardinianNuoro", "SardinianLogudoro"),
    # c("Romanian", "MeglenoRomanian"),
    # c("Umbrian", "Oscan")
    # c("SorbianUpper", "SorbianLower"),
    # c("Polish", "Kashubian"),
    # c("Slovak", "Czech"),
    # c("Ukrainian", "Belarusian"),
    # c("MacedonianVisoka", "MacedonianSuho"),
    # c("SloveneKostel", "Slovene"),
    # c("Latvian", "Latgalian")
    c("Lari", "Delvari"),
    c("Tati", "Mazanderani"),
    c("KurdishSQorveh", "KurdishSElami"),
    c("KurdishCJafi", "Hawrami"),
    c("Yaghnobi", "Sogdian"),
    c("Wakhi", "Sarikoli"),
    c("OsseticIron", "OsseticDigor"),
    c("KatavariKtivi", "KatavariEastern"),
    c("PashaiNorthWest", "Khowar"),
    c("Palula", "Gawri"),
    c("Hindi", "Urdu"),
    c("Bengali", "Assamese")
  ))
}
