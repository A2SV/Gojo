from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Message(db.Model):

    __tablename__ = 'message'
    
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(), nullable=False)
    from_bot = db.Column(db.Boolean(), nullable=False)
    timestamp = db.Column(db.BigInteger(), nullable=False)

    def __init__(self, chat_id, message, from_bot, timestamp):
        self.chat_id = chat_id
        self.message = message
        self.from_bot = from_bot
        self.timestamp = timestamp

    def __repr__(self):
        return self.message
    
    