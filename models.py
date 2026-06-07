from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(100),unique = True,nullable = False)
    password = db.Column(db.String(200),nullable = False)
    profile = db.relationship('Profile',backref = 'user', uselist = False)

class Blog(db.Model):
    __tablename__ = "blog" 
    id = db.Column(db.Integer,primary_key = True)
    filename = db.Column(db.String(200), nullable = False)
    title = db.Column(db.String(50),nullable = False)
    username = db.Column(db.String(200))
    user_id = db.Column(db.Integer)

class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(100),nullable = False)
    profile_pic = db.Column(db.String(200),nullable = False) 
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),unique = True)