from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.event import Event

@app.route ('/event/new')
def create():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('create.html')


@app.route ('/event/create', methods = ['POST'])
def user_create():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Event.validate_register(request.form):
        return redirect ('/event/new')


    create_data={
        'event_name': request.form ['event_name'],
        'description': request.form ['description'],
        'member_num': request.form['member_num'],
        'location': request.form['location'],
        'date': request.form['date'],
        'users_id': session['user_id']
    }
    event_id = Event.create(create_data)

    add_member_data = {
        "events_id": event_id,
        "users_id": session['user_id']
    }

    Event.add_memeber(add_member_data)

    return redirect ('/dashboard')

@app.route('/event/destroy/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': id
    }
    Event.destroy(data)
    return redirect('/dashboard')

@app.route('/event/details/<int:id>')
def event_details(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': id
    }
    return render_template ('event_details.html', event=Event.get_one(data))

@app.route('/event/edit/<int:id>')
def update(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id': id
    }
    
    return render_template ('edit.html', event=Event.get_one(data))

@app.route('/event/join/<int:id>')
def join_event(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "events_id": id,
        "users_id": session["user_id"]
    }
    Event.add_memeber(data)
    return redirect('/event/bulletin')

@app.route('/event/leave/<int:id>')
def leave_event(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "events_id": id,
        "users_id": session["user_id"]
    }
    Event.remove_member(data)
    return redirect('/event/bulletin')

@app.route('/event/update/<int:id>', methods=['POST'])
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Event.validate_register(request.form):
        return redirect (f'/event/edit/{id}')
    data={
        'id': id,
        'event_name': request.form ['event_name'],
        'description': request.form ['description'],
        'member_num': request.form['member_num'],
        'location': request.form['location'],
        'date': request.form['date']
    }
    Event.update(data)
    return redirect ('/dashboard')

@app.route('/event/bulletin')
def event_bulletin():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session["user_id"]
    }
    return render_template('bulletin.html', events=Event.get_users_and_events(data), logged_in_user=User.get_joined_events_id(data))