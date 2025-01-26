from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField,PasswordField,SubmitField,ValidationError,BooleanField,FileField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from flaskblog.model import User
from flask_login import current_user

#创建注册表类
class RegistrationForm(FlaskForm):
    #DataRequired表示数据不能为空；Length限制输入数据的长度
    username=StringField("Username",validators=[DataRequired(),Length(min=2,max=20)])
    #Email验证邮箱的有效性
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo("password")])
    submit=SubmitField("Sign Up")

    def validate_username(self,username):
        user=User.query.filter(User.username==username.data).first()
        if user:
            raise ValidationError("The username already exists. Please choose another one!")
    
    def validate_email(self, email):
        email=User.query.filter(User.email==email.data).first()
        if email:
            raise ValidationError("The email already exists. Please choose another one!")

class LoginForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    #remember用来确定是否使用secure cookie
    remember=BooleanField("Remember Me")
    submit=SubmitField("Login")

class UpdateAccountForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField("Email",validators=[DataRequired(),Email()])
    picture=FileField("Upadate Profile Picture",validators=[FileAllowed(["jpg","png"])])
    submit=SubmitField("Upadate")

    def validate_username(self,username):
        if username.data==current_user.username:
            user=User.query.filter(User.username==username.data).first()
            if user:
                raise ValidationError("The username already exists. Please choose another one!")
    
    def validate_email(self, email):
        if email.data==current_user.email:
            email=User.query.filter(User.email==email.data).first()
            if email:
                raise ValidationError("The email already exists. Please choose another one!")

class RequestResetForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('Request Passowrd Reset')

    def validate_email(self, email):
        email=User.query.filter(User.email==email.data).first()
        if email is None:
            raise ValidationError("There is no account with that email. You must register first.")

class ResetPasswordForm(FlaskForm):
    password=PasswordField("Password",validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo("password")])
    submit=SubmitField('Reset Password')