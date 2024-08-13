from flask import Flask, request,render_template, redirect,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from pywebio.input import *
from pywebio.output import *
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from pywebio.session import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()


@app.route('/')
def Home():
    return render_template('Home.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')



    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/dashboard')
        else:
            return render_template('login.html',error='Invalid user')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html',user=user)
    
    return redirect('/login')

@app.route('/Start Exam')
def Start_Exam():
    c = 0
  
    put_html("<h1>Quiz</h1>")


    q1 = radio("Q1. Base language of web?",['javaScript','ASP','PHP','HTML'])
    if q1 =='HTML':
        c+=1

    q2 = radio("Q2. Which is not a programming language",['Python','HTML','Scala','Java'])
    if q2 =='HTML':
        c+=1

    q3 = radio("Q3. Secondery memory is also called _____",['Virtual memory','RAM','ROM','Hard drives'])
    if q3 =='ROM':
        c+=1

    q4 = radio("Q4. functions that is used to get th length of string in Python",['count()','length()','dis()','len()'])
    if q4 == 'len()':
        c+=1

    q5 = radio("Q5. Which is not a web framework",['Django','React','Numpy','Angular'])
    if q5 == 'Numpy':
        c+=1

    if c>3:
        message = [style(put_html("<h1 style='display:inline;border-bottom:0px'>Congratulations !! </>PASSh1>"+ ", your score is <b>"
            + str(c) + "</b><br><br>") ,'color:green;'),style(put_html("<p>Result : <bED</b></p>"),'color:green'), put_html("<b>Thank You for your participation.</b>")]
        
        message=[style(put_html("<a href='/logout' class='btn btn-dark'>Logout</a>"))]

        popup("Result", content=message, size='large', implicit_close=True, closable=True)
    else:
        message = [style(put_html("<h1 style='display:inline;border-bottom:0px'>Oops! " + "</h1>" + ", your score is <b>"
            + str(c) + "</b><br><br>"),'color:red'), style(put_html("<p>Result : <b>FAILED</b></p>"), 'color:red') , put_html("<b>Thank You for your participation.</b><br><br>"), style(put_link('Retry ↺',""), 'color:red;align-content: center;border-radius: 5px;color:#f9faf8;padding: 5px 100px;text-align:center;align-items : center;background-color: white;\
            background-image: linear-gradient(270deg, #8cf5f5 1%, #0a43f3 100%);')]
        
        message=[style(put_html("<a href='/logout' class='btn btn-dark'>Logout</a>"))]
        
        popup("Result", content=message, size='large', implicit_close=True, closable=True)


app.add_url_rule('/Start_Exam','webio_view',webio_view(Start_Exam),methods=['GET','POST','OPTIONS'])

    



@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')

# main fuction for strating  
if __name__ == '__main__':
    app.run(debug=True)