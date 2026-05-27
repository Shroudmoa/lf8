from flask import Flask, render_template_string, request
import mariadb

app = Flask(__name__)

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
# HTML
# =========================================================

HTML = """

<!DOCTYPE html>
<html>

<head>

<title>Heiner IT Dashboard</title>

<style>

body{
font-family:Arial;
background:#ecf0f1;
padding:30px;
}

table{
width:100%;
border-collapse:collapse;
background:white;
}

th{
background:#3498db;
color:white;
padding:10px;
}

td{
padding:10px;
border-bottom:1px solid #ddd;
}

input{
padding:10px;
width:300px;
}

button{
padding:10px;
background:#27ae60;
color:white;
border:none;
}

</style>

</head>

<body>

<h1>📊 Kunden Dashboard</h1>

<form>

<input
type="text"
name="search"
placeholder="Firma suchen..."
value="{{search}}"
>

<button type="submit">
Suchen
</button>

</form>

<br>

<table>

<tr>

<th>KundenCode</th>
<th>Firma</th>
<th>Kontaktperson</th>
<th>Ort</th>
<th>Telefon</th>

</tr>

{% for kunde in kunden %}

<tr>

<td>{{kunde[0]}}</td>
<td>{{kunde[1]}}</td>
<td>{{kunde[2]}}</td>
<td>{{kunde[3]}}</td>
<td>{{kunde[4]}}</td>

</tr>

{% endfor %}

</table>

</body>
</html>

"""

# =========================================================
# ROUTE
# =========================================================

@app.route("/")
def index():

    search = request.args.get(
        "search",
        ""
    )

    cursor = db.cursor()

    if search:

        cursor.execute("""
            SELECT
                KundenCode,
                Firma,
                Kontaktperson,
                Ort,
                Telefon
            FROM kunde
            WHERE Firma LIKE ?
            ORDER BY Firma
        """, (
            f"%{search}%",
        ))

    else:

        cursor.execute("""
            SELECT
                KundenCode,
                Firma,
                Kontaktperson,
                Ort,
                Telefon
            FROM kunde
            ORDER BY Firma
        """)

    kunden = cursor.fetchall()

    cursor.close()

    return render_template_string(
        HTML,
        kunden=kunden,
        search=search
    )

# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
