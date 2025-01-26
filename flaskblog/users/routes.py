import os
import flask as fk
from flask_login import current_user,login_user,logout_user,login_required
from flaskblog.users.forms import RegistrationForm,LoginForm,UpdateAccountForm,RequestResetForm,ResetPasswordForm
from flaskblog.model import User,Post
from flaskblog import db,bcrypt
from flaskblog.users.utils import save_picture,send_reset_email

users=fk.Blueprint("users",__name__)

@users.route("/register",methods=["GET","POST"])
def registerPage():
    if current_user.is_authenticated:
        return fk.redirect(fk.url_for("main.homePage"))
    form=RegistrationForm()
    #提交的信息合法则显示成功创建账户
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data)
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        fk.flash(f"Your account is created! Please log in.","success")
        return fk.redirect(fk.url_for("users.loginPage"))
    return fk.render_template("register.html",title="Register",form=form)

@users.route("/login",methods=["GET","POST"])
def loginPage():
    if current_user.is_authenticated:
        return fk.redirect(fk.url_for("main.homePage"))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            nextPage=fk.request.args.get("next")
            fk.flash("Login Successful!","success")
            return fk.redirect(nextPage) if nextPage else fk.redirect(fk.url_for('main.homePage'))
        else:
            fk.flash("Login Unsuccessful. Please check email and password!","danger")
    return fk.render_template("login.html",title="Login",form=form)

@users.route("/logout")
def logoutPage():
    logout_user()
    return fk.redirect(fk.url_for("main.homePage"))

@users.route("/account",methods=["GET","POST"])
@login_required
def accountPage():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_fn=save_picture(form.picture.data)
            if current_user.image_file != "default.jpg":
                os.remove(os.path.join(users.root_path,"static/images",current_user.image_file))
            current_user.image_file=picture_fn
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        fk.flash("Your account has been updated!","success")
        return fk.redirect(fk.url_for("users.accountPage"))
    elif fk.request.method=="GET":
        form.username.data=current_user.username
        form.email.data=current_user.email
    imageFile=fk.url_for("static",filename="/images/"+current_user.image_file)
    return fk.render_template("account.html",title="Account",image=imageFile,form=form)

@users.route("/user/<username>")
def userPosts(username):
    page=fk.request.args.get("page",default=1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user).order_by(Post.date_post.desc()).paginate(page=page,per_page=3)
    return fk.render_template("user_posts.html",posts=posts,username=username)

@users.route("/reset_password",methods=['GET','POST'])
def resetRequest():
    if current_user.is_authenticated:
        return fk.redirect(fk.url_for("main.homePage"))
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        fk.flash("An email has been sent with instructions to reset your password","info")
        return fk.redirect(fk.url_for("users.loginPage"))
    return fk.render_template("reset_request.html",title="Reset Passwrord",form=form)

@users.route("/reset_password/<token>",methods=['GET','POST'])
def resetToken(token):
    if current_user.is_authenticated:
        return fk.redirect(fk.url_for("main.homePage"))
    user=User.verify_reset_token(token)
    if user is None:
        fk.flash("That is an invalid or expired token","warning")
        return fk.redirect(fk.url_for("users.resetRequest"))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        password=bcrypt.generate_password_hash(form.password.data)
        user.password=password
        db.session.commit()
        fk.flash("Your password has been updated!","success")
        return fk.redirect(fk.url_for("users.loginPage"))
    return fk.render_template("reset_token.html",title="Reset Passowrd",form=form)