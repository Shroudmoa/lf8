from flask import Flask, render_template_string, request, redirect, session
import mariadb
from datetime import datetime
import hashlib

# starting the flask app and setting the secret key for seesion management.
app = Flask(__name__)
app.secret_key = "heiner_secret_key" #supersecret btw


# Datenbankverbindung aufbauen
db = mariadb.connect(
    host="10.145.240.127",
    user="root",
    password="123",
    database="Heiner_IT"
)


# USERS / ROLES --- passworts werden gehasht gespeichert


users = {
    "Lager": hashlib.sha256("Lager".encode()).hexdigest(),
    "Verwaltung": hashlib.sha256("Verwaltung".encode()).hexdigest(),
    "Marketing": hashlib.sha256("Marketing".encode()).hexdigest(),
    "Geschäftsführung": hashlib.sha256("Geschäftsführung".encode()).hexdigest()
}


# LOGGING the logins and also logouts


def log_event(user, status):
    with open("login_log.txt", "a") as f:
        f.write(f"{datetime.now()} | {user} | {status}\n")


# LOGIN HTML => nur die Users aus der Users Dictionary dürfen sich anmelden und nur GF darf Kunden "verwalten"
#die Anderen Abteilungen können aus Testzwecken das Dashboard aufrufen aber keine Änderung vornehmen. 
# Alle Login Versuche werden auch in einer Textdatei gespeichert. 


LOGIN_HTML = """
<h2>DB-Verwaltung Login</h2>

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
#so hier haben wir get und post methods für login und passworter werden weiterhin gehasht verglichen.
#Falls der Login Erfolgreich wäre, wird session gespeichert und an Dashboard html weitergeleitet. 
#falls der Logiin fehlschlägt wird ne Meldung gezeigt und auch im logfile gespeichert
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


# DASHBOARD
#simple html mit sstatisken und kundenliste. GF darf wie schon erwähnt kunden bearbeiten hinzufügen und löschen.

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
    <a href="/delete/{{k[0]}}">Löschen</a>
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
#hier unter app.route dashboard haben wir die Logig für Anzeige der Infos und Kundenliste  + Search Func und einfach alles.
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


# ADD CUSTOMER
#nur GF darf kunden hinzufügen. und hier mit /add und Methode Post kann man einfach neue Kunden Hinzüfügen.

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


# DELETE CUSTOMER

#hier mit /delete kann der User (GF nur). Es wird Kunden code verwendet und auch nicht verwendet. in Web hat man einfach einen Knüpf.
# # aber diese Funktion kann ja auch in Zukunft nach Code fragen. (am Ende geändert deswegen...)  
@app.route("/delete/<code>")
def delete(code):

    if "user" not in session or session["user"] != "Geschäftsführung":
        return "Zugriff verweigert! Nur Geschäftsführung.", 403

    cursor = db.cursor()
    cursor.execute("DELETE FROM kunde WHERE KundenCode = ?", (code,))
    db.commit()
    cursor.close()

    return redirect("/dashboard")


# EDIT CUSTOMER
#wieder alles wie hinzüfügen. Kunden Code bleibt das Selbe beim bearbeiten, den Rest kann man ja ändern.  

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


# LOGOUT

#easy logout funktion. Session wird bei Logout gelöscht und dokumentiert
@app.route("/logout")
def logout():
    session.pop("user", None)
    #return to login page
    return redirect("/")


# RUN
#man kann die App hier mit debug mode starten  und das machen wir bis das Progeramm fertig ist 
#0.0.0.0 => erreichbar im Netzwerk und Port default 5000 aber bei mir LOKAL war 5000 belegt^^
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
