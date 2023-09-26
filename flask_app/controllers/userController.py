import os
import json
import stripe
from urllib.parse import quote
from dotenv import load_dotenv
from flask_mail import Message
from flask_bcrypt import Bcrypt
from flask_app import app, mail
from flask_app.models.users import User
from itsdangerous import URLSafeTimedSerializer
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask import Flask, jsonify, request, flash, url_for, redirect, session, render_template, Markup, request
stripe.api_key = "sk_test_51NDup2FabksylCi8SFvbhtLIVxxBS1gZ3MUvH1lq9sKc8tjJgllKghz1gPVsm6rybRXsQ3kVdoIssPDdaDFii2AK00NH08t73i"
endpoint_secret = "whsec_Y45JYq90PtTMH3FPwVLcfE4v9xrK0vvo"
from datetime import datetime, timedelta

load_dotenv()
bcrypt = Bcrypt(app)

# stripe.api_key = "sk_test_51NDup2FabksylCi8SFvbhtLIVxxBS1gZ3MUvH1lq9sKc8tjJgllKghz1gPVsm6rybRXsQ3kVdoIssPDdaDFii2AK00NH08t73i"


@app.template_filter()
def urlencode(value):
    return Markup(quote(value))


# LOGIN PAGE
@app.route('/login')
def newuser():
    reset_success = session.pop('reset_success', None)
    return render_template('login.html', reset_success=reset_success)


# REGISTER PAGE
@app.route("/register")
def newuseredit():
    return render_template("register.html")


# DASHBOARD PAGE
@app.route("/")
def redirectroute():
    logged_in = 'user_id' in session
    first_name = None
    id = None
    is_paying = None
    user = None
    if logged_in:
        user_id = session['user_id']
        user = User.get_one({'id': user_id})
        if user:
            first_name = user.first_name[0].upper()
            id = user.id
            is_paying = user.is_paying
    return render_template("landingPage.html", logged_in=logged_in, first_name=first_name, id=id, user=user, is_paying = is_paying)


# PROFILE PAGE
@app.route("/profile/page/9090u343109uu43438041292409313/3243/prof/<int:id>")
def profilePage(id):
    if not session:
        return redirect("/")
    data = {'id': id}
    user = User.get_one(data)
    first_name = user.first_name[0].upper()
    reset_success = session.pop('reset_success', None)
    return render_template('profile.html', user=user, first_name=first_name, reset_success=reset_success, id=id)




# FORGOT PASSWORD PAGE
@app.route("/forgot/pass")
def forgotPassword():
    return render_template('forgotPass.html')


# UPDATE PASSWORD PAGE
@app.route('/new/password/<token>', methods=['GET', 'POST'])
def newPassword(token):
    try:
        ts = URLSafeTimedSerializer(app.secret_key)
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        flash('The password reset link is invalid or has expired.', 'warning')
        return redirect(url_for('forgotPassword'))

    if request.method == 'POST':
        password = request.form.get('password')
        pw_hash = bcrypt.generate_password_hash(password)
        data = {'email': email, 'password': pw_hash}
        User.update_password(data)

        flash('Your password has been updated!', 'success')
        return redirect('/')
    else:
        return render_template('newpassword.html', token=token)


# PRICING PAGE
@app.route("/pricing/<int:id>")
def pricing(id):
    if not session:
        return redirect('/')
    data = {'id': id}
    user = User.get_one(data)
    first_name = user.first_name[0].upper()
    return render_template("pricing.html", user=user, first_name=first_name)


@app.route("/update/email", methods=['POST'])
def updateEmail():
    id = request.form['id']
    User.updateEmail(request.form)
    return redirect('/profile/page/9090u343109uu43438041292409313/3243/prof/'+id)


@app.route("/update/name", methods=['POST'])
def updateName():
    id = request.form['id']
    data = {"id": id, "first_name": request.form['first_name']}
    User.updatename(data)
    return redirect('/profile/page/9090u343109uu43438041292409313/3243/prof/'+id)


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
        ts = URLSafeTimedSerializer(app.secret_key)
        token = ts.dumps(email, salt='recover-key')
        reset_link = url_for('newPassword', token=token, _external=True)
        html = render_template('reset_email.html', reset_link=reset_link)
        msg = Message('Password Reset Request', sender='noreply@domain', recipients=[email])
        msg.html = html
        mail.send(msg)
        session['reset_success'] = True
    else:
        session['reset_success'] = False
    return redirect('/login')


@app.route("/forgot/password", methods=['POST'])
def forgotPasswordForm():
    if not User.validateEmail(request.form):
        session['email'] = request.form['email']
        print()
        id = request.form['id']
        return redirect('/profile/page/9090u343109uu43438041292409313/3243/prof/' + id)
    data = {"email": request.form["email"]}
    user = User.get_by_email(data)
    email = request.form['email']
    id = request.form['id']
    if user:
        ts = URLSafeTimedSerializer(app.secret_key)
        token = ts.dumps(email, salt='recover-key')
        reset_link = url_for('newPassword', token=token, _external=True)
        html_content = render_template(
            'reset_email.html', reset_link=reset_link)
        msg = Message('Password Reset Request',sender='noreply@domain', recipients=[email])
        msg.html = html_content
        mail.send(msg)
        session['reset_success'] = True
    else:
        session['reset_success'] = False
    return redirect('/profile/page/9090u343109uu43438041292409313/3243/prof/' + id)


@app.route('/create-customer', methods=['POST'])
def create_customer():
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
    customer = stripe.Customer.create(email=data['email'])

    data['stripe_customer_id'] = customer.id

    id = User.register(data)

    session['user_id'] = id
    session['username'] = data['first_name']

    resp = redirect('/')
    resp.set_cookie('customer', customer.id)
    customer_id = request.cookies.get('customer')
    print("THIS IS THE CUSTOMER ID", customer_id)
    return resp



@app.route('/webhook', methods=['POST'], provide_automatic_options=False)
def webhook():
    stripe.api_key = "sk_test_51NDup2FabksylCi8SFvbhtLIVxxBS1gZ3MUvH1lq9sKc8tjJgllKghz1gPVsm6rybRXsQ3kVdoIssPDdaDFii2AK00NH08t73i"
    endpoint_secret = "whsec_Y45JYq90PtTMH3FPwVLcfE4v9xrK0vvo"
    event = None
    payload = request.get_data(as_text=True)
    print("THIS IS THE PAYLOAD", payload)

    try:
        event = json.loads(payload)
    except:
        print('⚠️  Webhook error while parsing basic request.' + str(e))
        return jsonify(success=False)
    if endpoint_secret:
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError as e:
            print('⚠️  Webhook signature verification failed.' + str(e))
            return jsonify(success=False)

    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        payment_intent_id = payment_intent['id']
        stripe_customer_id = payment_intent['customer']
        amount_paid = payment_intent['amount']
        print('Payment for {} succeeded'.format(amount_paid))
        print('Payment Intent ID: {}'.format(payment_intent_id))
        print('Customer user ID: {}'.format(stripe_customer_id))
        data = {'stripe_customer_id': stripe_customer_id,
                "amount_paid": amount_paid, "is_paying": True}
        User.save(data)

    if event and event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session['id']
        customer_id = session['customer']
        amount_total = session['amount_total']
        selected_product = session['metadata'].get('selected_product')

        print('Payment for {} succeeded'.format(amount_total))
        print('Checkout Session ID: {}'.format(session_id))
        print('Customer user ID: {}'.format(customer_id))
        print('Selected Product: {}'.format(selected_product))

        data = {'stripe_customer_id': customer_id,
                "plan_type": selected_product}
        User.saveSubscription(data)


    if event and event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        customer_id = subscription['customer']
        new_plan_type = subscription['items']['data'][0]['plan']['id']
        cancel_at = subscription['cancel_at']

        if cancel_at:
            cancellation_date = datetime.fromtimestamp(cancel_at)
            data = {'stripe_customer_id': customer_id, "plan_type": new_plan_type, "subscription_expires_at": cancellation_date}
            User.saveSubscription(data)
        else:
            data = {'stripe_customer_id': customer_id, "plan_type": new_plan_type, "subscription_expires_at": None}
            User.saveSubscription(data)
    #     # return redirect("/success")

    # elif event['type'] == 'payment_method.attached':
    #     payment_method = event['data']['object']
    else:
        print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)


@app.route('/create-customer-portal-session', methods=['POST'])
def customer_portal():
    # Authenticate your user.
    stripe_customer_id = request.form['stripe_customer_id']
    session = stripe.billing_portal.Session.create(
        customer=stripe_customer_id,
        return_url='http://www.frontendtutor.com',
    )
    return redirect(session.url)


