from flask import Flask,render_template,request,flash,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

db=SQLAlchemy()

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    applied_jobs = db.relationship('AppliedJob', back_populates='user')

class Job(db.Model):

    job_id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(20),nullable = False)
    job_location = db.Column(db.String(20),nullable = False)
    job_salary = db.Column(db.Float,nullable = False)

    applicants = db.relationship('AppliedJob', back_populates='job')

class AppliedJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'), nullable=False)

    user = db.relationship('User', back_populates='applied_jobs')
    job = db.relationship('Job', back_populates='applicants')
    
    
db.create_all()    
#----------------------------------------------ROUTES----------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

#----------------------------------------REGISTRATION-------------------------------
@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    return render_template('register.html', role='user')

@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    return render_template('register.html', role='admin')

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    return render_template('login.html', role='user')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    return render_template('login.html', role='admin')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user_n = request.form['username']
        user_p = request.form['password']
        existing_user = User.query.filter_by(username=user_n).first()

        if existing_user:
            flash('Username already exists.', 'warning')
        
        elif user_n and user_p:
            new_user = User(username=user_n)
            new_user.set_password(user_p)  
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect('/login')
        else:
            flash('Please fill in all fields.', 'danger')


    return render_template('register.html')

#---------------------------------------------LOGIN---------------------------------------
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get['username']
        password = request.form.get['password']


        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):  
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('app.home'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
    
    return render_template('login.html')



#-------------------------------------------Job apply--------------------------------
@app.route('/job_reg',methods=['GET','POST'])
def job_reg():
    title = request.form('title')
    location = request.form('location')
    salary = request.form('salary')

if __name__=='__main__':
    app.run(debug=True)