from enquiry_api import db
from enquiry_api.models import Enquiry

class Sql(object):
    # create a Session
    session = db.session

#start of search sql statements
    def get_enquirys(params):
        variable= Sql.session.query(Enquiry).filter_by(**params).all()
        return variable

#start of insert sql Statements
    def new_enquiry(params):
        try_type = Enquiry(**params)
        Sql.session.add(try_type)
        Sql.session.commit()
        return Sql.get_enquirys(try_type.to_dict())

#start of update sql Statements
    def update_enquiry(id, params):
        updating = Sql.session.query(Enquiry).get(id)
        for key, value in params.items():
            setattr(updating, key, value)
        Sql.session.commit()
        return Sql.get_enquirys({'id':id})
