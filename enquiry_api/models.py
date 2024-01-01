from enquiry_api import db
from datetime import datetime
import datetime
from sqlalchemy.dialects.postgresql import JSONB


class Enquiry(db.Model):
    __tablename__ = 'enquiry'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)
    email = db.Column(db.String)
    full_name = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=True)
    phone_number = db.Column(db.Integer)
    additional_information = db.Column(db.String)
    photos = db.Column(JSONB, nullable=True)

    def save(self):  # pragma: no cover
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id" : self.id,
            "email" : self.email,
            "full_name" : self.full_name,
            "timestamp" : self.timestamp,
            "phone_number" : self.phone_number,
            "additional_information" : self.additional_information,
            "photos" : self.photos
        }
