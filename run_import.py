from import_data.import_data_scripts import run_imports
from enquiry_api import app
from flask_sqlalchemy import SQLAlchemy

app.config.from_pyfile("config.py")
app.config['SQLALCHEMY_POOL_SIZE'] = 100

db = SQLAlchemy(app)

from enquiry_api import models

if __name__ == "__main__":
    run_imports()
