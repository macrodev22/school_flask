from flask import Flask,render_template,request,redirect,url_for,flash
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from models import db,Program,Student,StudentProgram

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.secret_key = '(EZ+@P;uZPe+@[>?XI&@()_DMvvT+4'

login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Student, user_id)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        programs = Program.query.all()
        return render_template('register.html', programs=programs)
    elif request.method == 'POST':
        # Get form data using request.form
        full_name = request.form['fullName']
        gender = request.form['gender']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['passwordConfirm']
        selected_program_id = request.form['programs']
        
        # Validate password confirmation
        if password != password_confirm:
            flash("Passwords do not match!")
            return redirect('/register')
        
        
        # Create a new student record
        new_student = Student(
            name=full_name,
            email=email,
            gender=gender,
        )

        new_student.set_password(password)
        
        # Add the student to the database
        db.session.add(new_student)
        db.session.commit()

        # Add selected program to the student's programs
        selected_program = Program.query.get(selected_program_id)
        new_student.programs.append(selected_program)
        db.session.commit()
        
        login_user(new_student)
        # print(request.form)
        return redirect('/dashboard')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        # Authenticate
        email = request.form.get("email")
        password = request.form.get('password')

        student = Student.query.filter(Student.email == email).first()

        # Verify the password
        if student.check_password(password):
            user = student
            login_user(user)
            return redirect(url_for('student_dashboard'))
        else:
            return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def student_dashboard():
    student_id = current_user.id
    student = db.session.get(Student, student_id)
    program = student.programs
    programs = Program.query.all()
    
    return render_template('student_dashboard.html', programs=programs, student=student, student_program=program[0])

@app.route('/changemodule', methods=['POST'])
def module_change():
    # Change the module
    student_id = current_user.id
    selected_module_id = request.form.get('modules')
    
    student_program = StudentProgram.query.filter(StudentProgram.student_id == student_id).first()
    student_program.program_id = selected_module_id

    db.session.commit()
    return redirect(url_for('student_dashboard'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


#DB Initialisation
reinitialize = False

if __name__ == '__main__':
    if reinitialize:
        with app.app_context():
            db.create_all()

    app.run(debug=True)