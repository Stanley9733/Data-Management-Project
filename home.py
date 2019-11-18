from flask import Flask
from flask import Blueprint, redirect, session, render_template, request, url_for, jsonify,flash
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import math
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

# cursor.execute("INSERT INTO employee (eid, name, phone, admin, password) VALUES (%s,%s,%s,%s,%s);", (3, "zhuo",5167290363,0,generate_password_hash("hello")))
# print("Inserted",cursor.rowcount,"row(s) of data.")
# conn.commit()
# cursor.close()
# conn.close()

# cursor.execute("update employee set password = %s where eid = 2;",(generate_password_hash("ryan"),))
# conn.commit()


# cursor.execute("INSERT INTO employee (eid, name, phone, admin, password) VALUES (%s,%s,%s,%s,%s);", (4, "wilshire",8924848102,0,generate_password_hash("wilshire")))
# cursor.execute("INSERT INTO employee (eid, name, phone, admin, password) VALUES (%s,%s,%s,%s,%s);", (5, "jaylen",6728391043,0,generate_password_hash("jaylen")))
# print("Inserted",cursor.rowcount,"row(s) of data.")
# conn.commit()



@app.route('/',methods=['GET', 'POST'])
def hello():
    if 'username' in session:
        return redirect(url_for('showinfo'))
    else:
        if request.method == 'POST':
            data = request.form.to_dict(flat=True)
            name = str(data['username'])
            password = str(data['password'])

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

            cursor.execute("select * from employee where name = %s;",(name,))
            user = cursor.fetchall()
            # print(user)
            # print(password)
            # print(generate_password_hash("hello"))
            # print(user[0][4])
            if len(user)==0:
                flash("Employee Doesn't Exist, Please Check Username")
            else:
                if check_password_hash(user[0][4], password) != True:
                    flash("Incorrect Password")
                # else:
                #     if user[0][4] == 1:
                #         return redirect(url_for('admin_home'))
                else:
                    session['username'] = name
                    return redirect(url_for('showinfo'))

    return render_template("homepage.html")


@app.route('/ad/',methods=['GET', 'POST'])
def admin_login():
    if 'admin' in session:
        return redirect(url_for('admin_home'))
    else:
        if request.method == 'POST':
            data = request.form.to_dict(flat=True)
            name = str(data['admin'])
            password = str(data['password'])

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

            cursor.execute("select * from employee where name = %s;",(name,))
            user = cursor.fetchall()
            if len(user)==0:
                flash("You are not an admin")
            else:
                if check_password_hash(user[0][4], password) != True:
                    flash("Incorrect Password")
                else:
                    if user[0][3] == 1:
                        session['admin'] = str(data['admin'])
                        return redirect(url_for('admin_home'))
                    else:
                        flash("You are not an admin")

    return render_template("Admin login.html")

@app.route('/table/',methods=['GET', 'POST'])
def showinfo():
    if 'username' in session:
        if request.method == 'POST':
            move = request.form['submit']
            if move == 'Give Points':
                return redirect('/send/')
            if move == 'Redeem Points':
                return redirect('/redeem/')

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

        cursor.execute("select eid from employee where name = %s;",(session['username'],))
        id = cursor.fetchone()
        cursor.execute("select * from points where EID= %s and months = (select max(months) from points);",(id[0],))
        result = cursor.fetchone()
        showname = session['username']
        cursor.execute("select time, name, points, message from transactions join employee on EID = Receiver where Sender= %s order by time desc;",(id[0],))
        send = cursor.fetchall()
        cursor.execute("select time, name, points, message from transactions join employee on EID = Sender where Receiver= %s order by time desc;",(id[0],))
        receive = cursor.fetchall()
        return render_template("Employee home.html", showname = showname, result = result,send = send, receive = receive)
    else:
        return redirect(url_for('hello'))



@app.route('/redeem/',methods=['GET', 'POST'])
def redeem():
    if 'username' in session:
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

        if request.method == 'POST':
            data = request.form.to_dict(flat=True)
            points = int(data['numofpoints'])
            cards = math.floor(points/10000)
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
            cursor.execute("select eid from employee where name = %s;",(session['username'],))
            id = cursor.fetchone()
            cursor.execute("select AvailableRedeemPoints from points where EID = %s and months = (select max(months) from points);",(id[0],))
            point_current = cursor.fetchone()
            if cards <= 0:
                return render_template("Redeem.html", invalid = 1,point_current=point_current,showname = session['username'])
            elif int(point_current[0]) < cards*10000:
                return render_template("Redeem.html", invalid = 2,point_current=point_current,showname = session['username'])
            else:
                cursor.execute("insert into redeem(RedeemTime, EID, Pointsused, GiftCard) values(%s,%s,%s,%s);",(date, id[0], cards*10000, cards))
                cursor.execute("select AvailableRedeemPoints from points where EID= %s and months = (select max(months) from points);",(id[0],))
                Available = cursor.fetchone()[0]
                cursor.execute("UPDATE points SET AvailableRedeemPoints = %s where EID = %s and months = (select max(months) from transactions);",(Available-cards*10000,id[0],))
                cursor.execute("select Rewards from points where EID= %s and months = (select max(months) from points);",(id[0],))
                reward = cursor.fetchone()[0]
                cursor.execute("UPDATE points SET Rewards = %s where EID = %s and months = (select max(months) from transactions);",(reward+cards,id[0],))

                conn.commit()
                return render_template("Redeem.html", invalid = 3,cards = cards)

        return render_template("Redeem.html")
    else:
        return redirect(url_for('hello'))



@app.route('/send/',methods=['GET', 'POST'])
def send():
    if 'username' in session:
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

        cursor.execute("select name from employee where admin = 0 and name != %s;",(session['username'],))
        employee = cursor.fetchall()
        if request.method == 'POST':
            data = request.form.to_dict(flat=True)
            points = int(data['numofpoint'])
            message = data['message']
            receiver_name = request.form.get("Employee")
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            month = datetime.today().date().replace(day=1)
            # print(month)  
            cursor.execute("select eid from employee where name = %s;",(session['username'],))
            sender = cursor.fetchone()[0]
            cursor.execute("select eid from employee where name = %s;",(request.form.get("Employee"),))
            receiver = cursor.fetchone()[0]
            cursor.execute("select AvaliableGivePoints, PointsGiven from points where EID = %s and Months = %s;",(sender,month,))
            s = cursor.fetchone()
            if points <= 0:
                return render_template("Givepoints.html", e = employee,invalid = 1)
            elif s[0] > points:
                cursor.execute("insert into transactions(Time,Sender,Receiver,Points,Message) values(%s,%s,%s,%s,%s);",(date,sender,receiver,points,message,))
                conn.commit()
                cursor.execute("select AvailableRedeemPoints, PointsReceived from points where EID = %s and Months = %s;",(receiver,month,))
                r = cursor.fetchone()
                # print(r)
                cursor.execute("update points set AvailableRedeemPoints = %s where EID = %s and Months = %s;",(r[0]+points,receiver,month,))
                cursor.execute("update points set PointsReceived = %s where EID = %s and Months = %s;",(r[1]+points,receiver,month,))

                cursor.execute("update points set AvaliableGivePoints = %s where EID = %s and Months = %s;",(s[0]-points,sender,month,))
                cursor.execute("update points set PointsGiven = %s where EID = %s and Months = %s;",(s[1]+points,sender,month,))
                conn.commit()

                return render_template("Givepoints.html", e = employee, invalid = 2, p = points, name = receiver_name)
            else:
                return render_template("Givepoints.html", e = employee, invalid = 3, s = s)
        return render_template("Givepoints.html",e = employee)
    else:
        return redirect(url_for('hello'))

    

@app.route('/admin/',methods=['GET', 'POST'])
def admin_home():
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

    if 'admin' in session:
        # report of check employee
        cursor.callproc("not_give_all;")
        for result in cursor.stored_results():
                usernotgiveall = result.fetchall()


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
        cursor.execute("select year(RedeemTime) as year, month(RedeemTime) as month, name, sum(Pointsused), sum(GiftCard) from redeem join employee on employee.eid = redeem.eid where year(RedeemTime) = %s and month(RedeemTime) = %s or year(RedeemTime) = %s and month(RedeemTime) = %s  group by year, month, name;",(y1,m1,y2,m2))
        # cursor.execute("select year(RedeemTime) as year, month(RedeemTime) as month, EID, sum(Pointsused), sum(GiftCard) from redeem where year(RedeemTime) = %s or year(RedeemTime) = %s and month(RedeemTime) = %s or month(RedeemTime) = %s  group by year, month,EID;",(y1,y2,m1,m2))
        result = cursor.fetchall()
        # print(result)
        reset = False
        if request.method == 'POST':
            # cursor.execute("update points set AvaliableGivePoints = 1000;")
            cursor.execute("select eid from employee admin=0;")
            employee = cursor.fetchall()
            for e in [x[0] for x in employee]:
                cursor.execute("select * from points where eid=%s order by Months desc",(e,))
                record = cursor.fetchall()
                # print(record)
                # print(record[5])
                cursor.execute("insert into points values (DATE_ADD(%s, INTERVAL 1 MONTH), %s, %s, %s, %s, %s, %s);",(record[0][0],record[0][1],record[0][2],1000,0,0,record[0][6],))
                # cursor.execute("insert into points values (DATE_ADD(%s, INTERVAL 1 MONTH), %s, %s, %s, %s, %s, %s);",("2019-10-01",1,2,3,4,5,6,))
                conn.commit()
            reset = True
            

        cursor.execute("select * from employee where admin=0;")
        employee = cursor.fetchall()
        cursor.callproc("not_give_all;")
        for result in cursor.stored_results():
                usernotgiveall = result.fetchall()
        
        cursor.callproc("get_usage;")
        for result in cursor.stored_results():
            usage = result.fetchall()
        
        cursor.execute("select distinct year(RedeemTime) as year, month(RedeemTime) as month from redeem order by year desc, month desc limit 2;")
        year_month = cursor.fetchall()
        y1 = [x[0] for x in year_month][0]
        m1 = [x[1] for x in year_month][0]
        y2 = [x[0] for x in year_month][1]
        m2 = [x[1] for x in year_month][1]
        cursor.execute("select year(RedeemTime) as year, month(RedeemTime) as month, name, sum(Pointsused), sum(GiftCard) from redeem join employee on employee.eid = redeem.eid where year(RedeemTime) = %s and month(RedeemTime) = %s or year(RedeemTime) = %s and month(RedeemTime) = %s  group by year, month, name;",(y1,m1,y2,m2))
        # cursor.execute("select year(RedeemTime) as year, month(RedeemTime) as month, EID, sum(Pointsused), sum(GiftCard) from redeem where year(RedeemTime) = %s or year(RedeemTime) = %s and month(RedeemTime) = %s or month(RedeemTime) = %s  group by year, month,EID;",(y1,y2,m1,m2))
        result = cursor.fetchall()
        
        return render_template("Admin home.html",employee = employee, reset = reset, result = result, usernotgiveall=usernotgiveall,usage=usage)
    else:
        redirect(url_for('admin_login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('hello'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
