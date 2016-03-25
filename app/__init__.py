from flask import Flask
import logging

app = Flask(__name__)
from app import controller

log = logging.getLogger()
log.setLevel(logging.DEBUG)
