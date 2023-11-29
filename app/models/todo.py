from app.extensions import db
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property 

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    to_dos = db.relationship('ToDo', backref='user', lazy=True)
    
    @hybrid_property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, plaintext_password):    
        self._password = generate_password_hash(plaintext_password)

    def set_password(self, password):
        self.password = password

    def check_password(self, plaintext_password):
        return check_password_hash(self._password, plaintext_password)

    def __repr__(self) -> str:
        return f'User: {self.username}'

class ToDo(db.Model):
    __tablename__ = 'to_do_list'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    task = db.Column(db.String(255), nullable=False)
    deadline = db.Column(db.Date)
    completed = db.Column(db.Boolean)

    def __repr__(self) -> str:
        return f'{self.username}:{self.task}'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))