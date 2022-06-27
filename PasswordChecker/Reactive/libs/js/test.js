var checker = require('./reactive-password-checker/checker');
var bcrypt = require('bcrypt');

// Start debug mode
checker.DEBUG = true;

// Load password hashes from DB or anywhere else
hashed_passwords = [
'$2b$10$es429p6UqbLEw2PHDLk18e5jfR7M7zt.WivEiQ/uRJBFmjIVpDLtO', // 123456
'$2b$10$Eoip1fpBoijITpLzW1cRmOj.sWLsmLrfS5q3wGDYOgnyufOCT6b1i', // asdasd
'$2b$10$LAo4T24brW3ubTdOckxfa.gzK6qh0EoTH5ntos2y3ff2MzGkLdpDW', // 123456789
'$2b$10$QyG0W6FVOjMAUcKyGPq/g.rY.G/FJOzIigzg1goMLWh.3EYAM0ZDu', // 000000
'$2b$10$MUhpgCPLTd4qMTApGhDxMeDqoqIsWsRwy7GOBZ3DTq2nGZr/OUM4S', // qwerty
'$2b$10$4TdaepANTbR61N4hUd5wveuiZ7g1S0uw8vHtUjJH9Om8XBlZUs2MS', // 123456
'$2b$10$K7SZw2Piv3W66ZyXxxL.WufURI8gHqM3Eb1N6aW9/UKIyDMvfWBnq', // asdasd
'$2b$10$EUbjCI6UCBygCJ1dJu28eeGQTah1HX1yHf24XgUs1v93WtraM5leW', // 123456789
'$2b$10$oN7eSDc7wDAtakZuM/6up.jM4dx6yrkTtJNnhHx7IjWE/dEFmaQf6', // 000000
'$2b$10$2GREki7n7yzkdpWlQiSwhurn1NxIEhQPE0jogS8zhS8zaQOSZT1nm', // qwerty
'$2b$10$/HwKFnVLd6rFGv8JTrFSbeo.k0tSYMKzeydyy4OmylyZk6JCU746C'  // 7777777
];

// Load hashes
checker.load_passwords(hashed_passwords);

// When we want to start again, uncomment this part
//checker.clear_old_session();

// Custom verify function
function verify(password, hash) {
    return bcrypt.compareSync(password, hash);
}

(async function() {
    while (true) {
        try {
            // Get weak hashes with names of datasets the hash has been found in
            // and the number of times it has been found in those datasets
            result = await checker.check_next(verify);

            // Ending
            if (result === true) {
                break;
            }

            // Weak hashes found, notify user about the weak hash
            console.log(result);
        } catch (error) {
            console.log(error);
            break;
        }
    }
})();