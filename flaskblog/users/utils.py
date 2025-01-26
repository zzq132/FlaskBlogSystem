import secrets,os
import flask as fk
from flaskblog import mail
from flask_mail import Message
from flask import current_app

def save_picture(form_picture):
    random_hex=secrets.token_hex(4)
    _,file_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+file_ext
    picture_path=os.path.join(current_app.root_path,"static/images",picture_fn)
    form_picture.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message("Password Reset Request",recipients=[user.email])
    msg.body=f'''To reset your password, visit the following link:
{fk.url_for('users.resetToken',token=token,_external=True)}    
If you didn't make this request, just ignore this email and no changes will be made.'''
    mail.send(msg)
