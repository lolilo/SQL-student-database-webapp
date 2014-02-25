from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/student")
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

# @app.route("/projects")
# # page listing all students and their grades for that particular project 
# def get_student():
#     hackbright_app.connect_to_db()
#     project = request.args.get("project")
#     d1 = hackbright_app.get_grade_by_project(project)

#     html = render_template("student_info.html", project_data = d2)
#     return html


if __name__ == "__main__":
    # if running, call flask as our main loop 
    app.run(debug=True)
    # if something is wrong, display debug output

