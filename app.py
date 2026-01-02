from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__, static_folder="static")


db = mysql.connector.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME")
)


@app.route("/")
def home():
    return redirect("/users")


@app.route("/users", methods=["GET", "POST"])
def users():
    cur = db.cursor()

    msg = ""

    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']

        try:
            cur.execute(
                "INSERT INTO users (full_name, email, role, status) VALUES (%s, %s, %s, 'active')",
                (name, email, role)
            )
            db.commit()
            msg = "User added successfully!"

        except:
            msg = "❌ This email already exists!"

    cur.execute("SELECT * FROM users")
    data = cur.fetchall()

    return render_template("users.html", users=data, message=msg)


@app.route("/delete/<id>")
def delete(id):
    cur = db.cursor()
    cur.execute("DELETE FROM users WHERE id=%s",(id,))
    db.commit()
    return redirect("/users")


@app.route("/edit/<id>", methods=["GET","POST"])
def edit(id):
    cur = db.cursor()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        cur.execute(
            "UPDATE users SET full_name=%s, email=%s, role=%s WHERE id=%s",
            (name,email,role,id)
        )
        db.commit()
        return redirect("/users")

    cur.execute("SELECT * FROM users WHERE id=%s",(id,))
    data = cur.fetchone()
    return render_template("edit.html", u=data)



if __name__ == "__main__":
    app.run(debug=True)
