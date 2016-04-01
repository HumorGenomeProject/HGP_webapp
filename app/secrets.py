import os
from os import path
import random
import hashlib
import json

# This is a hidden file stored locally. Will not go on GitHub or ANYWHERE
FILENAME = '.secrets.json'

SECRET_SALT = None
SECRET_SESSION = None

field_salt = 'SALT'
field_session = 'SESSION'

if path.isfile(FILENAME):
    # Just read the file and get secrets
    with open(FILENAME, 'r') as infile:
        the_secrets = json.load(infile)
        SECRET_SALT = the_secrets.get(field_salt)
        SECRET_SESSION = the_secrets.get(field_session)

else:
    # Otherwise, create new secrets and store to file
    # Note: This will only be done once, ever. Once the app runs,
    # the file should not be tampered with

    # This is a crypto hashing library
    sha256 = hashlib.sha256()

    some_random_text = str(int(random.randrange(1234567, 999999999)))
    sha256.update(some_random_text)
    # Let the hex string from the crypto library be our secret salt
    SECRET_SALT = sha256.hexdigest()

    # Make a new sha256 for session secret
    sha256 = hashlib.sha256()

    some_random_text = str(int(random.randrange(1234567, 999999999)))
    sha256.update(some_random_text)
    SECRET_SESSION = sha256.hexdigest()

    the_secrets = {}
    the_secrets[field_salt] = SECRET_SALT
    the_secrets[field_session] = SECRET_SESSION

    # Write these secrets to the hidden file
    with open(FILENAME, 'w') as outfile:
        json.dump(the_secrets, outfile, indent=4)
