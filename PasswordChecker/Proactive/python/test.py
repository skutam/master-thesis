from pprint import pprint
from ProactivePasswordChecker import validate_password

threshold = 0.225

result = validate_password('password')

pprint(result)

if result['result'] < threshold:
    print('Password is strong')
else:
    print('Password is weak')
