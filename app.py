from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    session,
    send_file
)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "student123"

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:Harini%402006@localhost/studentdb"

app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False

db = SQLAlchemy(app)



class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    age = db.Column(
        db.Integer,
        nullable=False
    )

    department = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True
    )

    photo = db.Column(
        db.String(255)
    )


@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect(
            "/login"
        )

    total = Student.query.count()

    return render_template(
        "dashboard.html",
        total=total
    )



@app.route(
    "/login",
    methods=["GET", "POST"]
)

def login():

    if request.method == "POST":

        username = request.form[
            "username"
        ]

        password = request.form[
            "password"
        ]

        if (
            username == "admin"
            and
            password == "1234"
        ):

            session["user"] = username

            return redirect(
                "/dashboard"
            )

        flash(
            "Invalid Login"
        )

    return render_template(
        "login.html"
    )


@app.route("/logout")

def logout():

    session.clear()

    return redirect(
        "/login"
    )



@app.route(
    "/",
    methods=["GET", "POST"]
)

def register():

    if request.method == "POST":

        name = request.form["name"]

        age = request.form["age"]

        department = request.form[
            "department"
        ]

        email = request.form[
            "email"
        ]

        photo = request.files[
            "photo"
        ]

        filename = photo.filename

        if filename:

            photo.save(
                f"static/uploads/{filename}"
            )

        if int(age) <= 0:

            flash(
                "Age must be positive"
            )

            return redirect("/")

        existing = Student.query.filter_by(
            email=email
        ).first()

        if existing:

            flash(
                "Email already exists"
            )

            return redirect("/")

        student = Student(

            name=name,

            age=age,

            department=department,

            email=email,

            photo=filename

        )

        db.session.add(
            student
        )

        db.session.commit()

        flash(
            "Registered successfully"
        )

        return redirect("/")

    return render_template(
        "index.html"
    )



def search():

    query = request.args.get(
        "q",
        ""
    )

    students = Student.query.filter(

        Student.name.ilike(
            f"%{query}%"
        )

    ).all()

    return render_template(
        "students.html",
        students=students
    )


@app.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)

def edit_student(id):

    student = Student.query.get_or_404(id)

    if request.method == "POST":

        student.name = request.form[
            "name"
        ]

        student.age = request.form[
            "age"
        ]

        student.department = request.form[
            "department"
        ]

        student.email = request.form[
            "email"
        ]

        photo = request.files[
            "photo"
        ]

        if photo and photo.filename:

            filename = photo.filename

            photo.save(
                f"static/uploads/{filename}"
            )

            student.photo = filename

        db.session.commit()

        flash(
            "Updated successfully"
        )

        return redirect(
            "/students"
        )

    return render_template(
        "edit.html",
        student=student
    )

@app.route("/students")

def view_students():

    data = Student.query.all()

    return render_template(
        "students.html",
        students=data
    )


@app.route(
    "/delete/<int:id>"
)

def delete(id):

    student = Student.query.get_or_404(id)

    db.session.delete(
        student
    )

    db.session.commit()

    flash(
        "Deleted successfully"
    )

    return redirect(
        "/students"
    )



if __name__ == "__main__":

    app.run(
        debug=True
    )