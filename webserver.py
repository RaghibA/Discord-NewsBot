from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = '5bae84dd2155347cdc0bd2405250309c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(16), nullable = False)
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"User('{self.username}')"



# home page 
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# registration form
@app.route('/register')
def reg():
    return render_template('register.html', title='register')

@app.route('/register', methods=['GET','POST'])
def Register():

    reg_username = request.form['u']
    reg_password = request.form['p']
    reg_cpassword = request.form['c']

    hash_cpass = bcrypt.generate_password_hash(reg_password).decode('utf-8')

    # db
    newuser = user(username = reg_username, password = hash_cpass)
    db.session.add(newuser)
    db.session.commit()

    print(reg_username)
    print(reg_password)
    print(reg_cpassword)

    if reg_password != reg_cpassword:
        return render_template('register.html', title='register')

    return redirect('/login')


# login form
@app.route('/login')
def log():
    return render_template('login.html', title='login')

@app.route('/login', methods=['GET','POST'])
def Login():

    username = request.form['u']
    password = request.form['p']

    print(username)
    print(password)

    encpass = bcrypt.generate_password_hash(password).decode('utf-8')

    u = user.query.filter_by(username = username).first()

    if u and bcrypt.check_password_hash(u.password, password):
        return render_template('success.html')

    return  render_template('login.html')

if __name__ == '__main__':
    # for unt cse server
    #app.run(debug=True, host = "10.144.192.158", port = "8000")
    # for local
    app.run(debug=False, host = "127.0.0.1", port = "8000")