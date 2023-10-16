from app.extensions import db

class ToDo(db.Model):
    __tablename__ = 'to_do_list'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    task = db.Column(db.String(255), nullable=False)
    deadline = db.Column(db.Date)
    completed = db.Column(db.Boolean)

    def __repr__(self) -> str:
        return f'{self.username}:{self.task}'
