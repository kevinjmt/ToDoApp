import this

import pymongo
from bson import ObjectId
from flask import Flask, render_template, request, url_for, redirect, session
import bcrypt
# from todo.todo import todo_bp

app = Flask(__name__)
app.secret_key = "testing"
# app.register_blueprint(todo_bp, url_prefix='/todolist')

# default mongodb configuration - Remote database
# change remote database if needed, else : localhost
client = pymongo.MongoClient("mongodb+srv://kevin:kevin18@cluster0.ssitjv2.mongodb.net/?retryWrites=true&w=majority")
db = client.test

# database:
db = client.flask_db

# -> Collections:
# for ToDoApp
todos = db.todos
# for Authentication
records = db.register


# @app.route is needed to load a page
# View for indexpage
# url : /
@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    # check email -> check if user is authenticated in the current session
    if "email" not in session:
        # if user is not authenticated, redirect it to the login page
        return redirect(url_for("login"))
    # else redirect it to the main page (index)
    # render the main page
    return render_template('index.html')



# View for indexpage
# url : /register
@app.route("/register/", methods=['post', 'get'])
def register():
    message = ''
    # check email -> check if user is authenticated in the current session
    if "email" in session:
        # if user is authenticated, redirect it to the logged_in page to inform th user
        return redirect(url_for("logged_in"))
    # if the register form has been sent save item
    if request.method == "POST":
        # saving user fields into variables
        user = request.form.get("fullname")
        email = request.form.get("email")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        # if user already exists (if another user has same name, email and password in the MongoDB Database)
        # or email, or password differences are already linked to a user
        #   -> send an error message in the html page
        if user_found:
            message = 'There already is a user by that name'
            return render_template('register.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('register.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('register.html', message=message)
        else:
            # if not -> save the new user into a variable user_input (with hashed password)
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            # insert the new user in the DB
            records.insert_one(user_input)

            user_data = records.find_one({"email": email})
            new_email = user_data['email']

            # return the new user in the DB
            return render_template('logged_in.html', email=new_email)
    # render template for the register page
    return render_template('register.html')


@app.route('/about/')
def about():
    message = ''
    # check email -> check if user is authenticated in the current session
    if "email" not in session:
        # if not -> redirect the user to the main page
        return redirect(url_for("login"))
    # else -> render the page about
    return render_template('about.html')


@app.route("/login/", methods=["POST", "GET"])
def login():
    # insert a message in the HTML file using "message" variable
    message = 'Please login to your account'
    # check email -> check if user is authenticated in the current session
    if "email" in session:
        # if authenticated (already logged in) -> redirect to the logged_in page
        return redirect(url_for("logged_in"))

    # the form is filled and have been posted
    if request.method == "POST":
        # saving form fields into variables
        email = request.form.get("email")
        password = request.form.get("password")
        email_found = records.find_one({"email": email})
        # if an email has been filled (check if he filled the blanks)
        if email_found:
            # save text inputs into variables to check if the user has his IDs
            email_val = email_found['email']
            passwordcheck = email_found['password']

            # encode the password and send it to the db to check if it's correct
            # (using checkpw method -> password entered encoded == password from db ? -> redirect to the logged_in page)
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                # save current session to do not have to log in again
                session["email"] = email_val
                # redirect to the logged_in page
                return redirect(url_for('logged_in'))
            else:
                # if there is an email in the current session -> redirect to the logged_in page
                if "email" in session:
                    return redirect(url_for("logged_in"))
                # if not -> the user has entered the wrong password
                message = 'Wrong password'
                # redirect to the login_page
                return render_template('login.html', message=message)
        else:
            # if not email found -> wrong email or input not filled
            message = 'Email not found'
            # in this case -> redirect to login page
            return render_template('login.html', message=message)
    # render the login page
    return render_template('login.html', message=message)


@app.route('/logged_in/')
def logged_in():
    # check email -> check if user is authenticated in the current session
    if "email" in session:
        # email saved using the one in session (previously described)
        email = session["email"]
        # display it in the logged_in page
        return render_template('logged_in.html', email=email)
    else:
        # if not authenticated -> redirect to the login page
        return redirect(url_for("login"))


@app.route("/logout/", methods=["POST", "GET"])
def logout():
    # check email -> check if user is authenticated in the current session
    if "email" in session:
        # delete email of current session
        session.pop("email", None)
        # render the signout page (to show the user that he is logged out)
        return render_template("sign_out.html")
    else:
        # render the main page if authenticated
        return render_template('index.html')


@app.route('/todolist/', methods=('GET', 'POST'))
def todolist():
    message = ''
    # check email -> check if user is authenticated in the current session
    if "email" not in session:
        # redirect to the login page if not authenticated
        return redirect(url_for("login"))

    if request.method == 'POST':
        # save input fields into variables
        content = request.form['content']
        date = request.form['date']
        description = request.form['description']
        phone_number = request.form['phone_number']
        maps = request.form['maps']
        degree = request.form['degree']
        # insert it into the db
        todos.insert_one({'content': content, 'date': date, 'degree': degree, 'description': description, 'phone_number': phone_number, 'maps': maps})
        # redirect to the todo page
        return redirect(url_for('todolist'))
    # get all todos from db
    all_todos = todos.find()
    # then send the list into the html page (rendered here)
    return render_template('todolist.html', todos=all_todos)



@app.route('/<id>/edit', methods=('GET', 'POST'))
def edit(id):
    message = ''
    # check email -> check if user is authenticated in the current session
    if "email" not in session:
        # if not autenticated -> redirect to the login page
        return redirect(url_for("login"))
    # get element from the form and save it into variables
    if request.method == 'POST':

        content = request.form['content']
        date = request.form['date']
        description = request.form['description']
        phone_number = request.form['phone_number']
        maps = request.form['maps']
        degree = request.form['degree']
        # send data to the db
        todos.replace_one({"_id": ObjectId(id)}, {'content': content, 'date': date, 'degree': degree, 'description': description, 'phone_number': phone_number, 'maps': maps})
        # redirect to the todolist page
        return redirect(url_for('todolist'))
    # to edit the object -> send it to the html page
    to_edit = todos.find_one({"_id": ObjectId(id)})
    # return to the edit page
    return render_template('edit.html', todo=to_edit)


@app.post('/<id>/delete')
def delete(id):
    # delete method in the todos list
    todos.delete_one({"_id": ObjectId(id)})
    # redirect to the main page when finished deletion
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
