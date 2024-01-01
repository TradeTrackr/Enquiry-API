from flask_script import Manager
from enquiry_api import app
import os

manager = Manager(app)

@manager.command
def runserver(port=9998):
    """Run the app using flask server"""

    os.environ["PYTHONUNBUFFERED"] = "yes"
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["COMMIT"] = "LOCAL"
    os.environ["FLASK_APP"]=manage.py


    app.run(debug=True, port=int(port))

if __name__ == "__main__":
    manager.run()
