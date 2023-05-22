from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app import app

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

db = "frontend_tutor"

class Video:
    def __init__(self, data):
        self.id = data['id']
        self.video_title = data['video_title']
        self.video_description = data['video_description']
        self.video_url = data['video_url']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM videos'
        results = connectToMySQL(db).query_db(query)
        return [cls(row) for row in results]

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM videos WHERE id = %(id)s;'
        result = connectToMySQL(db).query_db(query, data)
        return cls(result[0])
    



    