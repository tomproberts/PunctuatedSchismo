library(treeio)
source("../families/LanguageFamilies.R")

get_summary_cherries <- function(family) {
  summary.tree <- paste0("data/phylo/gammaspike/summary/", family, ".nex")
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
    # c("Dutch", "Flemish"),
    # c("German", "GermanBernese"),
    # c("NorwegianNynorsk", "NorwegianBokmal"),
    # c("Swedish", "Elfdalian"),
    # c("BretonTreger", "BretonGwened"),
    # c("GaelicScottish", "GaelicManx"),
    # c("Portuguese", "PortugueseBrazilian"),
    c("French", "FrancoProvencal"),
    c("SardinianNuoro", "SardinianLogudoro"),
    c("Latvian", "Latgalian"),
    c("Ukrainian", "Belarusian")
    # c("OldFrench", "AngloNorman"),
    # c("Italian", "Milanese"),
    # c("Ladin", "Friulian"),
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
    # c("Lari", "Delvari"),
    # c("Tati", "Mazanderani"),
    # c("KurdishSQorveh", "KurdishSElami"),
    # c("KurdishCJafi", "Hawrami"),
    # c("Yaghnobi", "Sogdian"),
    # c("Wakhi", "Sarikoli"),
    # c("OsseticIron", "OsseticDigor"),
    # c("KatavariKtivi", "KatavariEastern"),
    # c("PashaiNorthWest", "Khowar"),
    # c("Palula", "Gawri"),
    # c("Hindi", "Urdu"),
    # c("Bengali", "Assamese")
  ))
  if (family == PAMA.NYUNGAN) return(list(
    c("Thaynakwith", "Mbakwithi"),
    c("Walangama", "Ikarranggal"),
    c("UwOykangand", "Olkola"),
    c("KLY", "KKY"),
    c("Wulguru", "Coonambella"),
    c("Djambarrpuyngu", "Dhuwal"),
    c("Lardil", "Kayardild"),
    c("MathiMathi", "LakeHindmarsh"),
    c("WangkumaraMcDWur", "Wangkumara")
  ))
}
