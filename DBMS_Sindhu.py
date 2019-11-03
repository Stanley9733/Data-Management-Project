from flask import Flask
from flask import Blueprint, redirect, render_template, request, url_for, jsonify
import hashlib
app = Flask(__name__)
app.debug = True


import mysql.connector
from mysql.connector import errorcode

try:
    conn = mysql.connector.connect(user='SS2020@msitmdbms',
                                   password='SSdbms@2020',
                                   database='dbms2020',
                                   host='msitmdbms.mysql.database.azure.com',
                                   ssl_ca='BaltimoreCyberTrustRoot.crt.pem')
except mysql.connector.Error as err:
    print(err)
else: 
    cursor = conn.cursor()
salt = "5gz"

### user password validation
def validate_password(db_password, userhashed_password):
    if dbpassword == userhashed_password:
        return True

### user validation function
def validate_user(username, password):
	Error = None
	validate_flag =  False
	cursor.execute("select * from Employee")
	records = cursor.fetchall()
	for itr in records:
		dbname = records[1]
		dbpassword = records[2]
		if dbname == username:
			validate_flag = validate_password(dbpassword, password)
			if(validate_flag == False):
				Error = 'Invalid Credentials. Please try again.'
		else:
			Error = 'Username not found, Please register'
	return validate_flag, Error

##### Insert into database

def registeruser(username, email, password,phonenumber):
    validation = False
    if phonenumber.isdigit() == False:
        print("Please enter only numbers")
    elif len(str(PhoneNumber)) != 10:
        print("Please enter valid Phone Number")
    else:
    	cursor.execute("INSERT INTO employee(name, email, password, phonenumber) VALUES(%s,%s,%s,%s,%s,%s,%s)", (username, email, password, phonenumber,))
        cursor.commit()
        validation = True
            
    return validation


@app.route('/')
def main():
	return render_template('user.html')

# @app.route('/index')
# def index():
# 	if 'username' in session:
# 		 return 'Logged in as ' + username + '<br>' + \
#          "<b><a href = '/logout'>click here to log out</a></b>"
#     else:
#     	return "You are not logged in <br><a href = '/login'></b>" + \
#       "click here to log in</b></a>"

#     return redirect('/user_portal/{}'.format(username))


@app.route('/register')
def register_user():
	Error = None
	### Password encryption usage of salt
	if request.method == 'POST':
		username = request.form['username']
        email = request.form['email']
        Phonenumber = request.form['phoneno']

        ### Password encryption
        password = request.form['password']
        password =  password + salt
        hashed_password =  hashlib.md5(password.encode())
        validation = registeruser(username, email, hashed_password, Phonenumber)
    if validation == False:
        error = "Registration is unsuccessful"
    else:
        error = "No Error"
        return redirect(url_for('user'))

    return render_template('register.html', error = error)


@app.route('/login', methods=['GET', 'POST'])
def login():
	Error = None
	login_validation =  False
	if request.method == 'POST':
		session['username'] = request.form['username']
		username = request.form['username']
		password = request.form['password']
		password =  password + salt
        hashed_password =  hashlib.md5(password.encode())

#### Calling the user and password validation
	login_validation, error_msg = validate_user(username, hashed_password)
	if(login_validation == True):
		return redirect('/user_portal/{}'.format(username))
	else:
		Error = error_msg
        return redirect(url_for('login'))

@app.route('/user_portal/<id>', methods = ['GET', 'POST'])
def user_portal(id):

	if 'username' in session:
		if request.method = 'POST':
			action =  request.form['submit']
		if action = 'Check Points':
			return redirect(url_for('checkpoints'))
		if action  = 'Redeem Points':
			return redirect(url_for('redeempoints'))
		if action = 'Give Points':
			return redirect(url_for('givepoints'))
	showname = id

	return render_template("Employee home.html", showname = showname)



