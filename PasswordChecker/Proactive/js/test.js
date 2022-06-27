// Include function from module
import { validate_password } from './skutam/checker.js';

// Define threshold
var threshold = 0.225;

// RUn analysis and compute the similarity rate of password
var result = validate_password('password');

// Show returned array of features
console.log(result);

if (result['result'] < threshold) {
	console.log('Password is strong');
} else {
	console.log('Password is weak');
}
