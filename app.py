
from flask import Flask,render_template,request,jsonify,session,redirect,url_for
from flask_recaptcha import ReCaptcha
from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'valdez@codeaudit.com'
app.config['MAIL_PASSWORD'] = 'efvaldez123356969'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config.update(dict( RECAPTCHA_ENABLED = True, RECAPTCHA_SITE_KEY = "6Ldssi8UAAAAAGtNMFFhm8Wvjr2N2DA67FMzo2Ta", RECAPTCHA_SECRET_KEY = "6Ldssi8UAAAAAL3uWzsmYds4MjKFxZ4dHFSBUZjW" ))
mail=Mail(app)
mail.init_app(app)
recaptcha= ReCaptcha()
recaptcha.init_app(app)

@app.route('/')
def index():
	return render_template('login.html')
@app.route('/login' , methods=['POST'])
def submit():
	recepient = request.form.get('email')
	fname = request.form.get('fname')
	lname = request.form.get('lname')
	print (recepient)
	msg = Message(subject="Intuition Machine Subscription",
                  sender="valdez@codeaudit.com",
                  recipients=[recepient])
	msg.body="Thank %s %s your for subscibing in Intuition Machine via %s"%(fname,lname,recepient)
	mail.send(msg)
	return "Please confirm email in " + recepient
	
if __name__ == "__main__": 
           app.run()