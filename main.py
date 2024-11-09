from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection
def create_connection():
    conn = sqlite3.connect("employee_management.db")
    return conn

# Create table if it doesn't exist
def create_table():
    conn = create_connection()
    sql_create_employee_table = """
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT NOT NULL,
        salary REAL NOT NULL
    );
    """
    cursor = conn.cursor()
    cursor.execute(sql_create_employee_table)
    conn.commit()
    conn.close()
@app.route('/',methods=['GET', 'POST'])
def home():
    return render_template('index.html')
# Add an employee
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        salary = float(request.form['salary'])
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)", (name, position, salary))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('add_employee.html')

# View all employees

@app.route('/view',methods=['GET', 'POST'])
def view_employees():

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()
    if request.method=="POST":
        redirect('/')

    return render_template('view_employees.html', employees=employees)

# Update an employee
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    conn = create_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        salary = float(request.form['salary'])
        cursor.execute("UPDATE employees SET name = ?, position = ?, salary = ? WHERE id = ?", (name, position, salary, id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_employees'))
    cursor.execute("SELECT * FROM employees WHERE id = ?", (id,))
    employee = cursor.fetchone()
    conn.close()
    return render_template('update_employee.html', employee=employee)

# Delete an employee
@app.route('/delete/<int:id>')
def delete_employee(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_employees'))

# Run the application
if __name__ == '__main__':
    create_table()
    app.run(debug=True)
