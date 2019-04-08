from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL      # import the function that will return an instance of a connection
app = Flask(__name__)

#Home Page
@app.route("/users")
def users():
    mysql = connectToMySQL('user_data')
    friends = mysql.query_db('SELECT * FROM friends;')
    print('*'*80)
    print(friends)
    return render_template("index.html", all_friends = friends)

#Opens New User Page
@app.route("/users/new")
def new_user():
    return render_template("new.html")

#Submits New User into Database
@app.route("/users/add_data", methods=["POST"])
def add_data():
    mysql = connectToMySQL('user_data')
    query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES(%(fn)s, %(ln)s, %(email)s, NOW(), NOW());"
    data = {
        "fn": request.form["user_first"],
        "ln": request.form["user_last"],
        "email": request.form["user_email"]
    }
    new_friends = mysql.query_db(query, data)
    print('*'*80)
    print('New friend added')
    return redirect("/users")

#Opens User Info Page
@app.route("/users/<id>")
def user_page(id):
    num = id
    mysql = connectToMySQL('user_data')
    friends = mysql.query_db(f'SELECT * FROM friends WHERE id ="{num}";')
    print('*'*80)
    print(f"Collected {num}'s info")
    return render_template("/userpage.html", all_friends = friends, idnum = num)

#Opens Edit User Page
@app.route("/users/<id>/edit")
def edit_user(id):
    num = id
    mysql = connectToMySQL('user_data')
    friends = mysql.query_db(f'SELECT * FROM friends WHERE id ="{num}";')
    print('*'*80)
    print(f"On {num}'s edit page")
    return render_template("edit.html", all_friends = friends, idnum = num)

#Submits Updates on User
@app.route("/users/update_data/<id>", methods=["POST"])
def update_data(id):
    num = id
    mysql = connectToMySQL('user_data')
    query = f"UPDATE friends SET first_name = %(fn)s, last_name = %(ln)s, email = %(email)s, updated_at = NOW() WHERE id = {num};"
    data = {
        "fn": request.form["user_first"],
        "ln": request.form["user_last"],
        "email": request.form["user_email"]
    }
    edit_friends = mysql.query_db(query, data)
    print('*'*80)
    print(f"{num}'s info has been updated")
    return redirect(f"/users/{num}")

#Destroys User
@app.route("/users/<id>/destroy")
def destroy_user(id):
    num = id
    mysql = connectToMySQL('user_data')
    query = f"DELETE FROM friends WHERE id = {num}"
    destroy_friends = mysql.query_db(query)
    print('*'*80)
    print(f"Friend #{num} has been destroyed")
    return redirect(f"/users")


if __name__ == "__main__":
    app.run(debug=True)