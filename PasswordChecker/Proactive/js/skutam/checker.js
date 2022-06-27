import { simple_analysis } from './proactive-password-checker/module/simple_analysis.js';
import { substring_analysis } from './proactive-password-checker/module/substring_analysis.js';
import { character_class_analysis, get_char_classes } from './proactive-password-checker/module/character_class_analysis.js';
import { sequence_analysis } from './proactive-password-checker/module/sequence_analysis.js';
import { word_use_analysis } from './proactive-password-checker/module/word_use_analysis.js';

export function get_character_classes() {
    return get_char_classes();
};

/**
 * Calculate the similarity rate of passwords with the ones we analysed
 * @param {string} password Password to be analysed
 * @returns {flaot} Value in range <0.0, 1.0> describing the similarity of password with the ones found in leaked databases
 */
export function validate_password(password) {
    // Passwords with length of 2 and lesser are automatically calculated to be 1.0, meaning BAD
    if (password.length <= 2) {
        return {result: 1.0};
    }

    var _simple_analysis = simple_analysis(password);                       // DONE
    var _substring_analysis = substring_analysis(password);                 // DONE
    var _character_class_analysis = character_class_analysis(password);     // DONE
    var _sequence_analysis = sequence_analysis(password);
    var _word_use_analysis = word_use_analysis(password);

    var result = 0;
    result += _simple_analysis['result'];
    result += _substring_analysis['result'];
    result += _character_class_analysis['result'];
    result += _sequence_analysis['result'];
    result += _word_use_analysis['result'];
    result /= 5.0;

    return {
        'simple_analysis': _simple_analysis,
        'substring_analysis': _substring_analysis,
        'character_class_analysis': _character_class_analysis,
        'sequence_analysis': _sequence_analysis,
        'word_use_analysis': _word_use_analysis,
        'result': result
    };
};