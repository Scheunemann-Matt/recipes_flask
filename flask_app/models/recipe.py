# import the function that will return an instance of a connection
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'(?=.*\d)(?=.*[A-Za-z])')
# model the class after the recipes table from our database
class Recipe:
    DB_NAME = "recipes_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.under30 = data['under30']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB_NAME).query_db(query)

        recipes = []
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes

    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM recipes WHERE recipes.id = %(id)s"
        results = connectToMySQL(cls.DB_NAME).query_db(query, id)
        if (not results):
            return False
        recipe = cls(results[0])
        return recipe

    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (title, under30, description, instructions, date_made, user_id, created_at, updated_at) VALUES (%(title)s, %(under30)s, %(description)s, %(instructions)s, %(date_made)s, %(user_id)s, NOW(), NOW())"

        return connectToMySQL(cls.DB_NAME).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET title = %(title)s, under30 = %(under30)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, updated_at = NOW() WHERE recipes.id = %(id)s"

        return connectToMySQL(cls.DB_NAME).query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s"

        return connectToMySQL(cls.DB_NAME).query_db(query, id)

    @classmethod
    def validate_recipe(cls, data):
        is_valid = True

        if (len(data['title']) < 3):
            is_valid = False
            flash("Title must be at least 3 characters")
        if (len(data['description']) < 3):
            is_valid = False
            flash("Description must be at least 3 characters")
        if (len(data['instructions']) < 3):
            is_valid = False
            flash("Instructions must be at least 3 characters")
        if (data['date_made'] == ''):
            is_valid = False
            flash("Please select a date")
        if ("under30" not in data):
            is_valid = False
            flash("Please select if the recipe takes under 30 minutes to make.")

        return is_valid