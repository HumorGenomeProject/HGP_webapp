
# This file stores secrets used for cryptography. Do not share these with anyone anywhere

# To generate new secrets, run the following in a python shell for each
# import hashlib
# sha256 = hashlib.sha256()
# sha256.update('Put some random unique long hard to guess text here')
# secret = sha256.hexdigest()  # This is your secret to copy here

SECRET_SALT = 'f52cc8c9235cfc33d23e6eb3c7163901440804ebcf7ff83896150f841c8057bd'

SECRET_SESSION = '04f38e9a5368681573f339d23a2ab1af4295054dd3265a84ffc193fd0611a046'
