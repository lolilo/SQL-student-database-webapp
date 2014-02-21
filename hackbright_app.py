import sqlite3

DB = None
CONN = None


def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()

    # print row

    # this '\' tells Python to not worry about whitespace, in this particular instance, a new line
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    
    # committing on the database connection, not the cursor
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def get_project_by_title(title):
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()

    print """\
Project ID: %s
Project Title: %s
Project Description: %s
Maximum Grade: %s""" %(row[0], row[1], row[2], row[3])    

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade) VALUES (?,?,?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s" % title



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
            make_new_project(*args)

          

    CONN.close()

if __name__ == "__main__":
    main()
