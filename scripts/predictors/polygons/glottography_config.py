from scripts.predictors.polygons.glottography import GlottographyConfig


def get_config(family_name: str):
    if family_name == 'Italic' or family_name == 'IndoEuropean':
        return indoeuropean_config()
    raise RuntimeError(f'Unknown family {family_name}')


def indoeuropean_config():
    return GlottographyConfig(sources=['bouckaert2012indoeuropean', 'dedio2019britain', 'asher2007world'],
                              patches={'sout2614': (0, 80),
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
