from flask import Flask, render_template, request, redirect, jsonify
import math
#from flask_paginate import Pagination, get_page_args
import re

app = Flask(__name__)

import psycopg2



def get_db_connection():
    conn = psycopg2.connect(database="your_db_name",
                            host="127.0.0.1",
                            user="postgres",
                            password="you_password",
                            port="5432")
    
    return conn

conn = get_db_connection()
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS emp_table (id serial PRIMARY KEY,'
                                 'name varchar (50) NOT NULL,'
                                 'email varchar (50) NOT NULL,'
                                 'designation varchar (50) NOT NULL,'
                                 'salary integer NOT NULL);'
                                 )

conn.commit()
cursor.close()
conn.close()



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/employees', methods=["GET", "POST"])
def employee_list():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    if request.method == "POST" :
        if request.is_json:
            data = request.get_json()
            name = data.get("name")
            email = data.get("email")
            designation = data.get("designation")
            salary = data.get("salary")
        else:
            name = request.form.get("name")
            email = request.form.get("email")
            designation = request.form.get("designation")
            salary = request.form.get("salary")

        regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not name or not email or not designation or not salary:
            error_message = "Please fill all fields."
            if request.is_json:
                return jsonify({"error": error_message})
            else:
                return render_template("failure.html", message=error_message)

        if not re.fullmatch(regex_email, email):
            error_message = "Invalid email format."
            if request.is_json:
                return jsonify({"error": error_message})
            else:
                return render_template("failure.html", message=error_message)

        try:
            salary = int(salary)
            if salary <= 0:
                raise ValueError()
        except ValueError:
            error_message = "Salary must be a positive integer."
            if request.is_json:
                return jsonify({"error": error_message})
            else:
                return render_template("failure.html", message=error_message)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO emp_table (name, email, designation, salary)'
                    'VALUES(%s, %s, %s, %s)',
                    (name, email, designation, salary)
                    )
        conn.commit()
        cursor.close()
        conn.close()

    #return redirect("/employees")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * from emp_table;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    
    #return jsonify({"emp":data})
    return render_template("display_emp.html", emps=data)

    
    # offset = (page - 1) * page_size
    # conn = get_db_connection()
    # cursor = conn.cursor()
    # cursor.execute("SELECT COUNT(*) FROM emp_table;")
    # total_records = cursor.fetchone()[0]
    # total_pages = math.ceil(total_records / page_size)

    # cursor.execute("SELECT * FROM emp_table ORDER BY id LIMIT %s OFFSET %s", (page_size, offset))
    # employees = cursor.fetchall()
    # cursor.close()
    # conn.close()

    # employees_data = [{
    #     "id": emp[0], "name": emp[1], "email": emp[2],
    #     "designation": emp[3], "salary": emp[4]
    # } for emp in employees]

    # return jsonify({
    #     "employees": employees_data,
    #     "total_pages": total_pages,
    #     "current_page": page
    # })
                                       



@app.route('/find_employees', methods=["GET"])
def find_by_id():
    id = request.args.get("emp_id")
    #print(f"employee id = {id}")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emp_table WHERE id = %s;", id)
    data = cursor.fetchall()
    cursor.close()
    conn.close() 
    if not data:
        return render_template("failure.html", message="Id not found")   
    return render_template("display_emp.html", emps = data)
    

@app.route('/delete/<id>', methods=["GET","DELETE"])
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE from emp_table WHERE id = %s;", id)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/employees")

@app.route('/update/<id>', methods=["GET", "POST"])
def update(id):
    if request.method == "POST":
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emp_table WHERE id = %s;", id)
        data = cursor.fetchone()
        cursor.close()
        conn.close()

        name = request.form.get("name")
        email = request.form.get("email")
        designation = request.form.get("designation")
        salary  = request.form.get("salary")

        if not name:
            name = data[1]
        if not email:
            email = data[2]
        if not designation:
            designation = ""
        if not salary:
            salary = data[4]
        
        salary = int(salary)

        regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if not re.fullmatch(regex_email, email):
            error_message = "Invalid email format."
            if request.is_json:
                return jsonify({"error": error_message})
            else:
                return render_template("failure.html", message=error_message)

        try:
            salary = int(salary)
            if salary <= 0:
                raise ValueError()
        except ValueError:
            error_message = "Salary must be a positive integer."
            if request.is_json:
                return jsonify({"error": error_message})
            else:
                return render_template("failure.html", message=error_message)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE emp_table SET name=%s, email=%s, designation=%s, salary=%s WHERE id=%s;',
                        (name, email, designation, salary, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/employees")

    elif request.method == "GET":
        return render_template("update_emp.html", emp_id = id)
    


    