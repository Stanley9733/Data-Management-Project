from flask import Flask
from flask import Blueprint, redirect, render_template, request, url_for, jsonify,flash
from datetime import datetime
app = Flask(__name__)
app.debug = True


import mysql.connector
from mysql.connector import errorcode

app.secret_key = b'\x11\xae\xba\x13\xca-\xa8X\x84l\xf3\xd3\xa3x\xed\x10'

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
        cursor.execute("select admin from employee where name = %s;",(name,))
        admin = cursor.fetchall()
        print(admin)
        if len(admin)==0:
            flash("You are not in the database")
        else:      
            if admin[0][0] == 1:
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
    # cursor.execute("select AvailableRedeemPoints from points where EID= %s;",(id[0],))
    # r_point = cursor.fetchone()[0]
    cursor.execute("select * from points where EID= %s;",(id[0],))
    result = cursor.fetchone()
    print(result)
    showname = name
    return render_template("Employee home.html", showname = showname, result = result)


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
            return render_template("Redeem.html", invalid = True,point_current=point_current)
        else:
            cursor.execute("insert into redeem(RedeemTime, EID, Pointsused, GiftCard) values(%s,%s,%s,%s);",(date, id[0], points, points/100))
            cursor.execute("select AvailableRedeemPoints from points where EID= %s;",(id[0],))
            Available = cursor.fetchone()[0]
            cursor.execute("UPDATE points SET AvailableRedeemPoints = %s where EID = %s;",(Available-points,id[0],))

            cursor.execute("select Rewards from points where EID= %s;",(id[0],))
            reward = cursor.fetchone()[0]
            cursor.execute("UPDATE points SET Rewards = %s where EID = %s;",(reward+points/100,id[0],))

            # cursor.execute("select AvailableRedeemPoints from points where EID= %s;",(id[0],))
            # AvailableRedeemPoints = cursor.fetchone()[0]
            # cursor.execute("UPDATE points SET AvailableRedeemPoints = %s where EID = %s;",(AvailableRedeemPoints-points,id[0],))
            conn.commit()
            return render_template("Redeem.html", invalid = False)

    return render_template("Redeem.html")

    

@app.route('/admin/<name>',methods=['GET', 'POST'])
def admin_home(name):
    # report of check employee
    cursor.callproc("not_give_all;")
    for result in cursor.stored_results():
            usernotgiveall = result.fetchall()
    print(usernotgiveall)

    # aggregate usage of points
    cursor.callproc("get_usage;")
    for result in cursor.stored_results():
            usage = result.fetchall()

    # report of all redemptions
    cursor.execute("select distinct year(RedeemTime) as year, month(RedeemTime) as month from redeem order by year desc, month desc limit 2;")
    year_month = cursor.fetchall()
    y1 = [x[0] for x in year_month][0]
    m1 = [x[1] for x in year_month][0]
    y2 = [x[0] for x in year_month][1]
    m2 = [x[1] for x in year_month][1]
    cursor.execute("select year(RedeemTime) as year, month(RedeemTime) as month, EID, sum(Pointsused), sum(GiftCard) from redeem where year(RedeemTime) = %s or year(RedeemTime) = %s and month(RedeemTime) = %s or month(RedeemTime) = %s  group by year, month,EID;",(y1,y2,m1,m2))
    result = cursor.fetchall()
    print(result)
    


    reset = False
    if request.method == 'POST':
        # cursor.execute("update points set AvaliableGivePoints = 1000;")
        cursor.execute("select eid from employee;")
        employee = cursor.fetchall()
        for e in [x[0] for x in employee]:
            cursor.execute("select * from points where eid=%s order by Months desc",(e,))
            record = cursor.fetchall()
            # print(record[5])
            cursor.execute("insert into points values (DATE_ADD(%s, INTERVAL 1 MONTH), %s, %s, %s, %s, %s, %s);",(record[0][0],record[0][1],record[0][2],1000,record[0][4],record[0][5],record[0][6],))
            # cursor.execute("insert into points values (DATE_ADD(%s, INTERVAL 1 MONTH), %s, %s, %s, %s, %s, %s);",("2019-10-01",1,2,3,4,5,6,))
            conn.commit()
        reset = True

    cursor.execute("select * from employee where admin=0;")
    employee = cursor.fetchall()
    return render_template("Admin home.html",employee = employee, reset = reset, result = result, usernotgiveall=usernotgiveall,usage=usage)