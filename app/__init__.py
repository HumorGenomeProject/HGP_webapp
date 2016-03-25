from flask import Flask
import logging

app = Flask(__name__)
from app import views

log = logging.getLogger()
log.setLevel(logging.DEBUG)
