import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'dev_secret_key'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    students = db.relationship('Student', backref='course', lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        course_id = request.form.get('course')
        
        if first_name and last_name and email and course_id:
            student = Student(
                first_name=first_name,
                last_name=last_name,
                email=email,
                course_id=course_id
            )
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('index'))
            
    courses = Course.query.all()
    return render_template('register.html', courses=courses)

@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.first_name = request.form.get('first_name')
        student.last_name = request.form.get('last_name')
        student.email = request.form.get('email')
        student.course_id = request.form.get('course')
        db.session.commit()
        return redirect(url_for('index'))
        
    courses = Course.query.all()
    return render_template('edit.html', student=student, courses=courses)

@app.route('/delete/<int:student_id>', methods=['GET', 'POST'])
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/courses')
def courses():
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses)

@app.route('/courses/new', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            new_course = Course(name=name)
            db.session.add(new_course)
            db.session.commit()
            return redirect(url_for('courses'))
    return render_template('add_course.html')

@app.route('/courses/edit/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            course.name = name
            db.session.commit()
            return redirect(url_for('courses'))
    return render_template('edit_course.html', course=course)

@app.route('/courses/delete/<int:course_id>', methods=['GET', 'POST'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.students:
        flash('Cannot delete course because there are students enrolled in it. Please reassign or delete the students first.', 'error')
        return redirect(url_for('courses'))
        
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully.', 'success')
    return redirect(url_for('courses'))

if __name__ == '__main__':
    app.run(debug=True)
