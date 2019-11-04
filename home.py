from flask import Flask
from flask import Blueprint, redirect, render_template, request, url_for, jsonify
from datetime import datetime
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
    cursor = conn.cursor(buffered=True)


# cursor.execute("DROP TABLE IF EXISTS inventory;")
# print(cursor.rowcount)
# cursor.execute("CREATE TABLE employee (eid int PRIMARY KEY, name VARCHAR(50), phone varchar(25), admin bool, password varchar(50));")
# print("Finished creating table.")

# cursor.execute("INSERT INTO employee (eid, name, phone, admin, password) VALUES (%s,%s,%s,%s,%s);", ("wenzhuo@utexas.edu", "stanley",111111111,0,"qwer"))
# print("Inserted",cursor.rowcount,"row(s) of data.")

# conn.commit()
# cursor.close()
# conn.close()



@app.route('/',methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        name = str(data['username'])
        print(name)
        cursor.execute("select admin from employee where name = %s;",(name,))
        admin = cursor.fetchone()
        if admin[0] == 1:
            return redirect('/admin/{}'.format(name))
        else:
            return redirect('/table/{}'.format(name))
    return render_template("homepage.html")

@app.route('/table/<name>',methods=['GET', 'POST'])
def showinfo(name):
    if request.method == 'POST':
        move = request.form['submit']
        if move == 'Give Points':
            return redirect("https://www.youtube.com/")
        if move == 'Redeem Points':
            return redirect('/redeem/{}'.format(name))

    cursor.execute("select eid from employee where name = %s;",(name,))
    id = cursor.fetchone()
    cursor.execute("select AvailableRedeemPoints from points where EID= %s;",(id[0],))
    r_point = cursor.fetchone()[0]
    print(r_point)
    cursor.execute("select * from points where EID= %s;",(id[0],))
    result = cursor.fetchone()
    showname = name
    return render_template("Employee home.html", showname = showname,r_point = r_point, result = result)


@app.route('/redeem/<name>',methods=['GET', 'POST'])
def redeem(name):
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        points = int(data['numofpoints'])
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        cursor.execute("select eid from employee where name = %s;",(name,))
        id = cursor.fetchone()
        # print(id)
        cursor.execute("select AvailableRedeemPoints from points where EID = %s;",(id[0],))
        point_current = cursor.fetchone()
        # print(point_current)
        if int(point_current[0]) < int(points):
            return render_template("Redeem.html", invalid = True)
        else:
            cursor.execute("insert into redeem(RedeemTime, EID, Pointsused, GiftCard) values(%s,%s,%s,%s);",(date, id[0], points, points/100))
            cursor.execute("select AvailableRedeemPoints from points where EID= %s;",(id[0],))
            Available = cursor.fetchone()[0]
            cursor.execute("UPDATE points SET AvailableRedeemPoints = %s where EID = %s;",(Available-points,id[0],))

            cursor.execute("select Rewards from points where EID= %s;",(id[0],))
            reward = cursor.fetchone()[0]
            cursor.execute("UPDATE points SET Rewards = %s where EID = %s;",(reward+points/100,id[0],))
            conn.commit()
            return render_template("Redeem.html", invalid = False)

    return render_template("Redeem.html")

    

@app.route('/admin/<name>',methods=['GET', 'POST'])
def admin_home(name):
    reset = False
    if request.method == 'POST':
        cursor.execute("TRUNCATE transactions;")
        reset = True

    cursor.execute("select * from employee where admin=0;")
    employee = cursor.fetchall()
    return render_template("Admin home.html",employee = employee, reset = reset)