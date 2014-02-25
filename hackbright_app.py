import sqlite3

DB = None
CONN = None


def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

    # this '\' tells Python to not worry about whitespace, in this particular instance, a new line
#     return """\
# Student: %s %s
# Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    
    # committing on the database connection, not the cursor
    CONN.commit()
    return "Successfully added student: %s %s" % (first_name, last_name)

def get_project_by_title(title):
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()

    return """\
Project ID: %s
Project Title: %s
Project Description: %s
Maximum Grade: %s""" %(row[0], row[1], row[2], row[3])    

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade) VALUES (?,?,?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    return "Successfully added project: %s" % title

def get_grade_by_project(title, student):
    query = """SELECT grade FROM Grades JOIN Students ON student_github = github lWHERE project_title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    # return row
    return """\
    Grade: %s""" % row[0]    

def give_grade_to_student(student, project, grade):
    query = """INSERT into Grades VALUES (
        (SELECT DISTINCT github FROM Students WHERE first_name = ?), ?, ?)"""
    DB.execute(query, (student, project, grade))
    CONN.commit()
    return "Successfully assigned grade of %s to %s for project %s" %(grade, student, project)

def show_all_grades_for_student(student_name):
    query = """SELECT project_title, grade FROM Grades 
        WHERE student_github = 
        (SELECT DISTINCT github FROM Students WHERE first_name = ?)"""  
    DB.execute(query, (student_name,))
    rows = DB.fetchall()
    return rows
    
    # return '%s\'s grades: ' % student_name
    # for i in rows:
    #     return "%s: %s" % (i[0], i[1])

def main():
    connect_to_db()
    command = None
    while command != "quit":

        # HBA Database> new_student Bartholomew MacGillicuddy bartmac

        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project_title":
            get_project_by_title(*args)
        elif command == "new_project":
            # need to format for string as second argument 
            title = args[0]
            desc = ' '.join(args[1:-1]) 
            max_grade = args[-1]  
            make_new_project(title, desc, max_grade)
        elif command == "get_grade":
            get_grade_by_project(*args)
        elif command == "assign_grade":
            give_grade_to_student(*args)  
        elif command == "show_student_grades":
            show_all_grades_for_student(*args)      

          

    CONN.close()

if __name__ == "__main__":
    main()
