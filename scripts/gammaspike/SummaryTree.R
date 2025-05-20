library(treeio)
source("scripts/families/LanguageFamilies.R")

get_summary_cherries <- function (family) {
  summary.tree <- paste0("data/gammaspike/summarytree/", family, ".nex")
  df <- as_tibble(read.beast(summary.tree))
  df <- df[!is.na(df$label),]
  parents <- df$parent
  cherries <- parents[duplicated(parents)]
  df <- df[df$parent %in% cherries,]
  df <- df[order(df$parent), ]

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

  return (cherries)
}

# print(get_summary_cherries(URALIC))
