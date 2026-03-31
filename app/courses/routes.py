from flask import render_template, request, redirect, url_for, flash
from app.courses import bp
from app.models import Course
from app import db

@bp.route('/')
def index():
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses)

@bp.route('/new', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            new_course = Course(name=name)
            db.session.add(new_course)
            db.session.commit()
            return redirect(url_for('courses.index'))
    return render_template('add_course.html')

@bp.route('/edit/<int:course_id>', methods=['GET', 'POST'])
def edit(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            course.name = name
            db.session.commit()
            return redirect(url_for('courses.index'))
    return render_template('edit_course.html', course=course)

@bp.route('/delete/<int:course_id>', methods=['GET', 'POST'])
def delete(course_id):
    course = Course.query.get_or_404(course_id)
    if course.students:
        flash('Cannot delete course because there are students enrolled in it. Please reassign or delete the students first.', 'error')
        return redirect(url_for('courses.index'))
        
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully.', 'success')
    return redirect(url_for('courses.index'))
