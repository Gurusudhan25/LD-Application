from flask import Flask , render_template , redirect , url_for , request 
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/ldApp"
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
        userData = mongo.db.students.find_one({"email":email})
        if (bcrypt.check_password_hash(userData["password"] , password)):
            return redirect('home')
    return render_template('login.html')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if (request.method == "POST"):
        name = request.form['name']
        email =  request.form['email']
        standard =  request.form['class']
        password = request.form['password1']
        re_password = request.form['password2']
        if(password == re_password):
            hashPassword1 = bcrypt.generate_password_hash(password)
            mongo.db.students.insert_one({"name":name , "password" : hashPassword1 , "email":email ,  "class":standard} )
            return redirect('login')
    return render_template('register.html')

@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/teacher",methods = ['GET', 'POST'])
def teacherLogin():
    if (request.method == "POST"):
        teacherEmail = request.form['email']
        password = request.form['password']
        adminDetail = mongo.db.admin.find_one({"email":teacherEmail})
        if (adminDetail["password"] == password):
            return redirect("adminpage")
    return render_template('admin.html')


@app.route('/adminpage')
def adminHome():
    adminName  = mongo.db.admin.find_one({"admin":"true"})
    return render_template('teacher.html' , adminName =  adminName["name"])


@app.route("/studentsData")
def availStudents():
    studentList = []
    for i in mongo.db.students.find():
        studentList.append(i["name"])
    length =  str(len(studentList))
    return length


@app.route("/studentlist")
def listData():
    studentList = []
    for i in mongo.db.students.find():
        studentList.append(i)
    return render_template('student.html',studentData = studentList )


@app.route('/addstudent' , methods=['GET', 'POST'])
def addStudent():
    if (request.method == "POST"):
            name = request.form['name']
            email =  request.form['email']
            standard =  request.form['class']
            password = request.form['password1']
            print(name, email, standard, password)
    
    return render_template('addstudent.html')

@app.route('/ld')
def ld():
    return render_template('LD.html')

@app.route('/non-ld')
def non_ld():
    return render_template('Non-LD.html')

if __name__=="__main__":
    app.run(debug=True , port=5000)



