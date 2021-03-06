from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def homepage():
    """Brings user to the student project homepage"""

    students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()

    return render_template('home.html',
                           students=students,
                           projects=projects)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    projects = hackbright.get_grades_by_github(github)

    html = render_template('student_info.html',
                           first=first,
                           last=last,
                           github=github,
                           projects=projects)

    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add", methods=["GET"])
def show_add_student_form():
    """Shows form to add a new student to the database."""

    return render_template("student_add_form.html")


@app.route("/student-add", methods=["POST"])
def add_student():
    """Adds new student to database from form"""

    first_name = request.form.get('first')
    last_name = request.form.get('last')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("added_student.html",
                           github=github,
                           first_name=first_name,
                           last_name=last_name)


@app.route("/project")
def get_project_info():
    """Displays information about the student project."""

    title = request.args.get('title')

    project_info = hackbright.get_project_by_title(title)
    student_grades = hackbright.get_grades_by_title(title)

    return render_template("project_info.html",
                           title=project_info[0],
                           description=project_info[1],
                           max_grade=project_info[2],
                           student_grades=student_grades)


@app.route("/project-add", methods=['GET'])
def show_add_project_form():
    """Shows form to add a new project to the database."""

    return render_template("project_add_form.html")


@app.route("/project-add", methods=['POST'])
def add_project():
    """Adds new project to database from form"""

    title = request.form.get('title')
    desc = request.form.get('desc')
    max_grade = request.form.get('max_grade')

    hackbright.make_new_project(title, desc, max_grade)

    return render_template("added_project.html",
                           title=title)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
