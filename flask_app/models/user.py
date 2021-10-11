# import the function that will return an instance of a connection
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'(?=.*\d)(?=.*[A-Z])')
# model the class after the users table from our database
class User:
    DB_NAME = "recipes_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB_NAME).query_db(query)

        users = []
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM users WHERE users.id = %(id)s"
        results = connectToMySQL(cls.DB_NAME).query_db(query, id)

        user = cls(results[0])
        if (not user):
            return False
        return user

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"

        return connectToMySQL(cls.DB_NAME).query_db(query, data)

    @classmethod
    def validate_email(cls, email):
        is_valid = True
        if (not EMAIL_REGEX.match(email)):
            is_valid = False

        return is_valid

    @classmethod
    def validate_user(cls, data):
        is_valid = True
        email_test_query = "SELECT * FROM users WHERE email = %(email)s"
        if (not cls.validate_email(data['email'])):
            flash("Please use a valid email")
            is_valid = False
        elif (connectToMySQL(cls.DB_NAME).query_db(email_test_query, data)):
            flash("That email has already been registered.")
            is_valid = False
        if (len(data['first_name']) < 2 or not data['first_name'].isalpha()):
            flash("First name must be at least 2 characters and not contain any numbers")
            is_valid = False
        if (len(data['last_name']) < 2 or not data['last_name'].isalpha()):
            flash("Last name must be at least 2 characters and not contain any numbers")
            is_valid = False
        if (len(data['password']) < 8 or not PASSWORD_REGEX.match(data['password'])):
            flash("Password must be at least 8 characters, contain at least one number, and at least one letter")
            is_valid = False
        if (data['password'] != data['confirm_password']):
            flash("Confirm Password does not match.")
            is_valid = False
        
        return is_valid

    @classmethod
    def get_one_from_email(cls, data):
        email_test_query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL(cls.DB_NAME).query_db(email_test_query, data)
        if (len(result) < 1):
            return False
        return result[0]