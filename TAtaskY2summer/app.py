from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase
import random



config = {
  "apiKey" : "AIzaSyBp0_hJrQwYrT3e2OR25ubJ83LM-7h5a5g",
  "authDomain" : "y2-ta-task-summer.firebaseapp.com",
  "projectId" : "y2-ta-task-summer",
  "storageBucket" : "y2-ta-task-summer.appspot.com",
  "messagingSenderId" : "180376131421",
  "appId" : "1:180376131421:web:02d8903be68f8b68f13ab4",
  "measurementId" : "G-9G60MLL087",
  "databaseURL" : "https://y2-ta-task-summer-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__)
app.config['SECRET_KEY'] = "best-key-ever!"


############## home page #############
@app.route("/", methods=['GET', 'POST'])
def home():
  error = ""
  name = "Welcome!"
  if "user" in login_session:
    # name = db.child("Users").child(login_session["user"]["localId"]).get().val()
    # name = name["email"]
    if request.method == 'POST':
      photo = request.form['photo']
    try:
      db.child("Photos").child(login_session["user"]["localId"]).push(photo)
    except:
      error = "failed to add photo"
  return render_template("home.html", name=name)



############### signup #############
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  error = ""
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    try:
      login_session['user'] = auth.create_user_with_email_and_password(email, password)
      return redirect(url_for('signin'))
    except:
      error = "Authentication failed"
      
  return render_template("signup.html")



############# signin ##########
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  error = ""
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    try:
      login_session['user'] = auth.sign_in_with_email_and_password(email, password)
      return redirect(url_for('home'))
    except:
      error = "Authentication failed"

  return render_template("signin.html")



########## profile ##########
@app.route('/profile', methods=['GET', 'POST'])
def profile():
  if "user" in login_session:
  # get photos from the database
    photos = db.child("Photos").child(login_session["user"]["localId"]).get().val()
    if photos != None:
        length = len(photos)
        return render_template("profile.html", photos = photos, length = length)
  else:
    return redirect(url_for("home"))
  return render_template("profile.html", photos = photos)


############ signout ############
@app.route('/signout')
def signout():
  login_session['user'] = None
  auth.current_user = None
  return redirect(url_for('home'))




if __name__ == '__main__':
  app.run(debug=True)