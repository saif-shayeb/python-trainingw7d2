from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

students = []

@app.route('/')
def index():

    return render_template('index.html', students=students)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        course = request.form.get('course')
        
        if first_name and last_name and email and course:
            students.append({
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'course': course
            })
            return redirect(url_for('index'))
            
    return render_template('register.html')
@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit(student_id):
    student = students[student_id]
    if request.method == 'POST':
        student['first_name'] = request.form.get('first_name')
        student['last_name'] = request.form.get('last_name')
        student['email'] = request.form.get('email')
        student['course'] = request.form.get('course')
        return redirect(url_for('index'))
    return render_template('edit.html', student=student, student_id=student_id)

@app.route('/delete/<int:student_id>', methods=['GET', 'POST'])
def delete(student_id):
    if 0 <= student_id < len(students):
        students.pop(student_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
