from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.event import Event
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) # we are creating an object called bcrypt, 
# which is made by invoking the function Bcrypt with our app as an argument

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():
    # if there are errors:
    # We call the staticmethod on user model to validate
    if not User.validate_register(request.form):
        # redirect to the route where the user form is rendered.
        return redirect('/')
    # else no errors:
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    print(id)
    # store user id into session
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    # see if the username provided exists in the database
    user = User.get_by_email(request.form)
    # user is not registered in the db
    if not user:
        # if we get False after checking the email
        flash("Invalid Email or Password","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email or Password","login")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user.id
    # never render on a post!!!
    return redirect('/dashboard')

@app.route('/user/details/<int:id>')
def user_details(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    return render_template("user_details.html", user=User.get_by_id(data), all_user=User.get_user_with_events(data))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }

    return render_template("dashboard.html",user=User.get_user_with_events(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

