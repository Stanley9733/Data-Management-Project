from flask import Flask
from flask import Blueprint, redirect, render_template, request, url_for, jsonify
app = Flask(__name__)
app.debug = True

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