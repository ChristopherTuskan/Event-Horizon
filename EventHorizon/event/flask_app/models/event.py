from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

DB = "event_schema"

class Event:
    def __init__(self,data):
        self.id = data['id']
        self.event_name = data['event_name']
        self.location = data['location']
        self.date = data['date']
        self.description = data['description']
        self.member_num = data['member_num']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.joined_users = []

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO 
                events 
                    (event_name, 
                    location, 
                    date, 
                    description, 
                    member_num,
                    users_id) 
            VALUES 
                (%(event_name)s, 
                %(location)s,
                %(date)s,
                %(description)s, 
                %(member_num)s,
                %(users_id)s);
            """
        results = connectToMySQL(DB).query_db(query, data)
        return results

    @classmethod
    def get_users_and_events(cls, data):
        query = "SELECT * FROM events JOIN users ON users.id = events.users_id WHERE users_id != %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        all_events = []
        for event in results:
            one_event = cls(event)
            user_data ={
                'id':event['users.id'], 
                'first_name':event['first_name'],
                'last_name':event['last_name'],
                'email':event['email'],
                'password':None,
                'created_at': event['users.created_at'],
                'updated_at':event['users.updated_at']
            }
            user_obj = user.User(user_data)
            one_event.creator = user_obj
            all_events.append(one_event)
        return all_events

    @classmethod
    def destroy (cls, data):
        query0 = "DELETE FROM events_users WHERE events_id = %(id)s;"
        connectToMySQL(DB).query_db(query0, data)

        query = "DELETE FROM events WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    

    @classmethod
    def get_event_with_users( cls, data ):
        query = """
            SELECT *
            FROM
                events
            LEFT JOIN
                events_users
            ON
                events_users.events_id = events.id
            LEFT JOIN
                users
            ON
                events_users.users_id = users.id
            WHERE
                events.id = %(id)s;
            """
        results = connectToMySQL(DB).query_db( query, data )
        event = cls (results [0])
        for result in results:
            one_user_data={
                'id':result['users.id'],
                'first_name':result['first_name'],
                'last_name':result['last_name'],
                'email':result['email'],
                'password': None,
                'created_at':result['users.created_at'],
                'updated_at':result['users.updated_at']
            }
            event.joined_users.append( user.User( one_user_data ))
        return event
    
    @classmethod
    def get_description (cls, data):
        query = "SELECT * FROM events JOIN users on users.id = events.user_id WHERE events.id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)

        row = cls (result[0])

        one_user_data={
            'id':result[0]['users.id'],
            'first_name':result[0]['first_name'],
            'last_name':result[0]['last_name'],
            'email':result[0]['email'],
            'password': None,
            'created_at':result[0]['users.created_at'],
            'updated_at':result[0]['users.updated_at']
        }
        user_obj=user.User(one_user_data)
        row.creator = user_obj
        return row

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM events WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = """
            UPDATE 
                events 
            SET 
                event_name=%(event_name)s,
                location=%(location)s,
                date = %(date)s,
                description=%(description)s,
                member_num=%(member_num)s 
            WHERE 
                id = %(id)s;
            """
        return connectToMySQL(DB).query_db(query,data)

    @classmethod
    def add_memeber(cls,data):
        query = "INSERT INTO events_users (events_id, users_id) VALUES (%(events_id)s, %(users_id)s);"
        member_id = connectToMySQL(DB).query_db(query, data)
        return member_id

    @classmethod
    def remove_member(cls,data):
        query = "DELETE FROM events_users WHERE users_id = %(users_id)s AND events_id = %(events_id)s;"
        return connectToMySQL(DB).query_db(query, data)


    @staticmethod
    def validate_register(tv):
        is_valid = True # we assume this is true

        if len(tv['event_name']) < 3:
            flash("Event Name must be at least 2 characters")
            is_valid= False

        if len(tv['location']) == 0:
            flash("Event Location required")
            is_valid= False

        if len(tv['date']) == 0:
            flash("Event Date required")
            is_valid= False    
                    
        if len(tv['description']) < 3:
            flash("Description must be at least 3 characters")
            is_valid= False

        if len(tv['member_num']) == 0:
            flash("Max Members need to be at least 1")
            is_valid= False

        return is_valid