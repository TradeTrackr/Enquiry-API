from enquiry_api import app
from enquiry_api.views import general, enquiry, client

def register_blueprints(app):
    """
    Adds all blueprint objects into the app.
    """
    app.register_blueprint(general.general)
    app.register_blueprint(enquiry.enquiry)
    app.register_blueprint(client.client)

    # All done!
    app.logger.info("Blueprints registered")
