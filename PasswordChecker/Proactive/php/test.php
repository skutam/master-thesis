<?php

// Include library
include_once __DIR__ . '/skutam/proactive-password-checker/src/checker.php';

// Define threshold
$threshold = 0.225;

// Run analysis and compute the similarity rate of password
$result = ProactivePasswordChecker\validate_password('password');

// Show the returned array of features
var_dump($result);

if ($result['result'] < $threshold) {
    echo 'Given password is strong.' . PHP_EOL;
} else {
    echo 'Given password is weak.' . PHP_EOL;
}

?>