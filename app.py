from flask import Flask , render_template , redirect , url_for , request
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/users"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route('/')
def main():
    return redirect('/login')

@app.route("/login" , methods = ['GET', 'POST'])
def login():
    if (request.method == "POST"):
        email = request.form['email']
        password = request.form['password']
        userData = mongo.db.users.find_one({"email":email})
        if (bcrypt.check_password_hash(userData["password"] , password)):
            return redirect('home')
    return render_template('login.html')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if (request.method == "POST"):
        name = request.form['name']
        email =  request.form['email']
        password = request.form['password1']
        re_password = request.form['password2']
        if(password == re_password):
            hashPassword1 = bcrypt.generate_password_hash(password)
            mongo.db.users.insert_one({"name":name , "password" : hashPassword1 , "email":email})
            return render_template('login.html')
    return render_template('register.html')

@app.route("/home")
def home():
    return render_template('home.html')


if __name__=="__main__":
    app.run(debug=True , port=8000)



