import numpy as np
from model import RF
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.exceptions import BadRequestKeyError
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
app.secret_key = "Secret"
app.config["MONGO_URI"] = "mongodb://localhost:27017/ldApp"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)


@app.route('/')
def main():
    return redirect('/login')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if (request.method == "POST"):
        email = request.form['email']
        password = request.form['password']
        userData = mongo.db.students.find_one({"email": email})
        if (bcrypt.check_password_hash(userData["password"], password)):
            return redirect('home')
    return render_template('login.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if (request.method == "POST"):
        name = request.form['name']
        email = request.form['email']
        standard = request.form['class']
        password = request.form['password1']
        re_password = request.form['password2']
        if (password == re_password):
            hashPassword1 = bcrypt.generate_password_hash(password)
            mongo.db.students.insert_one(
                {"name": name, "password": hashPassword1, "email": email,  "class": standard})
            return redirect('login')
    return render_template('register.html')


@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/teacher", methods=['GET', 'POST'])
def teacherLogin():
    if (request.method == "POST"):
        teacherEmail = request.form['email']
        password = request.form['password']
        adminDetail = mongo.db.admin.find_one({"email": teacherEmail})
        if (adminDetail["password"] == password):
            return redirect("adminpage")
    return render_template('admin.html')


@app.route('/adminpage')
def adminHome():
    adminName = mongo.db.admin.find_one({"admin": "true"})
    return render_template('teacher.html', adminName=adminName["name"], home_active="class= active")


@app.route("/studentsData")
def availStudents():
    studentList = []
    for i in mongo.db.students.find():
        studentList.append(i["name"])
    length = str(len(studentList))
    return length


@app.route("/studentlist")
def listData():
    studentList = []
    for i in mongo.db.students.find():
        studentList.append(i)
    return render_template('student.html', studentData=studentList, studentList_active="class= active")


@app.route('/addstudent', methods=['GET', 'POST'])
def addStudent():
    allDetails = True
    if (request.method == "POST"):
        try:
            name = request.form['name']
            email = request.form['email']
            standard = request.form['class']
            password = request.form['password1']
            q1 = request.form['question1']
            q2 = request.form['question2']
            q3 = request.form['question3']
            q4 = request.form['question4']
            q5 = request.form['question5']
            q6 = request.form['question6']
            q7 = request.form['question7']
            q8 = request.form['question8']
            studentlevel = [q1, q2, q3, q4, q5, q6, q7, q8]
            le = LabelEncoder()
            le.fit(studentlevel)
            arr = le.transform(studentlevel)
            arr = np.array([arr])
            prediction = RF.predict(arr)
            print(prediction[0])
            if (prediction[0] == 'yes'):
                mongo.db.students.insert_one(
                    {"name": name,
                     "password": password,
                     "email": email,
                     "class": standard,
                     'student_details': {"Does the Student Reads Well?: ": q1,
                                         "Does the Student Writes Well?: ": q2,
                                         "Does the Student Calculates Well?: ": q3,
                                         "Does Student pays Attention?: ": q4,
                                         "is Student Hyperactive?:": q5,
                                         "is Student Impulsive?: ": q6,
                                         "Does Student can discriminate voice?: ": q7,
                                         "Does Student can discriminate visual?: ": q8},
                     'ld': True})
            else:
                mongo.db.students.insert_one(
                    {"name": name,
                     "password": password,
                     "email": email,
                     "class": standard,
                     'student_details': {"Does the Student Reads Well?: ": q1,
                                         "Does the Student Writes Well?: ": q2,
                                         "Does the Student Calculates Well?: ": q3,
                                         "Does Student pays Attention?: ": q4,
                                         "is Student Hyperactive?:": q5,
                                         "is Student Impulsive?: ": q6,
                                         "Does Student can discriminate voice?: ": q7,
                                         "Does Student can discriminate visual?: ": q8},
                     'ld': False})

            flash("Successfully added student!", "success")
        except BadRequestKeyError:
            flash('Missing somefeilds', "danger")

    return render_template('addstudent.html', addPage_active="class= active")


@app.route('/ld')
def ld():
    return render_template('LD.html', ld_active="class= active")


@app.route('/non-ld')
def non_ld():
    return render_template('Non-LD.html', non_ld_active="class= active")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
