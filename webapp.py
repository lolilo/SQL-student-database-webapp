from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/student")
# page listing given student's projects and grades
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    d1 = hackbright_app.get_student_by_github(student_github)
    d2 = hackbright_app.show_all_grades_for_student(d1['first name'])
    html = render_template("student_info.html", first_name = d1['first name'],
                                                last_name = d1["last name"],
                                                github = d1["github"],
                                                project_data = d2)
    return html

@app.route("/projects")
# page listing all students and their grades for a given project 
# when clicking on a student's github account, it sends you back to the get_student handler
def get_grade_by_project():
    hackbright_app.connect_to_db()
    project = request.args.get("project")
    d = hackbright_app.get_grade_by_project(project)

    html = render_template("project_grades.html", project_title = project, project_data = d)
    return html


@app.route("/createstudent")
def make_new_student():
    html = render_template("create_student.html")
    return html

@app.route("/createstudentsuccess")
# http://localhost:5000/createstudentsuccess?first_name=ha&last_name=yo
# http://localhost:5000/createstudentsuccess?first_name=s&last_name=f&github=d
# if extra arguments, doesn't matter? That github argument. 
# Yes, this is true. Think for moment, LiLo. -__- Jeez. You can pass args in and not use them.
def made_new_student():
    hackbright_app.connect_to_db()
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    github = request.args.get("github")
    hackbright_app.make_new_student(first_name, last_name, github)

    html = "Student %s %s has been added to the database." % (first_name, last_name)
    return html

# Yeah, stub those functions.
@app.route("/newproject")
def make_new_project():
    html = render_template("create_project.html")
    return html

@app.route("/newprojectsuccess")
def made_new_project():
    hackbright_app.connect_to_db()
    title = request.args.get("title")
    desc = request.args.get("description")
    max_grade = request.args.get("max_grade")
    hackbright_app.make_new_project(title, desc, max_grade)

    html = "Project %s has been added to the database." % title
    return html

@app.route("/assigngrade")
def assign_grade():
    html = render_template("assign_grade.html")
    return html

@app.route("/assignedgrade")
def assigned_grade():
    hackbright_app.connect_to_db()
    student = request.args.get("student")
    project = request.args.get("project")
    grade = request.args.get("grade")
    hackbright_app.give_grade_to_student(student, project, grade)

    html = "Successfully assigned grade of %s for project %s to %s." % (grade, project, student)
    return html


# TO DO\
# Add links to pages that allow you to navigate the entirety of the app 
# you should never have to manually enter a URL to reach a particular handler.
# Make it look pretty.

if __name__ == "__main__":
    # if running, call flask as our main loop 
    app.run(debug=True)
    # if something is wrong, display debug output

