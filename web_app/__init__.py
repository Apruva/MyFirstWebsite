from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


date_now = datetime.date.today()

app = Flask(__name__)

#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = '\xb0A\x8b\x0c\xd8\xa7p\x01\x19q\xc7@\xc3ac"\xbc$$\xd7\x14\xb5(}'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')


from web_app import routes


