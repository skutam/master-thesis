# Test

Before running this script go into reactive password checker folder and install required libraries

## Installation

Reactive-password-checker requires [npm](https://www.npmjs.com/package/npm) 8.7.0+ to run. Run in this directory and in the `reactive-password-checker` this command to install libraries.

```bash
npm install
```

## Usage

```Javascript
var checker = require('./reactive-password-checker/checker');
var bcrypt = require('bcrypt');

// Turn on debuging mode, default is off
checker.DEBUG = true;

// Passwords for testing
passwords = [
    '123456',
    'asdasd',
    '123456789',
    '000000',
    'qwerty',
    '123456',
    'asdasd',
    '123456789',
    '000000',
    'qwerty',
    '7777777'
];

// Hash passwords using bcrypt
hashed_passwords = passwords.map(function(pass) {
    return bcrypt.hashSync(pass, 10);
});

// Load hashes
checker.load_passwords(hashed_passwords);

// Clear old checking session
checker.clear_old_session();

(async function() {
    while (true) {
        try {
            // Get weak hashes with names of datasets the hash has been found in
            // and the number of times it has been found in those datasets
            result = await checker.check_next();

            // Ending
            if (result === true) {
                break;
            }

            console.log(result);
        } catch (error) {
            console.log(error);
            break;
        }
    }
})();
```

We even support the use of custom verification functions, we only need a callback function defined as follow that is passed as argument into `check_next` function.

```Javascript
function(password, hash) {
	return custom_hashing_function(password) === hash;
}
```

## API

`Checker`
  * `clear_old_session(clear_hashes)`
    * `clear_hashes` - [OPTIONAL] - Default value is true
  * `load_passwords(hashes)`
    * `rounds` - [REQUIRED] - Array strings that are hashes
  * `load_passwords_with_identities(hashes)`
    * `rounds` - [REQUIRED] - Array of arrays in the format of (hash, identity)
  * `check_next(verify_callback)`
    * `verify_callback` - [OPTIONAL] - A callback that will be used for verification of hash and password
      * `password` - First parameter to the callback is the password
      * `hash` - Second parameter to the callback is the hash
