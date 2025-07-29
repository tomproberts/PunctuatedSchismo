from scripts.predictors.polygons.glottography import GlottographyConfig

# Available glottography datasets
ASHER_2007_WORLD = 'asher2007world'
BOUCKAERT_2012_INDOEUROPEAN = 'bouckaert2012indoeuropean'
DEDIO_2019_BRITAIN = 'dedio2019britain'
RANTANEN_2022_URHIA = 'rantanen2022urhia'
NATIVELAND_2024_LANGUAGES = 'nativeland2024languages'
STEEVER_2019_DRAVIDIAN = 'steever2019dravidian'
GODDARD_1999_NATIVE = 'goddard1999native'
HAYNIE_2019_MODERN = 'haynie2019modern'


def get_config(family_name: str):
    if family_name == 'Italic' or family_name == 'IndoEuropean':
        return indoeuropean_config()
    if family_name == 'Dravidian':
        return dravidian_config()
    if family_name == 'Uralic':
        return uralic_config()
    if family_name == 'UtoAztecan':
        return uto_config()
    if family_name == 'SinoTibetan':
        return sinotibetan_config()
    if family_name == 'Bantu':
        return bantu_config()
    if family_name == 'Philippines':
        return philippines_config()
    raise RuntimeError(f'Glottography Error: unknown family {family_name}')


def indoeuropean_config():
    return GlottographyConfig(sources=[BOUCKAERT_2012_INDOEUROPEAN, DEDIO_2019_BRITAIN, ASHER_2007_WORLD],
                              patches={
                                  'sout2614': (0, 80),
                                  'barb1262': (0, 81),
                                  'czec1258': (0, 21),
                                  'nucl1235': (0, 19),
                                  'dutc1256': (0, 25),  # wrong glottocode
                                  'stan1293': (0, 26),  # Old_English has wrong glottocode
                                  'hind1269': (0, 37),
                                  'urdu1245': (0, 97),  # Urdu has wrong glottocode
                                  'iris1253': (0, 40),
                                  'oldi1245': (0, 63),
                                  'lith1251': (0, 49),  # Not sure what Lithuanian_ST is
                                  'swed1254': (0, 89),
                                  'braz1246': (0, 72),
                                  'tokh1242': (0, 93),
                                  'tokh1243': (0, 94),
                                  'iron1242': (0, 41),  # Iron_Ossetic has wrong glottocode
                                  'digo1242': (0, 24),  # Ossetic has wrong glottocode
                                  'oldp1254': (0, 65),  # Modern persian has wrong glottocode
                                  'west2369': (0, 70),  # No Tehran Persian available
                                  'alba1267': (0, 2),  # Standard Albanian
                                  'gheg1238': (0, 4),  # Kosovo
                                  'arbe1236': (0, 3),  # Sicilian Albanian
                                  'mode1248': (0, 35),  # Modern Greek has wrong glottocode
                                  'angl1258': (1, 32),
                                  'oldf1239': (1, 34),
                              })


def dravidian_config():
    return GlottographyConfig(sources=['ravula', STEEVER_2019_DRAVIDIAN, ASHER_2007_WORLD],
                              patches={})


def uto_config():
    return GlottographyConfig(sources=[ASHER_2007_WORLD, NATIVELAND_2024_LANGUAGES],
                              patches={
                                  'nort2954': (0, 4617),
                                  'pipi1250': (0, 5042)
                              })


def sinotibetan_config():
    return GlottographyConfig(sources=[ASHER_2007_WORLD],
                              patches={
                                  'zaiw1241': (0, 369),
                                  'byan1241': (0, 1004),
                                  'lash1243': (0, 3281),
                                  'lisu1250': (0, 3378),
                                  'maru1249': (0, 3749),
                              })


def uralic_config():
    return GlottographyConfig(sources=[RANTANEN_2022_URHIA],
                              patches={
                                  'sout2674': (0, 159),
                                  'umes1235': (0, 187),
                                  'pite1240': (0, 140),
                                  'nort2671': (0, 128),
                                  'inar1241': (0, 1),
                                  'kild1236': (0, 65),
                                  'finn1318': (0, 30),
                                  'kare1335': (0, 50),
                                  'veps1250': (0, 193),
                                  'ingr1248': (0, 44),
                                  'esto1258': (0, 120),
                                  'sout2679': (0, 156),
                                  'erzy1239': (0, 21),
                                  'east2328': (0, 19),
                                  'komi1268': (0, 83),
                                  'komi1269': (0, 72),
                                  'udmu1245': (0, 185),
                                  'hung1274': (0, 42),
                                  'ngan1291': (0, 117),
                                  'nene1249': (0, 179),
                                  'skol1241': (0, 151),  # in glottography as 'sklo1241'
                                  'west2391': (0, 198),  # mapped to parent Votic
                                  'west1760': (0, 90),  # mapped to parent Livonian
                                  'nort2677': (0, 124),  # mapped to parent Northern Mansi
                                  'tazz1244': (0, 146)  # mapped to parent Selkup
                              })


def bantu_config():
    return GlottographyConfig(sources=[ASHER_2007_WORLD])


def philippines_config():
    return GlottographyConfig(sources=[ASHER_2007_WORLD])
