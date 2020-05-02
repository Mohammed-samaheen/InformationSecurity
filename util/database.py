from hashlib import sha256

filename = "database.txt"

with open(filename, 'r+') as d:
    content = d.readlines()
f = open(filename, 'a+')
salt = "InformationSecurity"


def user_validation(Username, Password):
    for i in content:
        entry = i.split("\t\t")

        # Username is in database
        if Username == entry[0]:

            # Hash given password and compare to database

            hashed_password = sha256((Password + salt).encode("utf-8")).hexdigest()

            if hashed_password == str.strip(entry[1]):
                # User entered correct password
                return True
            else:
                return False


def add_user(Username, Password):
    f.write(Username)
    hashed_password = sha256((Password + salt).encode("utf-8")).hexdigest()
    f.write('\t\t' + hashed_password + '\n')
    f.close()