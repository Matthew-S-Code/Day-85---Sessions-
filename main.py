from flask import Flask, request, redirect, session
from replit import db
import random, os

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.environ['sessionKey']

@app.route("/")
def index():
    if session.get('loggedIn'):
        return redirect("/welcome")
    return """<p><a href="/signup">Sign Up</a> <br> <a href="/login">Log in</a> </p>"""

@app.route("/signup")
def signup():
    if session.get('loggedIn'):
        return redirect("/welcome")
    try:
        with open("signup.html", "r") as f:
            page = f.read()
    except FileNotFoundError:
        page = "<p>Signup page not found.</p>"
    return page

@app.route("/login")
def login():
    if session.get('loggedIn'):
        return redirect("/welcome")
    try:
        with open("login.html", "r") as f:
            page = f.read()
    except FileNotFoundError:
        page = "<p>Login page not found.</p>"
    return page

@app.route("/signup", methods=["POST"])
def create():
    if session.get('loggedIn'):
        return redirect("/welcome")
    form = request.form
    username = form["username"]
    name = form["name"]
    password = form["password"]

    if username not in db:
        salt = str(random.randint(1000, 9999))
        newPassword = hash(password + salt)
        db[username] = {"name": name, "password": newPassword, "salt": salt}
        return redirect("/login")  # ✅ No session set here
    else:
        return redirect("/signup")

@app.route("/login", methods=["POST"])
def logUser():
    if session.get('loggedIn'):
        return redirect("/welcome")
    form = request.form
    username = form["username"]
    password = form["password"]

    if username not in db:
        return redirect("/login")

    user = db[username]
    salt = user["salt"]
    hashedPass = hash(password + salt)

    if hashedPass == user["password"]:
        session["loggedIn"] = username  # ✅ Session set only after successful login
        return redirect("/welcome")
    else:
        return redirect("/login")

@app.route("/welcome")
def welcome():
    if not session.get('loggedIn'):
        return redirect("/")
    name = db[session['loggedIn']]['name']
    return f"""<h1>Hello there {name}</h1>
               <a href="/logout"><button>Logout</button></a>"""

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

app.run(host='0.0.0.0', port=81)
