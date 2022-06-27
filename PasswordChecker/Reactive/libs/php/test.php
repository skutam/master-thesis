<?php 

include_once __DIR__ . '/skutam/reactive-password-checker/src/PasswordChecker/checker.php';


function custom_callback(string $password, string $hash): bool {
    return password_verify($password, $hash);
}

$weak_hashes = [
    '$2y$10$LZoeB96.qw/z1/3x/N05deUTie0TV2Ud5rBJ4KBA9OsTRrwFbtQPW', // 123456
    '$2y$10$aQm0SXhKtO0pgemCSeiGDugzqzb7zVwradYPVKdBsMkHPtu8IgQjm', // asdasd
    '$2y$10$.lvcWGzrrr08sKL1ZA6GFudmQS7lK.0MVqMyQyfzvurVYhazEIX2O', // 123456789
    '$2y$10$C8RDsar3rH9Yzkin3g7XwexT1k4/tFvFvqNcfnYYyfx0vv0tnROQm', // 000000
    '$2y$10$VXE3BwMxjCGfHNyonuJRbOHtrdhNFRxVyxV4X0Bl6kZee/.LIt9FW', // qwerty
    '$2y$10$USE4Jv.m5n5j6/aBbdTkceUbg2DCH8gxYT6Jf2ooTkqrwVMV0Dzky', // 123456
    '$2y$10$6MgmnLZNez9qOYlAYwZqmu.M6g9h89iOx5wTz4gRJrKhgVssRw18G', // asdasd
    '$2y$10$nTtD26Gynt1wxohOq8tmteBJaZcX8lpcn/63MsVAQxNLpbVb.GNYq', // 123456789
    '$2y$10$5a2gLsSK9Qg.g9TnE7Dn5.Wkpaq.Vw0qS25VYGh8g2k8jXUTBsj3S', // 000000
    '$2y$10$semNVW3o8YhgC3XNDYzaMeM3FabndBgJfNNdaN/WkaaVcA9kTgnjW', // 7777777
];

// Instantiate class
$password_checker = new PasswordChecker\Checker(true);

// When we want to start again, uncomment this part
// $password_checker->clear_old_session(true);

$password_checker->load_passwords($weak_hashes);

// Start searching for passwords
while (true) {
    // Functin will load 100000 weak passwords and check the hashes against them
    $weak_hashes = $password_checker->check_next('custom_callback');

    // No more passwords to check or no more weak passwords, ending
    if ($weak_hashes === true) {
        echo "Finished";
        break;
    }

    var_dump($weak_hashes);
}