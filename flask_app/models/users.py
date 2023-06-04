from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app import app
from datetime import datetime, timedelta

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

db = "frontend_tutor"

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.subscription_expires_at = data['subscription_expires_at']
        # self.payment_intent_id = data['payment_intent_id']
        self.stripe_customer_id = data['stripe_customer_id']
        self.amount_paid = data['amount_paid']
        self.plan_type = data['plan_type']
        self.is_paying = data['is_paying']
        

    @classmethod
    def save(cls, data):
        query = """
        UPDATE users
        SET is_paying = %(is_paying)s, amount_paid = %(amount_paid)s
        WHERE stripe_customer_id = %(stripe_customer_id)s
        """
        
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def saveSubscription(cls, data):
        query = """
        UPDATE users
        SET plan_type = %(plan_type)s, subscription_expires_at = %(subscription_expires_at)s
        WHERE stripe_customer_id = %(stripe_customer_id)s
        """
        
        return connectToMySQL(db).query_db(query, data)

    def update_is_paying(self):
        current_datetime = datetime.now()
        expiration_datetime = self.subscription_expires_at
        if current_datetime >= expiration_datetime:
            self.is_paying = False
            self.amount_paid = None
            self.plan_type = None
            data = {
                'is_paying': self.is_paying,
                "amount_paid": self.amount_paid,
                "plan_type": self.plan_type,
                'stripe_customer_id': self.stripe_customer_id
            }
            self.save(data)



    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users'
        results = connectToMySQL(db).query_db(query)
        return [cls(row) for row in results]
    

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL(db).query_db(query, data)
        return cls(result[0])
    


    @classmethod
    def register(cls, data):
        query = '''
        INSERT INTO users
        (first_name, last_name, email, password,stripe_customer_id, created_at) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s,%(stripe_customer_id)s,  NOW());
        '''
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def updateEmail(cls, data):
        query = 'UPDATE users SET email = %(email)s'
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def updatename(cls, data):
        query = 'UPDATE users SET first_name = %(first_name)s'
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def update_password(cls,data):
        query = 'UPDATE users SET password = %(password)s WHERE email = %(email)s'
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def stripe_customer_id(cls,data):
        query = "UPDATE users SET stripe_customer_id = %()s WHERE id = %()s"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE from users WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @staticmethod
    def validateEmail(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "email_error_forgot")
            is_valid = False
        return is_valid

    @staticmethod
    def validate(user):
        is_valid = True
        if User.get_by_email({"email": user['email']}):
            flash('Email already exists', 'exsist')
            is_valid = False

        if len(user['first_name']) < 3:
            flash("First Name must be at least 3 characters.", 'first_name_error')
            is_valid = False

        if len(user['last_name']) < 3:
            flash("Last Name must be at least 3 characters.", "last_name_error")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "email_error")
            is_valid = False

        if len(user['password']) < 8:
            flash('Password must be at least 8 characters', "password_error")
            is_valid = False
        return is_valid
    



