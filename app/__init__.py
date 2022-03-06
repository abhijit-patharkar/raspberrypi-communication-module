from flask import Flask
from threading import Event 
from app.ping import Ping
app = Flask(__name__)
from app import webroutes