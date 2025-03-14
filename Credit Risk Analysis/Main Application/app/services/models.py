from sqlalchemy import Column, Integer, String, DateTime
from app.server import db


class ActionCapture(db.Model):
    __tablename__ = "action_capture"
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    pair_id = db.Column(db.String(255))
    company_id_voted = db.Column(db.String(255))
    company_name_voted = db.Column(db.String(255))
    company_id_compared = db.Column(db.String(255))
    company_name_compared = db.Column(db.String(255))
    button1_clicked = db.Column(db.Integer) # for ML training set
    user = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, nullable=False)


    def __repr__(self):
        return "<ActionCapture %r>" % self.id


# Create User table:
class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique = True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
        return "<User %r>" % self.id   
    def is_active():
        return True
    def get_id(self):
        return self.id


