import os
from flask import Flask
app = Flask(__name__)
from flask_mail import Mail
app.secret_key = 'helefvefvr4332432lo'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'jangsing02@gmail.com'
app.config['MAIL_PASSWORD'] = 'cyhebbsqvohzqdjo'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
mail = Mail(app)

