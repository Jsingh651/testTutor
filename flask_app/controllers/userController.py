
from itsdangerous import URLSafeTimedSerializer
from flask_app.models.users import User
from flask import request, flash, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_bcrypt import Bcrypt
from flask_app import app
from flask import Flask, redirect, session, render_template, flash, request, Markup
from urllib.parse import quote
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os
from flask_app import mail
from dotenv import load_dotenv
load_dotenv()


@app.template_filter()
def urlencode(value):
    return Markup(quote(value))


bcrypt = Bcrypt(app)


@app.route("/")
def redirectroute():
    logged_in = 'user_id' in session
    first_name = None
    id = None
    if logged_in:
        user_id = session['user_id']
        user = User.get_one({'id': user_id})
        if user:
            first_name = user.first_name[0].upper()
            id = user.id

    return render_template("landingPage.html", logged_in=logged_in, first_name=first_name, id=id)


@app.route("/forgot/pass")
def forgotPassword():
    return render_template('forgotPass.html')


@app.route("/forgot/password", methods=['POST'])
def forgotPasswordForm():
    if not User.validateEmail(request.form):
        session['email'] = request.form['email']
        id = request.form['id']
        return redirect('/profile/page/9090u343109uu43438041292409313/3243/prof/' + id)

    data = {"email": request.form["email"]}
    user = User.get_by_email(data)
    email = request.form['email']
    id = request.form['id']

    if user:
        # Create a token
        ts = URLSafeTimedSerializer(app.secret_key)
        token = ts.dumps(email, salt='recover-key')

        # Create a reset email
        msg = Message('Password Reset Request',
                      sender='noreply@domain', recipients=[email])
        msg.body = f'''To reset your password, visit the following link: {url_for('newPassword', token=token, _external=True)}'''
        mail.send(msg)

        session['reset_success'] = True  # Store the success state in session
    else:
        session['reset_success'] = False  # Store the failure state in session

    return redirect('/profile/page/9090u343109uu43438041292409313/3243/prof/' + id)


@app.route('/new/password/<token>', methods=['GET', 'POST'])
def newPassword(token):
    try:
        # Confirm the token
        ts = URLSafeTimedSerializer(app.secret_key)
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        flash('The password reset link is invalid or has expired.', 'warning')
        return redirect(url_for('forgotPassword'))

    if request.method == 'POST':
        password = request.form.get('password')  # Get password from form
        pw_hash = bcrypt.generate_password_hash(password)
        data = {'email': email, 'password': pw_hash}
        # Call the class method to update the password
        User.update_password(data)

        flash('Your password has been updated!', 'success')
        # Redirect to login page after password reset
        return redirect('/')
    else:
        return render_template('newpassword.html', token=token)


@app.route("/profile/page/9090u343109uu43438041292409313/3243/prof/<int:id>")
def profilePage(id):
    data = {'id': id}
    user = User.get_one(data)
    first_name = user.first_name[0].upper()

    # Retrieve and remove the reset_success state from session
    reset_success = session.pop('reset_success', None)

    return render_template('profile.html', user=user, first_name=first_name, reset_success=reset_success, id=id)


@app.route("/update/email", methods=['POST'])
def updateEmail():
    id = request.form['id']
    User.updateEmail(request.form)
    return redirect('/profile/page/9090u343109uu43438041292409313/3243/prof/'+id)


@app.route("/update/name", methods=['POST'])
def updateName():
    id = request.form['id']
    User.updatename(request.form)
    return redirect('/profile/page/9090u343109uu43438041292409313/3243/prof/'+id)


@app.route('/login')
def newuser():
    # Retrieve and remove the reset_success state from session
    reset_success = session.pop('reset_success', None)
    return render_template('login.html', reset_success=reset_success)


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
        'password': pw_hash
    }
    first_name = request.form['first_name']
    first_name.capitalize()
    id = User.register(data)
    session['user_id'] = id
    session['username'] = data['first_name']

    return redirect('/')


@app.route('/login/user', methods=['POST'])
def login():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/login')
    session['user_id'] = user_in_db.id
    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route("/forgot/password/form", methods=['POST'])
def forgotPasswordFormlogin():
    if not User.validateEmail(request.form):
        session['email'] = request.form['email']
        return redirect('/forgot/pass')

    data = {"email": request.form["email"]}
    user = User.get_by_email(data)
    email = request.form['email']

    if user:
        # Create a token
        ts = URLSafeTimedSerializer(app.secret_key)
        token = ts.dumps(email, salt='recover-key')

        # Create a reset email
        msg = Message('Password Reset Request', sender='noreply@domain', recipients=[email])
        msg.body = f'''To reset your password, visit the following link: {url_for('newPassword', token=token, _external=True)}'''
        mail.send(msg)

        session['reset_success'] = True  # Store the success state in session
    else:
        session['reset_success'] = False  # Store the failure state in session

    return redirect('/forgot/pass')
