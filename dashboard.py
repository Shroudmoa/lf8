from flask import Flask, render_template_string, request
import mariadb

# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

# =========================================================
# DATENBANKVERBINDUNG
# =========================================================

try:

    db = mariadb.connect(
        host="192.168.0.79",
        user="root",
        password="vm",
        database="Heiner_IT"
    )

    print("MariaDB verbunden!")

except mariadb.Error as e:

    print("Fehler:", e)

# =========================================================
# HTML TEMPLATE
# =========================================================

HTML = """

<!DOCTYPE html>
<html lang="de">
<head>

    <meta charset="UTF-8">

    <title>Heiner IT Dashboard</title>

    <style>

        body {
            font-family: Arial;
            background-color: #ecf0f1;
            margin: 30px;
        }

        h1 {
            color: #2c3e50;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }

        th {
            background: #3498db;
            color: white;
            padding: 10px;
        }

        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }

        tr:hover {
            background: #f5f5f5;
        }

        .search-box {
            margin-bottom: 20px;
        }

        input[type=text] {
            padding: 10px;
            width: 300px;
        }

        button {
            padding: 10px;
            background: #27ae60;
            color: white;
            border: none;
            cursor: pointer;
        }

    </style>

</head>

<body>

    <h1>📊 Heiner IT Kunden-Dashboard</h1>

    <form method="GET">

        <div class="search-box">

            <input
                type="text"
                name="search"
                placeholder="Firma oder Ort suchen..."
                value="{{ search }}"
            >

            <button type="submit">
                Suchen
            </button>

        </div>

    </form>

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

            <td>{{ kunde[0] }}</td>
            <td>{{ kunde[1] }}</td>
            <td>{{ kunde[2] }}</td>
            <td>{{ kunde[3] }}</td>
            <td>{{ kunde[4] }}</td>

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

    search = request.args.get("search", "")

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
            WHERE
                Firma LIKE ?
                OR Ort LIKE ?
            ORDER BY Firma
        """, (
            f"%{search}%",
            f"%{search}%"
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
        host="0.0.0.0",
        port=5000
    )
