from flask import Flask
from flask import  request,render_template
app = Flask(__name__, template_folder='templates') 

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup/" )
def signup():
    return render_template("signup.html") 
@app.route("/signin/" )
def signin():
    return render_template("signin.html")


app.run(host="0.0.0.0",port=8000,debug=True)
