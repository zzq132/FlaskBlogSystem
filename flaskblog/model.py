from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as serializer
from flaskblog import db,login_manager
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#数据库对象
class User(db.Model,UserMixin):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    image_file=db.Column(db.String(20),nullable=False,default="default.jpg")
    password=db.Column(db.String(60),nullable=False)
    posts=db.relationship('Post',back_populates='author')

    def get_reset_token(self):
        s=serializer(current_app.config['SECRET_KEY'])
        with open("FlaskApp\\flaskblog\\static\\token.txt","w") as f:
            s.dump({'user_id':self.id},f)
        with open("FlaskApp\\flaskblog\\static\\token.txt","r") as f:
            token=f.read()
        return token
    
    @staticmethod
    def verify_reset_token(token,expires_sec=1800):
        s=serializer(current_app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token,max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    __tablename__='post'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    date_post=db.Column(db.DateTime,nullable=False,default=datetime.now)
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    author=db.relationship('User',back_populates='posts')
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_post}')"
