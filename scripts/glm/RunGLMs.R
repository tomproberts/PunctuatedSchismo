source("scripts/families/LanguageFamilies.R")
source("scripts/glm/GLMUtils.R")

# Gradual Indo-European
fit.glm(
  family = INDO.EUROPEAN,
  relaxed = TRUE,
  formula = formula(
    rate ~ n_loans + log(area) + log(area_sister)
  ),
  output = "data/glm/IndoEuropeanRelaxed.RData"
)

# Punctuated Indo-European
fit.glm(
  family = INDO.EUROPEAN,
  punctuated = TRUE,
  formula = formula(
    burst ~ n_loans + log(area) + log(area_sister)
  ),
  output = "data/glm/IndoEuropean.RData"
)

# Gradual Pama-Nyungan

# Punctuated Pama-Nyungan