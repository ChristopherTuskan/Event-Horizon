from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models import event

class User:
    db = "event_schema"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.joined_events = []
        self.name = self.first_name + " " + self.last_name

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching email
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_user_with_events( cls, data ):
        query ="""
            SELECT * FROM users
            LEFT JOIN events_users ON events_users.users_id = users.id
            LEFT JOIN events ON events_users.events_id = events.id
            WHERE users.id = %(id)s;
            """
        results = connectToMySQL(cls.db).query_db( query, data )
        user = cls (results [0])
        for result in results:
            event_data = {
                "id": result["events.id"],
                # "event_name": result["event_name"],
                # "location": result["location"],
                # "date": result["date"],
                # "description": result["description"],
                # "member_num": result["member_num"],
                # "created_at": result["created_at"],
                # "updated_at": result["updated_at"]
            }
            
            user_data = {
                "id": result["events.users_id"]
            }

            if event_data == {'id': None}:

                return
             

            user_event = event.Event.get_one(event_data)
            user_event.creator = User.get_by_id(user_data)
            user.joined_events.append(user_event)
        return user

    @classmethod
    def get_joined_events_id( cls, data ):
        query ="""
            SELECT * FROM users
            LEFT JOIN events_users ON events_users.users_id = users.id
            LEFT JOIN events ON events_users.events_id = events.id
            WHERE users.id = %(id)s;
            """
        results = connectToMySQL(cls.db).query_db( query, data )
        user = cls (results [0])
        for result in results:
            user.joined_events.append(result["events.id"])
        return user

    # Static methods don't have self or cls passed into the parameters.
    # We do need to take in a parameter to represent our user
    @staticmethod
    def validate_register(user):
        is_valid = True # we assume this is true
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email","register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
        return is_valid

