
from flask import Flask,render_template,request,jsonify,session,redirect,url_for
from flask_recaptcha import ReCaptcha
from flask_mail import Mail
from flask_mail import Message
#from models import User
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField,validators,DateField,SelectField
from wtforms.validators import InputRequired,Email,Length 
#from wtforms_sqlalchemy.orm import model_form
from flask_sqlalchemy import SQLAlchemy
import requests

#login
from flask_login import LoginManager,UserMixin,login_user,login_required,current_user
login_manager=LoginManager()
import json

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:helloworld@localhost/intuitionmachine'
app.config['MAIL_USERNAME'] = 'valdez@codeaudit.com'
app.config['MAIL_PASSWORD'] = 'helloworld112233'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['CSRF_ENABLED'] = True
app.config.update(dict( RECAPTCHA_ENABLED = True, RECAPTCHA_SITE_KEY = "6Lf3ti8UAAAAAHSO98fqkGKvDfP99T2VE_jfpwi7", RECAPTCHA_SECRET_KEY = "6Lf3ti8UAAAAAAv_LKpvRBez-FzAG7FWEIRvViV3" ))
app.config['SECRET_KEY']='Secret'
mail=Mail(app)
mail.init_app(app)
recaptcha= ReCaptcha()
recaptcha.init_app(app)
db=SQLAlchemy(app)

login_manager.init_app(app)
login_manager.login_message='You must be logged in to view this page.'


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

from flask_login import UserMixin
class User(UserMixin,db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer,primary_key=True)
	fname = db.Column(db.String(50))
	lname = db.Column(db.String(50))
	birthday=db.Column(db.String(50))
	email=db.Column(db.String(255),unique=True)
	streetAddress=db.Column(db.String(255))
	country=db.Column(db.String(255))
	city=db.Column(db.String(255))
	state=db.Column(db.String(255))
	zipCode=db.Column(db.String(255))
	ethAddress=db.Column(db.String(255))
	govID=db.Column(db.String(255))
	geoIP=db.Column(db.String(255))
	geoLoc=db.Column(db.String(255))
	password=db.Column(db.String(255))
	role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
	is_admin = db.Column(db.Boolean(), default=False)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role',lazy='dynamic')

class LoginForm(FlaskForm):
	email = StringField('email', [validators.DataRequired()],description='email')
	password = PasswordField('password', [validators.DataRequired()],description='password')
class SignupForm(FlaskForm):	
	email = StringField('email', [validators.Length(min=4, max=25)])
	password =PasswordField('password', [validators.Length(min=4, max=25)])
	fname=StringField("fname", [validators.Length(min=4, max=25)])
	lname=StringField("lname", [validators.Length(min=4, max=25)])
	birthday=DateField("birthday")
	streetAddress=StringField("streetAddress", [validators.DataRequired()])
	country=SelectField("country", [validators.DataRequired()])
	city=StringField("city", [validators.Length(min=4, max=25)])
	state=StringField("state", [validators.Length(min=4, max=25)])
	zipCode=StringField("zipCode", [validators.Length(min=4, max=25)])
	ethereumAddress=StringField("ethereumAddress", [validators.DataRequired()])
	govID=StringField("govID", [validators.Length(min=4, max=25)])

@app.route('/getcountry')
def get_country():
	temp=User.query.all()
	countryData={} #city:count
	for user in temp:
			countryData[user.country]=0
	print(countryData)
	for user in temp:
		if user.country in countryData:
			countryData[user.country]+=1
	jsonData=[]
	for i in countryData:
		jsonData.append({'country':i,'count':countryData[i]})
	return jsonify(jsonData)
@app.route('/getusers')
def get_users():
	temp=User.query.all()	
	city=[]
	country=[]
	state=[]
	geoLoc=[]
	print(temp)
	for user in temp:
		city.append(user.city)
		country.append(user.country)
		state.append(user.state)
		geoLoc.append(user.geoLoc)
	print(city)
	return jsonify({'city':city,'country':country,'state':state,'geoloc':geoLoc})
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for("login"))

@app.route('/', methods=['GET','POST'])
def index():
	error=None
	success=False
	form=SignupForm()
	if request.method=='POST':
		tempUser=User.query.filter_by(email=form.email.data).first()
		if tempUser:
			error='Email Already Exists'
			return render_template('index.html',error=error,success=success,form=form)
		else:
			geoIP=request.remote_addr
			url = 'http://freegeoip.net/json/'+geoIP
			req=requests.get(url)
			reqJSON = req.json()
			geoLoc = reqJSON['country_name']
			test=User(fname=form.fname.data,lname=form.lname.data,email=form.email.data,birthday=form.birthday.data,
				streetAddress=form.streetAddress.data,country=request.form.get('country'),city=form.city.data
				,state=form.state.data,zipCode=form.zipCode.data,ethAddress=form.ethereumAddress.data,govID=form.govID.data,geoIP=geoIP,geoLoc=geoLoc,password=form.password.data)
			db.session.add(test)
			db.session.commit()
			success=True
			return redirect(url_for('login'))
	else:
		return render_template('index.html',error=error,success=success,form=form)

@app.route('/login',methods=['GET','POST'])
def login():
	error=None
	form=LoginForm()
	if request.method=='POST':
		print ("HEY")
		print (form.email.data)
		testUser=User.query.filter_by(email=form.email.data).first()
		print(testUser)
		print(testUser.is_admin)
		print (form.password.data)
		print(testUser.password)
		if testUser is not None and form.password.data==testUser.password:
			login_user(testUser)
			if testUser.is_admin:
					return redirect(url_for('admin_main'))
			else:
				return redirect(url_for('main'))
		else:
			error="Invalid Username or Password."
			return render_template('login.html',error=error,form=form)
	else:
		return render_template('login.html',error=error,form=form)

@app.route('/main',methods=['GET','POST'])
@login_required
def main():
		return "success"
@app.route('/admin')
@login_required
def admin_main():
	return render_template('admin.html')

if __name__ == "__main__": 
           app.run()