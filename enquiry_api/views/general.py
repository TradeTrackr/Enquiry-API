from flask import request, Blueprint, Response, json, current_app

general = Blueprint('general', __name__)


@general.route("/health")
def check_status():
    return Response(response=json.dumps({
        "app": current_app.config["APP_NAME"],
        "status": "OK",
    }),  mimetype='application/json', status=200)
