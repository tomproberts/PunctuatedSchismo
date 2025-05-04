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
since their modern day locations are not necessarily representative of inter-group dynamics at the split event (this is
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

| family         | lexical data                                                                      | polygons                            |
|----------------|-----------------------------------------------------------------------------------|-------------------------------------|
| `IndoEuropean` | [IE-CoR](https://iecor.clld.org/languages)                                        | \~ some in `glottography`           |
| `Dravidian`    | [DravLex](https://github.com/phlorest/kolipakam_et_al2018)                        | \~ ✓(map available in paper)        |
| `PamaNyungan`  | [Chirila](https://github.com/phlorest/bouckaert_et_al2018)                        | ✓ (all? polygons available)         |
| `Uralic`       | [UraLex](https://github.com/lexibank/uralex)                                      | ✓ (4 missing from `glottography`)   |
| `UtoAztecan`   | [Greenhill et al. 2023](https://github.com/lexibank/utoaztecan)                   | ? ✓ (most in `glottography:world`?) |
| `SinoTibetan`  | [Sino-Tibetan Database of Lexical Cognates](https://github.com/lexibank/sagartst) | \~ (maybe in `glottography:world`?) |
| `Austronesian` | ? maybe need permission from Simon Greenhill                                      | ?                                   |

### Indo-European

23 broken cherries (only one polygon out of two):

- †cherry, because Hawrami ([hawr1243](https://glottolog.org/resource/languoid/id/hawr1243)) missing
- †cherry, because Latgalian ([east2282](https://glottolog.org/resource/languoid/id/east2282)) missing
- †cherry, because Old Catalan ([oldc1251](https://glottolog.org/resource/languoid/id/oldc1251)) missing
- †cherry, because Rusyn ([rusy1239](https://glottolog.org/resource/languoid/id/rusy1239)) missing
- †cherry, because Kurdish C.: Jafi ([cent1972](https://glottolog.org/resource/languoid/id/cent1972)) missing
- †cherry, because Luvian ([cune1239](https://glottolog.org/resource/languoid/id/cune1239)) missing
- †cherry, because Greek: Cypriot ([cypr1249](https://glottolog.org/resource/languoid/id/cypr1249)) missing
- †cherry, because Old Spanish ([olds1249](https://glottolog.org/resource/languoid/id/olds1249)) missing
- †cherry, because Megleno-Romanian ([megl1237](https://glottolog.org/resource/languoid/id/megl1237)) missing
- †cherry, because Pashai: North-West ([nort2665](https://glottolog.org/resource/languoid/id/nort2665)) missing
- †cherry, because Old Welsh ([oldw1241](https://glottolog.org/resource/languoid/id/oldw1241)) missing
- †cherry, because Franco-Provençal ([fran1269](https://glottolog.org/resource/languoid/id/fran1269)) missing
- †cherry, because Palula ([ashr1238](https://glottolog.org/resource/languoid/id/ashr1238)) missing
- †cherry, because Raji: Barzoki ([cent2264](https://glottolog.org/resource/languoid/id/cent2264)) missing
- †cherry, because Sorbian: Lower ([lowe1385](https://glottolog.org/resource/languoid/id/lowe1385)) missing
- †cherry, because German: Bernese ([swis1247](https://glottolog.org/resource/languoid/id/swis1247)) missing
- †cherry, because Khotanese ([khot1251](https://glottolog.org/resource/languoid/id/khot1251)) missing
- †cherry, because Lari ([lari1253](https://glottolog.org/resource/languoid/id/lari1253)) missing
- †cherry, because Slovene: Kostel ([lowe1384](https://glottolog.org/resource/languoid/id/lowe1384)) missing
- †cherry, because Old Polish ([oldp1256](https://glottolog.org/resource/languoid/id/oldp1256)) missing
- †cherry, because Neapolitan ([neap1235](https://glottolog.org/resource/languoid/id/neap1235)) missing
- †cherry, because Kalaṣa-alâ: Nišeigrâm ([chim1297](https://glottolog.org/resource/languoid/id/chim1297)) missing
- †cherry, because Armenian: Western ([homs1234](https://glottolog.org/resource/languoid/id/homs1234)) missing

7 dead cherries (neither polygon present):

- †cherry, because both Greek: Cappadocian ([capp1239](https://glottolog.org/resource/languoid/id/capp1239)) and Greek:
  Pontic ([pont1253](https://glottolog.org/resource/languoid/id/pont1253)) missing
- †cherry, because both Breton: Gwened ([vann1244](https://glottolog.org/resource/languoid/id/vann1244)) and Breton:
  Treger ([treg1244](https://glottolog.org/resource/languoid/id/treg1244)) missing
- †cherry, because both Norwegian: Bokmål ([norw1259](https://glottolog.org/resource/languoid/id/norw1259)) and
  Norwegian: Nynorsk ([norw1262](https://glottolog.org/resource/languoid/id/norw1262)) missing
- †cherry, because both Macedonian: Suho ([sout3278](https://glottolog.org/resource/languoid/id/sout3278)) and
  Macedonian: Visoka ([sout3277](https://glottolog.org/resource/languoid/id/sout3277)) missing
- †cherry, because both Kâta-vari: Eastern ([east2308](https://glottolog.org/resource/languoid/id/east2308)) and
  Kâta-vari: Ktivi ([west2372](https://glottolog.org/resource/languoid/id/west2372)) missing
- †cherry, because both Kurdish S.: Elami ([feyl1238](https://glottolog.org/resource/languoid/id/feyl1238)) and Kurdish
  S.: Qorveh ([koly1245](https://glottolog.org/resource/languoid/id/koly1245)) missing
- †cherry, because both Sogdian ([sogd1245](https://glottolog.org/resource/languoid/id/sogd1245)) and
  Yaghnobi ([yagn1238](https://glottolog.org/resource/languoid/id/yagn1238)) missing

### Dravidian

3 broken cherries (only one polygon out of two):

- †cherry, because Malto ([saur1249](https://glottolog.org/resource/languoid/id/saur1249)) missing
- †cherry, because Betta_Kurumba ([bett1235](https://glottolog.org/resource/languoid/id/bett1235)) missing
- †cherry, because Yeruva ([ravu1237](https://glottolog.org/resource/languoid/id/ravu1237)) missing

2 dead cherries (neither polygon present):

- †cherry, because both Gondi ([nort2702](https://glottolog.org/resource/languoid/id/nort2702)) and
  Koya ([koya1251](https://glottolog.org/resource/languoid/id/koya1251)) missing
- †cherry, because both Ollari_Gadba ([pott1240](https://glottolog.org/resource/languoid/id/pott1240)) and
  Parji ([duru1236](https://glottolog.org/resource/languoid/id/duru1236)) missing

### Pama-Nyungan

### Uralic

### Uto-Aztecan

### Sino-Tibetan

