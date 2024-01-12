from enquiry_api import db
from datetime import datetime
import datetime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


class Enquiry(db.Model):
    __tablename__ = 'enquiry'

    id = Column(Integer, primary_key=True)
    company_id = Column(String)
    email = Column(String)
    full_name = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow(), nullable=True)
    phone_number = Column(String)
    additional_information = Column(String)
    photos = Column(JSONB, nullable=True)
    postcode = Column(String)
    address_number_or_name = Column(String)
    address_line1 = Column(String)
    address_line2 = Column(String)
    address_line3 = Column(String)
    category = Column(String)
    category_detail = Column(String)
    status = Column(String)

    def save(self):  # pragma: no cover
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id" : self.id,
            "email" : self.email,
            "full_name" : self.full_name,
            "company_id" : self.company_id,
            "timestamp" : self.timestamp,
            "phone_number" : self.phone_number,
            "additional_information" : self.additional_information,
            "photos" : self.photos,
            "postcode" : self.postcode,
            "address_number_or_name" : self.address_number_or_name,
            "address_line1" : self.address_line1,
            "address_line2" : self.address_line2,
            "address_line3" : self.address_line3,
            "category" : self.category,
            "category_detail" : self.category_detail,
            "status" : self.status
        }

class EnquiryActivity(db.Model):
    __tablename__ = 'enquiryactivity'

    id = Column(Integer, primary_key=True)
    enquiry_id = Column(Integer, ForeignKey('enquiry.id'))
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow(), nullable=True)

    def save(self):  # pragma: no cover
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id" : self.id,
            "enquiry_id" : self.enquiry_id,
            "status" : self.status,
            "timestamp" : self.timestamp
        }
