from flask import Flask
app = Flask(__name__)

from . import server
from careerbuild.careerbuild import processing
from careerbuild.careerbuild import skills
