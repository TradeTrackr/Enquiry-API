from import_data.import_data_scripts import run_imports
from enquiry_api import app
from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import uuid
import requests
from flask.json import JSONEncoder
from datetime import date

app.config.from_pyfile("config.py")
app.config['SQLALCHEMY_POOL_SIZE'] = 100

db = SQLAlchemy(app)

from enquiry_api import models

if __name__ == "__main__":
    run_imports()
