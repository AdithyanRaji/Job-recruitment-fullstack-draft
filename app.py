from flask import Flask,render_template,request,flash,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
from flask import send_file
from datetime import datetime, timezone

app = Flask(__name__)

db=SQLAlchemy()

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/resumes'

db.init_app(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10), nullable=False)  # 'user' or 'admin'
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    full_name = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    applied_jobs = db.relationship('AppliedJob', back_populates='user')

class Job(db.Model):

    job_id = db.Column(db.Integer, primary_key=True)
    job_company = db.Column(db.String(20),nullable = False)
    job_description = db.Column(db.String(100),nullable = True)
    job_title = db.Column(db.String(20),nullable = False)
    job_location = db.Column(db.String(20),nullable = False)
    job_salary = db.Column(db.Float,nullable = False)

    applicants = db.relationship('AppliedJob', back_populates='job')

class AppliedJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'), nullable=False)
    job_title = db.Column(db.String(20), nullable=False)
    resume_path = db.Column(db.String(200), nullable=False)
    
    status = db.Column(db.String(20), default="Pending")  # Pending / Selected / Rejected
    applied_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    selected_at = db.Column(db.DateTime, nullable=True)
    
    user = db.relationship('User', back_populates='applied_jobs')
    job = db.relationship('Job', back_populates='applicants')
    
# add the with optiuon to create_all
'''with app.app_context():
    db.drop_all()
    db.create_all()'''
#------------------------------------------ROUTES---------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<uname>/home')
def home(uname):
    if 'username' not in session or session['role'] != 'user':
        flash("Please login as a user.", "warning")
        return redirect(url_for('user_login'))
        
    jobs = Job.query.all()
    return render_template('home.html', uname=uname, jobs=jobs)

#-------------------------------------------REGISTRATION-------------------------------------
@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    return render_template('register.html', role='user')

@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    return render_template('register.html', role='admin')


@app.route('/<role>/check_register', methods=['GET', 'POST'])
def check_register(role):
    if request.method == 'POST':
        user_n = request.form['username']
        if role != 'admin':
            user_em = request.form['email']
            user_fn = request.form['full_name']
        user_p = request.form['password']

        existing_user = User.query.filter_by(username=user_n).first()

        if existing_user:
            flash('Username already exists.', 'warning')
            return render_template('register.html', role=role)

        elif user_n and user_p:
            if role != 'admin':
                new_user = User(username=user_n, email=user_em, full_name=user_fn, role=role)
            else:
                new_user = User(username=user_n, role=role)
            new_user.set_password(user_p)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(f'/{role}/login')

        else:
            flash('Please fill in all fields.', 'danger')

    return render_template('register.html', role=role)

#------------------------------------------------LOGIN---------------------------------------
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    return render_template('login.html', role='user')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    return render_template('login.html', role='admin')

@app.route('/<role>/check_login', methods=['GET', 'POST'])
def check_login(role):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['username'] = username
            session['role'] = user.role  
            flash('Login successful!', 'success')

            # redirect based on role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                jobs = Job.query.all()
                return redirect(url_for('home',uname=username))
        else:
            flash('Invalid credentials, please try again.', 'danger')

    return render_template('login.html', role=role)

#--------------------------------------------ADMIN DASHBOARD---------------------------------

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'role' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html', uname=session['username'])
    else:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('index'))

@app.route('/add_jobs',methods=['GET','POST'])
def add_jobs():
    if request.method == 'POST':
        
        j_title = request.form['job_title']
        j_company = request.form['company_name']
        j_description = request.form['job_description']
        j_location = request.form['location']
        j_salary = float(request.form['salary'])
        new_job = Job(job_title=j_title,job_company=j_company ,job_location=j_location,job_description=j_description , job_salary=j_salary)
        db.session.add(new_job)
        db.session.commit()
        flash('Job added successfully!', 'success')
        return redirect(url_for('admin_dashboard',uname=session['username']))
    
    return render_template('admn_func/addjobs.html')

@app.route('/joblistings')
def joblistings():
    jobs = Job.query.all()
    return render_template('admn_func/joblistings.html', jobs=jobs)

@app.route('/select_applicant', methods=['GET'])
def select_applicants():
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied.", "danger")
        return redirect(url_for('index'))

    app = AppliedJob.query.all()
    return render_template('admn_func/selc_appcn.html', applicants=app)
    

@app.route('/applicant_info')
def applicant_info():
    u_info = User.query.all()
    return render_template('admn_func/userinfo.html', users=u_info)


@app.route('/selected_app/<uname>', methods=['GET', 'POST'])
def selected_app(uname):
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied.", "danger")
        return redirect(url_for('index'))
    if request.method == 'POST':
        applicant_id=request.form['applicant_id']
        app = AppliedJob.query.get_or_404(applicant_id)
        app.status = "Selected"
        app.selected_at = datetime.now(timezone.utc)

        db.session.commit()
        flash('Applicant selected successfully!', 'success')
        return redirect(url_for('select_applicants'))
        

    selected_apps = AppliedJob.query.filter_by(status='Selected').all()
    return render_template('admn_func/selctd_users.html', applicants=selected_apps, uname=uname)

@app.route('/reject_cand', methods=['POST'])
def reject_cand():
    # admin guard
    if 'role' not in session or session['role'] != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('index'))

    applicant_id = request.form.get('applicant_id')
    if not applicant_id:
        flash('No applicant specified.', 'warning')
        return redirect(request.referrer or url_for('selected_app', uname=session.get('username')))

    try:
        applicant_id = int(applicant_id)
    except ValueError:
        flash('Invalid applicant id.', 'danger')
        return redirect(request.referrer or url_for('selected_app', uname=session.get('username')))

    app_obj = AppliedJob.query.get_or_404(applicant_id)

    try:
        # either remove the record or mark as 'Rejected'
        # Option A: mark rejected
        app_obj.status = 'Rejected'
        app_obj.selected_at = None
        db.session.commit()
        
        flash(f'{app_obj.username} removed/marked as Rejected.', 'success')
    except Exception as e:
        db.session.rollback()
        # optionally log the exception
        flash('Could not remove applicant. Try again.', 'danger')

    return redirect(request.referrer or url_for('selected_app', uname=session.get('username')))

#---------------------------------------------User Job apply--------------------------------------
    
@app.route('/job_reg',methods=['GET','POST'])
def job_reg():
    title = request.form('title')
    location = request.form('location')
    salary = request.form('salary')

@app.route('/view_jobs', methods=['GET', 'POST'])
def view_jobs():
    jobs = Job.query.all()
    return render_template('jobs.html', jobs=jobs)

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    if request.method == 'POST':
        name = session['username']
        resume = request.files['resume']

        if resume:
            filename = secure_filename(resume.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            resume.save(save_path)

            user_id = User.query.filter_by(username=name).first().id
            application = AppliedJob(username=name,resume_path=save_path, job_id=job_id,user_id=user_id, job_title=request.form['title'])
            db.session.add(application)
            db.session.commit()

            flash('Application submitted!', 'success')
            return redirect(url_for('joblistings'))

    return render_template('apply.html', job_id=job_id)


@app.route('/view_resume/<int:applicant_id>', methods=['GET'])
def view_resume(applicant_id):
    applicant = AppliedJob.query.get_or_404(applicant_id)
    resume_path = applicant.resume_path

    return send_file(resume_path, as_attachment=False)

#---------------------------------------------LOGOUT-----------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

#---------------------------------------------RUN APP----------------------------------------
if __name__=='__main__':
    app.run(debug=True)