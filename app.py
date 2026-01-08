from flask import Flask, render_template, request, redirect, session, url_for
from models import init_db, get_db
from payroll import calculate_salary
from auth import authenticate, login_required
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Initialize database
init_db()

# Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if authenticate(username, password):
            session["user"] = username
            return redirect("/dashboard")
    return render_template("login.html")

# Dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    employees = db.execute("SELECT * FROM employee").fetchall()
    return render_template("dashboard.html", employees=employees)

# Add Employee
@app.route("/employee", methods=["GET", "POST"])
@login_required
def add_employee():
    if request.method == "POST":
        name = request.form["name"]
        basic = float(request.form["basic"])
        days = int(request.form["days"])
        gross, net = calculate_salary(basic, days)
        db = get_db()
        db.execute("INSERT INTO employee(name,basic,days,gross,net) VALUES (?,?,?,?,?)",
                   (name, basic, days, gross, net))
        db.commit()
        return redirect("/dashboard")
    return render_template("employee.html")

# Payroll
@app.route("/payroll")
@login_required
def payroll():
    db = get_db()
    employees = db.execute("SELECT * FROM employee").fetchall()
    return render_template("payroll.html", employees=employees)

# Payslip
@app.route("/payslip/<int:id>")
@login_required
def payslip(id):
    db = get_db()
    employee = db.execute("SELECT * FROM employee WHERE id=?", (id,)).fetchone()
    if not employee:
        return "Employee not found"
    return render_template("payslip.html", employee=employee)

# Delete Employee
@app.route("/delete/<int:id>")
@login_required
def delete_employee(id):
    db = get_db()
    db.execute("DELETE FROM employee WHERE id=?", (id,))
    db.commit()
    return redirect("/dashboard")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
