<?php

namespace ProactivePasswordChecker;

include_once(__DIR__ . '/Analyses/CharClassAnalysis.php');
include_once(__DIR__ . '/Analyses/SequenceAnalysis.php');
include_once(__DIR__ . '/Analyses/SimpleAnalysis.php');
include_once(__DIR__ . '/Analyses/SubstringAnalysis.php');
include_once(__DIR__ . '/Analyses/WordUseAnalysis.php');

function validate_password(string $password) {
    if (mb_strlen($password) <= 2) {
        return array('result' => 1.0);
    }

    $result = array(
        'simple_analysis' => simple_analysis($password),
        'char_class_analysis' => char_class_analysis($password),
        'sequence_analysis' => sequence_analysis($password),
        'substring_analysis' => substring_analysis($password),
        'word_use_analysis' => word_use_analysis($password)
    );

    $result['result'] = (
        $result['simple_analysis']['result'] +
        $result['char_class_analysis']['result'] +
        $result['sequence_analysis']['result'] +
        $result['substring_analysis']['result'] +
        $result['word_use_analysis']['result']
    ) / 5.0;
    return $result;
}

?>