from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)

app.config.from_pyfile("config.py")
if app.config["APM_ENABLED"]:
	from elasticapm.contrib.flask import ElasticAPM
	print("starting apm")
	apm = ElasticAPM(app)
else:
	print("no apm to start")

db = SQLAlchemy(app)

migrate = Migrate(app, db)


from enquiry_api import models
from enquiry_api.blueprints import register_blueprints
from enquiry_api.exceptions import register_exception_handlers

register_exception_handlers(app)
register_blueprints(app)
