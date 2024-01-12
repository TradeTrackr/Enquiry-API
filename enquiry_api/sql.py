from enquiry_api import db
from enquiry_api.models import Enquiry, EnquiryActivity

class Sql(object):
    # create a Session
    session = db.session

#start of search sql statements
    def get_enquirys(params):
        variable= Sql.session.query(Enquiry).filter_by(**params).all()
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

