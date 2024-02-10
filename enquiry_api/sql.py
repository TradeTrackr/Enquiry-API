from enquiry_api import db
from enquiry_api.models import Enquiry, EnquiryActivity
from sqlalchemy import desc, and_
from datetime import datetime, timedelta

class Sql(object):
    # create a Session
    session = db.session

#start of search sql statements
    def get_enquirys(params):
        variable= Sql.session.query(Enquiry).filter_by(**params).all()
        return variable

    def get_enquiry_activity(params):
        variable= Sql.session.query(EnquiryActivity).filter_by(**params).all()
        return variable

    def get_new_enquiries(company_id):
        # Get the current date and time
        now = datetime.utcnow()
        
        # Calculate the date and time for 7 days ago
        seven_days_ago = now - timedelta(days=7)
        print(seven_days_ago)

        variable = Sql.session.query(Enquiry).filter(
            and_(
                Enquiry.timestamp >= seven_days_ago,
                Enquiry.company_id == company_id,
            )
        ).all()

        return variable

    def get_enquiry_and_activity(params):
        variable = Sql.session.query(Enquiry, EnquiryActivity)\
                            .outerjoin(EnquiryActivity, Enquiry.id == EnquiryActivity.enquiry_id)

        # Assuming 'params' is a dictionary that contains 'id' and 'company_id' you want to filter by
        if 'id' in params:
            variable = variable.filter(Enquiry.id == params['id'])
        if 'company_id' in params:
            variable = variable.filter(Enquiry.company_id == params['company_id'])

        return variable.all()

    def get_enquirys_most_recent_activity(params):
        variable = Sql.session.query(Enquiry).filter(Enquiry.email == params['email'], Enquiry.company_id == params['company_id'])
        enquiries_list = []

        enquiries = variable.all()
        for enquiry in enquiries:
            # Fetch the most recent activity for the current enquiry
            most_recent_activity = Sql.session.query(EnquiryActivity)\
                                        .filter(EnquiryActivity.enquiry_id == enquiry.id)\
                                        .order_by(desc(EnquiryActivity.timestamp))\
                                        .first()

            enquiry_dict = enquiry.to_dict()
            enquiry_dict['most_recent_activity'] = most_recent_activity.to_dict() if most_recent_activity else None
            enquiries_list.append(enquiry_dict)

        return enquiries_list


#start of insert sql Statements
    def new_enquiry(params):
        try_type = Enquiry(**params)
        Sql.session.add(try_type)
        Sql.session.commit()
        return Sql.get_enquirys(try_type.to_dict())

    def new_enquiry_activity(params):
        try_type = EnquiryActivity(**params)
        Sql.session.add(try_type)
        Sql.session.commit()
        return Sql.get_enquiry_activity(try_type.to_dict())

#start of update sql Statements
    def update_enquiry(id, params):
        updating = Sql.session.query(Enquiry).get(id)
        for key, value in params.items():
            setattr(updating, key, value)
        Sql.session.commit()
        return Sql.get_enquirys({'id':id})

