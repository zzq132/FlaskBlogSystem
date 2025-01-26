import os

class Config():
    #SECRET_KEY用于对会话数据进行加密和签名；启用于 CSRF 保护时，用于生成唯一的 CSRF Token
    #密钥使用secrets.token_hex(15)生成
    SECRET_KEY=os.environ.get("SECRET_KEY")
    #连接数据库
    SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI")
    MAIL_SERVER="smtp.163.com"
    MAIL_PORT=465
    MAIL_USE_TLS=False
    MAIL_USE_SSL = True
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER=os.environ.get("MAIL_USERNAME")