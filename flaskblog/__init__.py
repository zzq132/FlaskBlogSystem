import flask as fk
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


db=SQLAlchemy()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view="users.loginPage"
login_manager.login_message_category="info" #设置提醒信息的bootstrap类
mail=Mail()

def create_app(config_file=Config):
    app=fk.Flask(__name__)
    app.config.from_object(config_file)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    with app.app_context():
        db.create_all()

    from flaskblog.main.routes import main
    from flaskblog.posts.routes import posts
    from flaskblog.users.routes import users
    from flaskblog.errors.handlers import errors
    #注册蓝图示例
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(users)
    app.register_blueprint(errors)

    return app