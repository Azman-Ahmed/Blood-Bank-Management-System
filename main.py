


from flask import Flask, request, render_template, redirect, session, url_for
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

app.secret_key = 'super secret key'

client = MongoClient("localhost", 27017)
db = client.flask_db
todos = db.todos

info = db.info


@app.route('/home', methods=['POST','GET'])
def home():
    return render_template("home.html", **locals())


@app.route('/layout', methods=['POST','GET'])
def layout():
    return render_template("layout.html", **locals())



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('login'))

    return render_template('firstpage.html')



@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        uname = request.form['name']
        password = request.form['password']
        db_user = todos.find_one({"name": uname})

        if db_user is None:
            return "Username not found"
        if password != db_user["password"]:
            return "password did not match"

        return redirect(url_for('success'))

    return render_template("log_in.html",**locals())



@app.route('/success', methods=['POST', 'GET'])
def success():
    if request.method == 'POST':
        option = request.form['option']
        if option=="donate":
            return redirect(url_for('donate'))
        elif option=="check":
            return redirect(url_for('check'))
        elif option=="request":
            return redirect(url_for('req'))
    return render_template("page1.html")

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        blood_type = request.form['blood-type']
        weight = request.form['weight']
        last_donation_date = request.form['last-donation-date']

        info.insert_one({'name': name, 'blood type': blood_type})

        return render_template("donaterec.html",**locals())
    return render_template("donate.html")

@app.route('/donaterec')
def donaterec():
    return render_template("donaterec.html",**locals())

@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        blood_type = request.args.get('blood-type')

        # Perform the query to count available blood in MongoDB
        blood_count = info.count_documents({"blood-type": blood_type})

        return render_template("tem.html",**locals())
    return render_template("check.html",**locals())


@app.route('/req')
def req():
    return "Request"



@app.route('/userlogout', methods=['POST','GET'])
def userlogout():
    session.pop('name', None)
    return render_template("usersignin.html", **locals())


@app.route('/usersignup', methods=('POST','GET'))
def usersignup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        con_password = request.form['confirm-password']
        contact = request.form['phone']
        if password == con_password:
            todos.insert_one({'name': name, 'email': email, 'password': password, 'contact': contact})
        else:
            render_template('usersignup.html', **locals())

    all_todos = todos.find()
    return render_template('usersignup.html', todos=all_todos)



@app.route('/admin_login', methods=['POST','GET'])
def admin():
    return render_template("admin_login.html", **locals())


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002)

