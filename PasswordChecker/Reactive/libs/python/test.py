from pprint import pprint
from ReactivePasswordChecker import Checker

# Load hashes from database
hashed_passwords = [
'$2b$10$xtvC0Zem4uuAyy3A9fBWceL9FrXBhOAfRwuopK5rSU6vWYlDiiP3O', # 123456
'$2b$10$ZS1SBn0D0lm/h8NUEpMcMOJiZbbOjFbIutl0hBo4MACz4kpIdRrva', # asdasd
'$2b$10$ZuMY1CshH6SeazCkb2RrfujZdWzCM1HBJhYIXxKBo0g5C5s7BIDTO', # 123456789
'$2b$10$kK4PzfYE67M7EXT1cQEkTOQFUlvPV00zwS0o60a0sfYg9HmJvsmia', # 000000
'$2b$10$6jjNtsYew6GB9sdoHvpoYux.BDR8/qDc/BwuqkS4C9hxw55RvMVL6', # qwerty
'$2b$10$uZSMpFh6pRDruTjRoMnlAuw90LUP8dREbqrTFmYCQKCs4Df3FyGeO', # 123456
'$2b$10$SN2khE2KYgmPQANLPk1GA.WAUBzY5/oY5bO4rTTplhBAc9UdalBSS', # asdasd
'$2b$10$r4vkDQ7K6Z866KdjmEmH3evVDacSq4tq4zJdEFMa9SfS9M9hwkkIa', # 123456789
'$2b$10$5mz2ou0dcPp5B8f9PpvKf./nf9H/05c900vwNdhXc05zcTduju7fe', # 000000
'$2b$10$.YlVb4GJr4U4zFfEO1cMteAWMUw4tpLKGqDi0BWvXhjh5.2Z7Nvdu', # qwerty
'$2b$10$A6NpJYAxCSHwygFh5G8/reqa0Yxn8yob57uH73KgGbal3feM4GFk.'  # 7777777
]

# Instantiate class, enable debuging mode
checker = Checker(True)

# When we want to start again, uncomment this part
#checker.clear_old_session()

# Load hashes
checker.load_passwords(hashed_passwords)

# Keep checking them until all are checked
while True:
    weak_hashes = checker.check_next()

    # Ending
    if weak_hashes is None:
        break

    # Notify users of their weak hashes
    pprint(weak_hashes)
