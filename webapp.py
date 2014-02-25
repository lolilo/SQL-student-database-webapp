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
    row = hackbright_app.get_student_by_github(student_github)
    # row[0] is the student's first name
    row2 = hackbright_app.show_all_grades_for_student(row[0])

    # return '%s\'s grades: ' % row[0]
    # for i in row2:
    #     return "%s: %s" % (i[0], i[1])

    html = render_template("student_info.html", first_name = row[0],
                                                last_name = row[1],
                                                github=row[2],
                                                project=row2[0][0],
                                                grade=row2[0][1])
    return html

if __name__ == "__main__":
    # if running, call flask as our main loop 
    app.run(debug=True)
    # if something is wrong, display debug output

