var CLASSES = [
    [String.fromCharCode(0),String.fromCharCode(1),String.fromCharCode(2),String.fromCharCode(3),String.fromCharCode(4),String.fromCharCode(5),String.fromCharCode(6),String.fromCharCode(7),String.fromCharCode(8),String.fromCharCode(10),String.fromCharCode(11),String.fromCharCode(13),String.fromCharCode(14),String.fromCharCode(15),String.fromCharCode(16),String.fromCharCode(17),String.fromCharCode(18),String.fromCharCode(19),String.fromCharCode(20),String.fromCharCode(21),String.fromCharCode(22),String.fromCharCode(23),String.fromCharCode(24),String.fromCharCode(25),String.fromCharCode(26),String.fromCharCode(27)],
    [String.fromCharCode(32),String.fromCharCode(9),String.fromCharCode(12),String.fromCharCode(28),String.fromCharCode(29),String.fromCharCode(30),String.fromCharCode(31),String.fromCharCode(133),String.fromCharCode(160),String.fromCharCode(5760),String.fromCharCode(6158),String.fromCharCode(8192),String.fromCharCode(8193),String.fromCharCode(8194),String.fromCharCode(8195),String.fromCharCode(8196),String.fromCharCode(8197),String.fromCharCode(8198),String.fromCharCode(8199),String.fromCharCode(8200),String.fromCharCode(8201),String.fromCharCode(8202),String.fromCharCode(8232),String.fromCharCode(8233),String.fromCharCode(8239),String.fromCharCode(8287),String.fromCharCode(12288)],
    ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'],
    ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'],
    ['0','1','2','3','4','5','6','7','8','9'],
    [String.fromCharCode(3)],
    [String.fromCharCode(33),String.fromCharCode(34),String.fromCharCode(35),String.fromCharCode(36),String.fromCharCode(37),String.fromCharCode(38),String.fromCharCode(39),String.fromCharCode(40),String.fromCharCode(41),String.fromCharCode(42),String.fromCharCode(43),String.fromCharCode(44),String.fromCharCode(45),String.fromCharCode(46),String.fromCharCode(47),String.fromCharCode(58),String.fromCharCode(59),String.fromCharCode(60),String.fromCharCode(61),String.fromCharCode(62),String.fromCharCode(63),String.fromCharCode(64)],
    [String.fromCharCode(91),String.fromCharCode(92),String.fromCharCode(93),String.fromCharCode(94),String.fromCharCode(95),String.fromCharCode(96)],
    [String.fromCharCode(123),String.fromCharCode(124),String.fromCharCode(125),String.fromCharCode(126),String.fromCharCode(127)],
    [String.fromCharCode(166),String.fromCharCode(174),String.fromCharCode(177),String.fromCharCode(182),String.fromCharCode(184),String.fromCharCode(186),String.fromCharCode(192),String.fromCharCode(194),String.fromCharCode(195),String.fromCharCode(197),String.fromCharCode(201),String.fromCharCode(202),String.fromCharCode(203),String.fromCharCode(204),String.fromCharCode(205),String.fromCharCode(206),String.fromCharCode(207),String.fromCharCode(208),String.fromCharCode(209),String.fromCharCode(210),String.fromCharCode(211),String.fromCharCode(214),String.fromCharCode(215),String.fromCharCode(224),String.fromCharCode(225),String.fromCharCode(226),String.fromCharCode(227),String.fromCharCode(228),String.fromCharCode(229),String.fromCharCode(230),String.fromCharCode(231),String.fromCharCode(232),String.fromCharCode(233),String.fromCharCode(234),String.fromCharCode(235),String.fromCharCode(236),String.fromCharCode(237),String.fromCharCode(238),String.fromCharCode(239),String.fromCharCode(240),String.fromCharCode(241),String.fromCharCode(242),String.fromCharCode(243),String.fromCharCode(244),String.fromCharCode(245),String.fromCharCode(246),String.fromCharCode(248),String.fromCharCode(249),String.fromCharCode(251),String.fromCharCode(252),String.fromCharCode(253),String.fromCharCode(254),String.fromCharCode(255)],
    [String.fromCharCode(382)],
    [String.fromCharCode(8226)]
];

var CLASS_CHARACTERS = {'2 4':[ 317978512,628133181],'4':[ 97877839,310154669],'2':[ 97771865,212276830],'2 3 4':[ 55401000,114504965],'3 4':[ 27184903,59103965],'2 3':[ 16389699,31919062],'3':[ 10622042,15529363],'2 6':[ 1575028,4907321],'2 4 6':[ 1482417,3332293],'4 6':[ 533489,1849876],'2 3 4 6':[ 286536,1316387],'2 7':[ 263533,1029851],'2 4 7':[ 256601,766318],'2 3 6':[ 153473,509717],'3 6':[ 63740,356244],'4 7':[ 60629,292504],'3 4 6':[ 44749,231875],'2 3 4 7':[ 39017,187126],'2 3 7':[ 31370,148109],'6':[ 30809,116739],'1 2 4':[ 18669,85930],'1 2':[ 14000,67261],'3 7':[ 9494,53261],'1 4':[ 7812,43767],'3 4 7':[ 6980,35955],'6 7':[ 5677,28975],'4 6 7':[ 4020,23298],'1 2 3':[ 3339,19278],'7':[ 2683,15939],'2 6 7':[ 2575,13256],'1 2 3 4':[ 1936,10681],'1 3':[ 1645,8745],'9':[ 1258,7100],'2 4 6 7':[ 973,5842],'4 8':[ 893,4869],'6 8':[ 437,3976],'8':[ 434,3539],'2 8':[ 376,3105],'2 9':[ 361,2729],'1 3 4':[ 283,2368],'1 6':[ 277,2085],'2 3 4 6 7':[ 252,1808],'3 6 7':[ 238,1556],'6 7 8':[ 233,1318],'3 8':[ 155,1085],'2 4 8':[ 140,930],'1 4 6':[ 138,790],'4 6 8':[ 131,652],'2 3 6 7':[ 86,521],'2 3 4 8':[ 78,435],'4 9':[ 68,357],'2 3 8':[ 42,289],'3 4 6 7':[ 36,247],'1':[ 25,211],'2 6 8':[ 25,186],'2 3 9':[ 23,161],'7 8':[ 22,138],'1 2 6':[ 22,116],'1 4 7':[ 19,94],'2 3 7 8':[ 14,75],'11':[ 10,61],'0':[ 7,51],'2 4 6 8':[ 7,44],'3 4 8':[ 7,37],'1 2 7':[ 7,30],'1 2 4 6':[ 6,23],'10 2':[ 5,17],'6 9':[ 3,12],'2 4 6 7 8':[ 3,9],'2 3 4 6 7 8':[ 3,6],'1 2 3 6':[ 2,3],'2 4 9':[ 1,1]};
var CLASS_CHARACTERS_SUM = 628133181;

var result = {};

/**
 * 
 * @param {string} password 
 */
function character_class(password) {
    var classes = [];

    for (var i = 0; i < password.length; i++) {
        // Push index in which class we found the char
        classes.push(CLASSES.findIndex(function(class_row) {
            return class_row.includes(password[i]);
        }));
    }

    // Filter out undefined from classes
    var found_classes = classes.filter(function(index) {
        return index > -1;
    });

    // Make the list unique
    found_classes = [... new Set(found_classes)];

    // Sort classes and create string from them
    found_classes = found_classes.sort();


    var classes_str = found_classes.join(' ');
    var res = CLASS_CHARACTERS[classes_str];

    result['character_class_analysis'] = {};

    if (res !== undefined) {
        result['result'] += (((res[1] * 1.0 / CLASS_CHARACTERS_SUM) * classes.length) / password.length);
        result['character_class_analysis'][classes_str] = res[0];
    }
}

/**
 * 
 * @param {string} password 
 */
function character_class_analysis(password) {
    result = { result: 0.0};

    character_class(password);

    return result;
}

function get_char_classes() {
    return CLASSES;
}

export { character_class_analysis, get_char_classes };    // DONE