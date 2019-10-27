from flask import Flask
from flask import Blueprint, redirect, render_template, request, url_for, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("homepage.html")

@app.route('/table')
def showinfo():
    return render_template("table.html")