# Roadmap
Here is the list of tasks that I need to be working on, along with rough dates for how long I think they will take. (I can work on multiple tasks concurrently)

## Tasks
- [x] Probably set up dedicated github repo, since we have to open-source everything at the end **(14. Feb)**
- [x] Understand phylogenetics to correct tree heights, and to fully understand the beast configs from Douglas **(26. Feb)**
- [x] Learn how to convert all the datasets to presence/absence matrices (technically not necessary if I take the data from the configs of the cited papers) **(28. Feb)**
- [x] Make extracting Glottolog trees more robust **(10. Mar)**
- [ ] Fit trees on new families (clades?) **(21. Mar)**
  - [ ] Austronesian
  - [ ] Pama-Nyungan
  - [ ] Uto-Aztecan
  - [ ] Dravidian
- [ ] Learn how to fit GLMs in STAN or brms **(15. Mar)**
- [ ] Collect and calculate predictors (probably most time consuming part):
	- [ ] Spatial distances → will likely take to write the code to calculate, but once we obtain the polygons it shouldn't be too hard to run all languages for each family. **(11. Apr)**
	- [ ] Historical population data → population size, and spread/density (calculate from polygon area)? **(18. Apr)**
	- [x] Literature culture/prestige → number of literature pages on glottolog for each doculect
	- [ ] Prestige → binary “official/administrative language of a political entity”, “language of religious rite”, “presence/absence of translation of key religious work or when date” or “language of juridical codification” **(2. May)**
	- [ ] Phonological distances → levenshtein is easy, PMI slightly more complicated (calculate for each language family?), both need alignment so we have to do automatic alignment. **(16. May)**
- [ ] Fit the GLMs for each family **(6. Jun)**
- [ ] Writing paper **(30. Aug)**
	- [ ] Introduction, background and methods (similar to what's already in the proposal)
	- [ ] Results and discussion → interpretation of GLM parameter weights, think about *estimands*, do we also discuss non-constrained tree topologies? 
	- [ ] Provide full clade posteriors for diagrams (in supplementary materials)
- [ ] Investigate genetic similarity (Gelato has glottocodes, so wherever we have the requisite data we can do an easy analysis) **(12. Sep)**

