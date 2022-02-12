
class ConfigDebug():
    #  SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Ahmad123.@localhost/bank' 
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://Ahmad123:0931440973Zzzz12345@plusbank.mysql.database.azure.com/web'    # File-based SQL database
    SECRET_KEY = 'SDFA11#'






# Flask-Mail SMTP server settings
    MAIL_SERVER = '127.0.0.1'
    MAIL_PORT = 1025
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'email@example.com'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'

# Flask-User settings
    USER_APP_NAME = "Flask-User Basic App"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True        # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"
 