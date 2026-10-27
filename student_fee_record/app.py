from flask import Flask, request, render_template, redirect
import psycopg2

app = Flask(__name__)

# Connect to database
def db_connect():
    return psycopg2.connect(
        dbname="samarth",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )


# Create Fee table
def create_table():
    con = db_connect()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Fee (
            Fee_ID SERIAL PRIMARY KEY,
            Student_Name VARCHAR(100),
            Course VARCHAR(100),
            Amount_Paid FLOAT
        )
    """)

    con.commit()
    cur.close()
    con.close()


# Insert fee record
@app.route("/", methods=["GET", "POST"])
def add_fee():
    if request.method == "POST":
        student_name = request.form["Student_Name"]
        course = request.form["Course"]
        amount_paid = request.form["Amount_Paid"]

        con = db_connect()
        cur = con.cursor()

        cur.execute(
            "INSERT INTO Fee (Student_Name, Course, Amount_Paid) VALUES (%s, %s, %s)",
            (student_name, course, amount_paid)
        )

        con.commit()
        cur.close()
        con.close()

        return redirect("/fee")

    return render_template("add.html")


# Display fee records
@app.route("/fee")
def display_fees():
    con = db_connect()
    cur = con.cursor()

    cur.execute("SELECT * FROM Fee ORDER BY Fee_ID")
    fees = cur.fetchall()

    cur.execute("SELECT COALESCE(SUM(Amount_Paid), 0) FROM Fee")
    total = cur.fetchone()[0]

    cur.close()
    con.close()

    return render_template("fee.html", fees=fees, total=total)


# Update amount paid
@app.route("/update", methods=["GET", "POST"])
def update_fee():
    if request.method == "POST":
        fee_id = request.form["Fee_ID"]
        amount_paid = request.form["Amount_Paid"]

        con = db_connect()
        cur = con.cursor()

        cur.execute(
            "UPDATE Fee SET Amount_Paid = %s WHERE Fee_ID = %s",
            (amount_paid, fee_id)
        )

        con.commit()
        cur.close()
        con.close()

        return redirect("/fee")

    return render_template("update.html")


# Delete fee record
@app.route("/delete", methods=["GET", "POST"])
def delete_fee():
    if request.method == "POST":
        fee_id = request.form["Fee_ID"]

        con = db_connect()
        cur = con.cursor()

        cur.execute("DELETE FROM Fee WHERE Fee_ID = %s", (fee_id,))

        con.commit()
        cur.close()
        con.close()

        return redirect("/fee")

    return render_template("delete.html")


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
