from flask import Flask
from flask import Blueprint, redirect, render_template, request, url_for, jsonify
app = Flask(__name__)
app.debug = True


import mysql.connector
from mysql.connector import errorcode

# Obtain connection string information from the portal
# config = {
#   'host':'msitmdbms.mysql.database.azure.com',
#   'user':'SS2020@msitmdbms',
#   'password':'SSdbms@2020',
#   'database':'dbms2020'
# }

# # Construct connection string
# try:
#    conn = mysql.connector.connect(**config)
#    print("Connection established")
# except mysql.connector.Error as err:
#   if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#     print("Something is wrong with the user name or password")
#   elif err.errno == errorcode.ER_BAD_DB_ERROR:
#     print("Database does not exist")
#   else:
#     print(err)
# else:
#   cursor = conn.cursor()

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


# cursor.execute("DROP TABLE IF EXISTS inventory;")
# print(cursor.rowcount)
cursor.execute("CREATE TABLE employee (eid int PRIMARY KEY, name VARCHAR(50), phone varchar(25), admin bool, password varchar(50));")
print("Finished creating table.")

conn.commit()
cursor.close()
conn.close()



@app.route('/',methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        name = data['username']
        return redirect('/table/{}'.format(name))
    return render_template("homepage.html")

@app.route('/table/<id>',methods=['GET', 'POST'])
def showinfo(id):
    if request.method == 'POST':
        move = request.form['submit']
        if move == 'Check Points':
            return redirect('/redeem/{}'.format(id))
        if move == 'Give Points':
            return redirect("https://www.youtube.com/")
        if move == 'Redeem Points':
            return redirect("http://www.baidu.com")
    showname = id
    return render_template("Employee home.html", showname = showname)


@app.route('/redeem/<id>',methods=['GET', 'POST'])
def redeem(id):
    return render_template("Redeem.html")   