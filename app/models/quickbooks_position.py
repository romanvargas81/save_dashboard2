from services.db import DB as db

class QuickbooksPosition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submitter = db.Column(db.String(length=50), nullable=False)
    as_of_date = db.Column(db.DateTime, nullable=False)
    period = db.Column(db.Date, nullable=False)
    wisetack_junior_position = db.Column(db.Float)
    lighter_junior_position = db.Column(db.Float)
 
    def __init__(self, submitter, as_of_date, period, wisetack_junior_position,lighter_junior_position ):
        self.submitter = submitter
        self.as_of_date = as_of_date
        self.period = period
        self.wisetack_junior_position = wisetack_junior_position
        self.lighter_junior_position = lighter_junior_position