_CLASSES = (
    (chr(0),chr(1),chr(2),chr(3),chr(4),chr(5),chr(6),chr(7),chr(8),chr(10),chr(11),chr(10),chr(14),chr(15),chr(16),chr(17),chr(18),chr(19),chr(20),chr(21),chr(22),chr(23),chr(24),chr(25),chr(26),chr(27)),
    (chr(9),chr(12),chr(28),chr(29),chr(30),chr(31),chr(32),chr(133),chr(160),chr(5760),chr(6158),chr(8192),chr(8193),chr(8194),chr(8195),chr(8196),chr(8197),chr(8198),chr(8199),chr(8200),chr(8201),chr(8202),chr(8232),chr(8233),chr(8239),chr(8287),chr(12288)),
    ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'),
    ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'),
    ('0','1','2','3','4','5','6','7','8','9'),
    (chr(3)),
    (chr(33),chr(34),chr(35),chr(36),chr(37),chr(38),chr(39),chr(40),chr(41),chr(42),chr(43),chr(44),chr(45),chr(46),chr(47),chr(58),chr(59),chr(60),chr(61),chr(62),chr(63),chr(64)),
    (chr(91),chr(92),chr(93),chr(94),chr(95),chr(96)),
    (chr(123),chr(124),chr(125),chr(126),chr(127)),
    (chr(166),chr(174),chr(177),chr(182),chr(184),chr(186),chr(192),chr(194),chr(195),chr(197),chr(201),chr(202),chr(203),chr(204),chr(205),chr(206),chr(207),chr(208),chr(209),chr(210),chr(211),chr(214),chr(215),chr(224),chr(225),chr(226),chr(227),chr(228),chr(229),chr(230),chr(231),chr(232),chr(233),chr(234),chr(235),chr(236),chr(237),chr(238),chr(239),chr(240),chr(241),chr(242),chr(243),chr(244),chr(245),chr(246),chr(248),chr(249),chr(251),chr(252),chr(253),chr(254),chr(255)),
    (chr(382)),
    (chr(8226))
)

_CLASSES_CHARACTERS = {'2 4':( 317978512,628133181),'4':( 97877839,310154669),'2':( 97771865,212276830),'2 3 4':( 55401000,114504965),'3 4':( 27184903,59103965),'2 3':( 16389699,31919062),'3':( 10622042,15529363),'2 6':( 1575028,4907321),'2 4 6':( 1482417,3332293),'4 6':( 533489,1849876),'2 3 4 6':( 286536,1316387),'2 7':( 263533,1029851),'2 4 7':( 256601,766318),'2 3 6':( 153473,509717),'3 6':( 63740,356244),'4 7':( 60629,292504),'3 4 6':( 44749,231875),'2 3 4 7':( 39017,187126),'2 3 7':( 31370,148109),'6':( 30809,116739),'1 2 4':( 18669,85930),'1 2':( 14000,67261),'3 7':( 9494,53261),'1 4':( 7812,43767),'3 4 7':( 6980,35955),'6 7':( 5677,28975),'4 6 7':( 4020,23298),'1 2 3':( 3339,19278),'7':( 2683,15939),'2 6 7':( 2575,13256),'1 2 3 4':( 1936,10681),'1 3':( 1645,8745),'9':( 1258,7100),'2 4 6 7':( 973,5842),'4 8':( 893,4869),'6 8':( 437,3976),'8':( 434,3539),'2 8':( 376,3105),'2 9':( 361,2729),'1 3 4':( 283,2368),'1 6':( 277,2085),'2 3 4 6 7':( 252,1808),'3 6 7':( 238,1556),'6 7 8':( 233,1318),'3 8':( 155,1085),'2 4 8':( 140,930),'1 4 6':( 138,790),'4 6 8':( 131,652),'2 3 6 7':( 86,521),'2 3 4 8':( 78,435),'4 9':( 68,357),'2 3 8':( 42,289),'3 4 6 7':( 36,247),'1':( 25,211),'2 6 8':( 25,186),'2 3 9':( 23,161),'7 8':( 22,138),'1 2 6':( 22,116),'1 4 7':( 19,94),'2 3 7 8':( 14,75),'11':( 10,61),'0':( 7,51),'2 4 6 8':( 7,44),'3 4 8':( 7,37),'1 2 7':( 7,30),'1 2 4 6':( 6,23),'10 2':( 5,17),'6 9':( 3,12),'2 4 6 7 8':( 3,9),'2 3 4 6 7 8':( 3,6),'1 2 3 6':( 2,3),'2 4 9':( 1,1),}
_CLASSES_CHARACTERS_SUM = 628133181


def _character_class(password: str) -> dict:
    # Get all classes the characters belong to
    classes = [i for char in password for i, _CLASS in enumerate(_CLASSES) if char in _CLASS]
    classes_count = len(classes)            # Get number of classes found
    classes = list(set(classes))            # Convert them to unique list
    classes.sort()                          # Sort them by INT
    classes = [str(i) for i in classes]     # Convert to String
    classes_str = ' '.join(classes)         # Join to form a class string

    # Search for class string, when found return calculated value
    if classes_str in _CLASSES_CHARACTERS:
        res = _CLASSES_CHARACTERS[classes_str]
        return {
            'character_class_analysis': {classes_str: res[0]},
            'result': (((res[1] / _CLASSES_CHARACTERS_SUM) * classes_count) / len(password))
        }

    # Return empty value
    return {'character_class_analysis': {}, 'result': 0.0}


def char_class_analysis(password: str) -> dict:
    return _character_class(password)
