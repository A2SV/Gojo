from app import db
from sqlalchemy.dialects.postgresql import JSON

class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(), nullable=False)
    from_bot = db.Column(db.Boolean(), nullable=False)

    def __init__(self, id, message, from_bot):
        self.id = id
        self.message = message
        self.from_bot = from_bot

    def __repr__(self):
        return '<Message %r>' % self.message