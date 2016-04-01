from flask import Flask
import logging
from secrets import SECRET_SESSION, SECRET_SALT

app = Flask(__name__)
app.secret_key = SECRET_SESSION

import controller

log = logging.getLogger()
log.setLevel(logging.DEBUG)
