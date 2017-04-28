from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "dyrutiy786futiugyd5s7dfugy"
# local
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://project2:iyfmq0j007i@localhost/project2"
# heroku
app.config['SQLALCHEMY_DATABASE_URL'] = "postgresql://gtuhxuesxaerwz:8927799e7c3a60d6fb68ccb0ff2a059bf532378f7137a1eb463e1a8ee4271117@ec2-54-243-252-91.compute-1.amazonaws.com:5432/d8u15687avuqtg"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
