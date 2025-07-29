# Polygons

## Intro

One of our main hypotheses in this paper is that the greater the level of contact between two groups at a split, the
greater need they have for social signalling (to differentiate group membership).
We would expect, then, that these groups would innovate their speech (e.g. lexicon) to exaggerate group distinctions -
that is, they would undergo schismogenesis.

We use geographic distance (ideally topographic, but initially geodesic) between speakers as a proxy for language
contact.
We want a metric that reflects the unequal level of contact experienced by speakers in each group, since all speakers of
a small subgroup that broke off from the larger one should have (on average) more contact with the speakers of the large
one, whereas the average speaker from the larger group may not have much contact with the speakers of the small group (
at the periphery).

Polygons are a better representation of where speakers of a language are, when compared to point estimates, since
populations are rarely confined to one geographic point and are instead spread out.
They allow us to compute these asymmetric distances, since we can take (e.g. 1000) random speakers from one region and
calculate their distance from another group/area (e.g. shortest walking distance).

## Guidelines

The polygons we use should be as close to the areas where the languages/subgroups were immediately after the split,
since their modern day locations are not necessarily representative of intergroup dynamics at the split event (this is
particularly the case in a colonial context).
In the case of settlement, e.g. as was the case for Faroese, the polygons for each group should exclude each other (
which may not be the case for the rough area of Old Norse).

Where possible, we use already available polygons from _Glottography_, which includes sets of polygons from different
sources.
However, a particular language (e.g. Neapolitan) may not be already available to us, in which case we have to find the
maps and digitise the polygons ourselves.
This may also be the case where the polygon for a particular language may be available to us, but from the wrong time
period (e.g Modern English).

## Data Availability

| family         | lexical data                                                                          | polygons                           |
|----------------|---------------------------------------------------------------------------------------|------------------------------------|
| `IndoEuropean` | [IE-CoR](https://iecor.clld.org/languages)                                            | 18/44 cherries in `glottography`   |
| `Dravidian`    | [DravLex](https://github.com/phlorest/kolipakam_et_al2018)                            | 5/5 cherries available             |
| `Uralic`       | [UraLex](https://github.com/lexibank/uralex)                                          | 8/8 cherries in `rantanen2022urhia`|
| `UtoAztecan`   | [Greenhill et al. 2023](https://github.com/lexibank/utoaztecan)                       | 8/12 cherries in `glottography`    |
| `SinoTibetan`  | [Sino-Tibetan Database of Lexical Cognates](https://github.com/lexibank/sagartst)     | 6/15 cherries in `asher2007world`  |
| `Philippines`  | [Austronesian Basic Vocabulary Database](https://github.com/lexibank/abvdphilippines) | 4/66 cherries in `glottography`    |
| `PamaNyungan`  | [Chirila](https://github.com/phlorest/bouckaert_et_al2018)                            | all/most polygons available        |

### [*IndoEuropean*](./data/glottography/PolygonsIndoEuropean.md) (160 taxa, 18/44 cherries)

### *Dravidian* (20 taxa, 5/5 cherries)

### [*Uralic*](./data/glottography/PolygonsUralic.md) (26 taxa, 8/8 cherries)

### [*UtoAztecan*](./data/glottography/PolygonsUtoAztecan.md) (35 taxa, 8/12 cherries)

### [*SinoTibetan*](./data/glottography/PolygonsSinoTibetan.md) (50 taxa, 6/15 cherries)

### [*Philippines*](./data/glottography/PolygonsPhilippines.md) (202 taxa, 4/66 cherries)

### *Pama-Nyungan* (306 taxa)

Summary:

- 178 out of 306 trivially found
- god knows how many others are there just poorly linked

