from flask import Flask, render_template_string, request, redirect, session
import mariadb
from datetime import datetime
import hashlib

app = Flask(__name__)
app.secret_key = "heiner_secret_key"

# =========================================================
# DATABASE
# =========================================================

db = mariadb.connect(
    host="192.168.0.79",
    user="root",
    password="vm",
    database="Heiner_IT"
)

# =========================================================
# USERS / ROLES
# =========================================================

users = {
    "Lager": hashlib.sha256("Lager".encode()).hexdigest(),
    "Verwaltung": hashlib.sha256("Verwaltung".encode()).hexdigest(),
    "Marketing": hashlib.sha256("Marketing".encode()).hexdigest(),
    "Geschäftsführung": hashlib.sha256("Geschäftsführung".encode()).hexdigest()
}

# =========================================================
# LOGGING
# =========================================================

def log_event(user, status):
    with open("login_log.txt", "a") as f:
        f.write(f"{datetime.now()} | {user} | {status}\n")

# =========================================================
# LOGIN
# =========================================================

LOGIN_HTML = """
<h2>Login</h2>

<form method="POST">
    <select name="user">
        {% for u in users %}
        <option value="{{u}}">{{u}}</option>
        {% endfor %}
    </select>

    <input type="password" name="password" placeholder="Passwort">
    <button>Login</button>
</form>

<p style="color:red">{{error}}</p>
"""

@app.route("/", methods=["GET", "POST"])
def login():

    error = ""

    if request.method == "POST":

        user = request.form["user"]
        password = request.form["password"]

        hashed = hashlib.sha256(password.encode()).hexdigest()

        if user in users and users[user] == hashed:

            session["user"] = user
            log_event(user, "LOGIN OK")
            return redirect("/dashboard")

        else:
            log_event(user, "LOGIN FAIL")
            error = "Falsches Passwort"

    return render_template_string(LOGIN_HTML, users=users.keys(), error=error)

# =========================================================
# DASHBOARD
# =========================================================

DASHBOARD_HTML = """
<h2>Dashboard - {{user}}</h2>

<a href="/logout">Logout</a>

<hr>

<h3>Statistiken</h3>
<ul>
<li>Kunden: {{kunden_count}}</li>
<li>Artikel: {{artikel_count}}</li>
<li>Lieferanten: {{lieferanten_count}}</li>
</ul>

<hr>

{% if user == "Geschäftsführung" %}
<h3>Kunde hinzufügen</h3>

<form method="POST" action="/add">
    <input name="code" placeholder="Code" required>
    <input name="firma" placeholder="Firma" required>
    <input name="kontakt" placeholder="Kontakt">
    <input name="ort" placeholder="Ort">
    <input name="telefon" placeholder="Telefon">
    <button>Hinzufügen</button>
</form>
{% endif %}

<hr>

<h3>Kundenliste</h3>

<form method="GET">
    <input name="search" placeholder="Suche Firma..." value="{{search}}">
    <button>Suchen</button>
</form>

<table border="1" cellpadding="5">
<tr>
<th>Code</th>
<th>Firma</th>
<th>Kontakt</th>
<th>Ort</th>
<th>Telefon</th>
{% if user == "Geschäftsführung" %}
<th>Aktionen</th>
{% endif %}
</tr>

{% for k in kunden %}
<tr>
<td>{{k[0]}}</td>
<td>{{k[1]}}</td>
<td>{{k[2]}}</td>
<td>{{k[3]}}</td>
<td>{{k[4]}}</td>

{% if user == "Geschäftsführung" %}
<td>
    <a href="/delete/{{k[0]}}">❌ Löschen</a>
</td>
{% endif %}
</tr>
{% endfor %}
</table>

{% if user == "Geschäftsführung" %}
<hr>

<h3>Kunde bearbeiten</h3>

<form method="POST" action="/edit">
    <input name="code" placeholder="Code (zum Bearbeiten)" required>
    <input name="firma" placeholder="Firma">
    <input name="kontakt" placeholder="Kontakt">
    <input name="ort" placeholder="Ort">
    <input name="telefon" placeholder="Telefon">
    <button>Update</button>
</form>
{% endif %}
"""

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    search = request.args.get("search", "")

    cursor = db.cursor()

    # STATS
    cursor.execute("SELECT COUNT(*) FROM kunde")
    kunden_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM artikel")
    artikel_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM lieferant")
    lieferanten_count = cursor.fetchone()[0]

    # CUSTOMER LIST
    if search:
        cursor.execute("""
            SELECT KundenCode, Firma, Kontaktperson, Ort, Telefon
            FROM kunde
            WHERE Firma LIKE ?
        """, (f"%{search}%",))
    else:
        cursor.execute("""
            SELECT KundenCode, Firma, Kontaktperson, Ort, Telefon
            FROM kunde
        """)

    kunden = cursor.fetchall()
    cursor.close()

    return render_template_string(
        DASHBOARD_HTML,
        user=session["user"],
        kunden=kunden,
        kunden_count=kunden_count,
        artikel_count=artikel_count,
        lieferanten_count=lieferanten_count,
        search=search
    )

# =========================================================
# ADD CUSTOMER
# =========================================================

@app.route("/add", methods=["POST"])
def add():

    if "user" not in session or session["user"] != "Geschäftsführung":
        return "Zugriff verweigert! Nur Geschäftsführung.", 403

    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO kunde (KundenCode, Firma, Kontaktperson, Ort, Telefon)
        VALUES (?, ?, ?, ?, ?)
    """, (
        request.form["code"],
        request.form["firma"],
        request.form["kontakt"],
        request.form["ort"],
        request.form["telefon"]
    ))

    db.commit()
    cursor.close()

    return redirect("/dashboard")

# =========================================================
# DELETE CUSTOMER
# =========================================================

@app.route("/delete/<code>")
def delete(code):

    if "user" not in session or session["user"] != "Geschäftsführung":
        return "Zugriff verweigert! Nur Geschäftsführung.", 403

    cursor = db.cursor()
    cursor.execute("DELETE FROM kunde WHERE KundenCode = ?", (code,))
    db.commit()
    cursor.close()

    return redirect("/dashboard")

# =========================================================
# EDIT CUSTOMER
# =========================================================

@app.route("/edit", methods=["POST"])
def edit():

    if "user" not in session or session["user"] != "Geschäftsführung":
        return "Zugriff verweigert! Nur Geschäftsführung.", 403

    cursor = db.cursor()

    cursor.execute("""
        UPDATE kunde
        SET Firma=?, Kontaktperson=?, Ort=?, Telefon=?
        WHERE KundenCode=?
    """, (
        request.form["firma"],
        request.form["kontakt"],
        request.form["ort"],
        request.form["telefon"],
        request.form["code"]
    ))

    db.commit()
    cursor.close()

    return redirect("/dashboard")

# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
