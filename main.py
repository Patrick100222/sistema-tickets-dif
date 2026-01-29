from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Crear base de datos y tabla
def crear_bd():
    conexion = sqlite3.connect("tickets.db")
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        area TEXT,
        problema TEXT,
        fecha TEXT,
        estado TEXT,
        observaciones TEXT,
        complejidad TEXT
    )
    """)
    conexion.commit()
    conexion.close()


crear_bd()

# Página principal (crear ticket)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form["nombre"]
        area = request.form["area"]
        problema = request.form["problema"]
        estado = "Abierto"
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

        conexion = sqlite3.connect("tickets.db")
        cursor = conexion.cursor()
        cursor.execute("""
        INSERT INTO tickets (nombre, area, problema, estado, fecha)
        VALUES (?, ?, ?, ?, ?)
        """, (nombre, area, problema, estado, fecha))
        conexion.commit()
        conexion.close()

        return redirect("/tickets")

    return render_template("index.html")

# Ver tickets
@app.route("/tickets")
def ver_tickets():
    conexion = sqlite3.connect("tickets.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()
    conexion.close()

    return render_template("tickets.html", tickets=tickets)

# Cerrar ticket
@app.route("/cerrar/<int:id>", methods=["GET", "POST"])
def cerrar_ticket(id):
    conexion = sqlite3.connect("tickets.db")
    cursor = conexion.cursor()

    if request.method == "POST":
        observaciones = request.form["observaciones"]
        complejidad = request.form["complejidad"]

        cursor.execute("""
        UPDATE tickets
        SET estado = 'Cerrado',
            observaciones = ?,
            complejidad = ?
        WHERE id = ?
        """, (observaciones, complejidad, id))

        conexion.commit()
        conexion.close()
        return redirect("/tickets")

    conexion.close()
    return render_template("cerrar_ticket.html", ticket_id=id)

@app.route("/dashboard")
def dashboard():
    conexion = sqlite3.connect("tickets.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM tickets")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE estado='Abierto'")
    abiertos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE estado='Cerrado'")
    cerrados = cursor.fetchone()[0]

    cursor.execute("""
        SELECT complejidad, COUNT(*)
        FROM tickets
        WHERE complejidad IS NOT NULL
        GROUP BY complejidad
    """)
    complejidades = cursor.fetchall()

    conexion.close()

    return render_template(
        "dashboard.html",
        total=total,
        abiertos=abiertos,
        cerrados=cerrados,
        complejidades=complejidades
    )


if __name__ == "__main__":
    app.run(debug=True)

