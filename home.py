from flask import Flask
from flask import Blueprint, redirect, render_template, request, url_for, jsonify
app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        name = data['username']
        return redirect('/table/{}'.format(name))
    return render_template("homepage.html")

@app.route('/table/<id>')
def showinfo(id):
    showname = id
    return render_template("Employee home.html", showname = showname)