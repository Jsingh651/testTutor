
from flask_app import app
from flask import Flask, redirect, session, render_template, flash,request, Markup
from urllib.parse import quote
import os
from dotenv import load_dotenv
load_dotenv()
@app.template_filter()
def urlencode(value):
    return Markup(quote(value))
from flask_app.models.users import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def redirectroute():
    return render_template("landingPage.html")

@app.route('/login')
def newuser():
    return render_template('login.html')

@app.route("/register")
def newuseredit():
    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register():

    if not User.validate(request.form):
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        return redirect('/register')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'accepted': request.form['accepted'],
        'password': pw_hash
    }
    first_name = request.form['first_name']
    first_name.capitalize()
    id = User.register(data)
    session['user_id'] = id
    session['username'] = data['first_name']

    return redirect('/')

@app.route('/login/user', methods = ['POST'])
def login ():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/login')
    session['user_id'] = user_in_db.id
    return redirect ('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
