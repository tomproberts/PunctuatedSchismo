source("scripts/families/LanguageFamilies.R")
source("scripts/glm/GLMUtils.R")

# Gradual Indo-European
fit.glm(
  family = INDO.EUROPEAN,
  relaxed = TRUE,
  formula = formula(
    rate ~ n_loans + log(area) + log(area_sister)
  ),
  output = "data/glm/glm-ie-area-noloans.RData"
)

# Punctuated Indo-European
fit.glm(
  family = INDO.EUROPEAN,
  punctuated = TRUE,
  formula = formula(
    burst ~ n_loans
  ),
  output = "data/glm/glm-iepunc-loans.RData"
)

# Gradual Pama-Nyungan
fit.glm(
  family = PAMA.NYUNGAN,
  relaxed = TRUE,
  formula = formula(
    rate ~ n_loans + log(water_availability) + log(water_availability_sister)
  ),
  output = "data/glm/glm-pn-water.RData"
)

# Punctuated Pama-Nyungan
