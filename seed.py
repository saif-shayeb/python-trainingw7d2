from app import app, db, Course, Student

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Add courses
    c1 = Course(name='Computer Science')
    c2 = Course(name='Engineering')
    c3 = Course(name='Mathematics')
    c4 = Course(name='Physics')
    
    db.session.add_all([c1, c2, c3, c4])
    db.session.commit()

    # Add students
    s1 = Student(first_name='John', last_name='Doe', email='john@example.com', course=c1)
    s2 = Student(first_name='Jane', last_name='Smith', email='jane@example.com', course=c2)
    s3 = Student(first_name='Alice', last_name='Johnson', email='alice@example.com', course=c1)

    db.session.add_all([s1, s2, s3])
    db.session.commit()

    print("Database seeded with courses and demo students!")
