source("scripts/families/LanguageFamilies.R")
source("scripts/glm/GLMUtils.R")

# Gradual Indo-European
fit.glm(
  family = INDO.EUROPEAN,
  relaxed = TRUE,
  formula = formula(
    rate ~ n_loans + log(water_availability) + log(water_availability_sister) + log(area) + log(area_sister)
  ),
  output = "data/glm/IndoEuropeanCombinedRelaxed.RData"
)

# Punctuated Indo-European
fit.glm(
  family = INDO.EUROPEAN,
  punctuated = TRUE,
  formula = formula(
    burst ~ n_loans + log(area) + log(area_sister)
  ),
  output = "data/glm/IndoEuropean.RData",
  thin = 1
)

# Gradual Pama-Nyungan
fit.glm(
  family = PAMA.NYUNGAN,
  relaxed = TRUE,
  formula = formula(
    rate ~ n_loans +
      log(area) +
      log(area_sister),
  ),
  output = "data/glm/PamaNyunganAreaRelaxed.RData"
)

# Punctuated Pama-Nyungan
