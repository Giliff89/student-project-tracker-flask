from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    html = render_template('student_info.html',
                           first=first,
                           last=last,
                           github=github)

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


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
