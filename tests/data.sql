-- create some users to test authentication
INSERT INTO Users (username, PasswordHash, firstName, lastName, isInfected, isAdmin)
VALUES
    ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'Test', 'User', False, True),
    ('other', 'pbkdf2:sha256:260000$7fhOzRgjqhRCLyoy$8ff82aad06c9578e22133613fee05c2505ae7036600f36321948969945088df5', 'Other', 'User', False, False);