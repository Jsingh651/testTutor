from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app import app

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

db = "frontend_tutor"

class Payments:
    def __init__(self, data):
        self.payment_id = data['id']
        self.payment_intent_id = data['payment_intent_id']
        self.amount_paid = data['amount_paid']
        self.payment_created_at = data['created_at']
        self.user = None

        
