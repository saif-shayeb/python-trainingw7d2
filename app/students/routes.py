from flask import render_template, request, redirect, url_for, flash
from app.students import bp
from app.models import Student, Course
from app import db

@bp.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        course_id = request.form.get('course')
        
        if first_name and last_name and email and course_id:
            if Student.query.filter_by(email=email).first():
                flash('Email address is already registered. Please use a different one.', 'error')
                courses = Course.query.all()
                return render_template('register.html', courses=courses, form_data=request.form)
                
            student = Student(
                first_name=first_name,
                last_name=last_name,
                email=email,
                course_id=course_id
            )
            db.session.add(student)
            db.session.commit()
            flash('Student registered successfully!', 'success')
            return redirect(url_for('students.index'))
        else:
            flash('All fields are required!', 'error')
            courses = Course.query.all()
            return render_template('register.html', courses=courses, form_data=request.form)
            
    courses = Course.query.all()
    return render_template('register.html', courses=courses)

@bp.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Prevent taking an email that belongs to another student
        existing_student = Student.query.filter_by(email=email).first()
        if existing_student and existing_student.id != student_id:
            flash('Email address is already in use by another student.', 'error')
            return redirect(url_for('students.edit', student_id=student_id))

        student.first_name = request.form.get('first_name')
        student.last_name = request.form.get('last_name')
        student.email = email
        student.course_id = request.form.get('course')
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('students.index'))
        
    courses = Course.query.all()
    return render_template('edit.html', student=student, courses=courses)

@bp.route('/delete/<int:student_id>', methods=['GET'])
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('students.index'))
