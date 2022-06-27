from .Analyses import simple_analysis, char_class_analysis, sequence_analysis, substring_analysis, word_use_analysis


def validate_password(password: str):
    # Passwords with length of 2 and lesser are automatically calculated to be 1.0
    if len(password) <= 2:
        return {'result': 1.0}

    # Get result of each analysis
    result = {'simple_analysis': simple_analysis(password),
              'char_class_analysis': char_class_analysis(password),
              'sequence_analysis': sequence_analysis(password),
              'substring_analysis': substring_analysis(password),
              'word_use_analysis': word_use_analysis(password)}

    # Get average result of all the analysis
    result['result'] = float(sum([result[key]['result'] for key in result.keys()]) / 5.0)
    return result
