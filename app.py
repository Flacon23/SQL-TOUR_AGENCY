from flask import Flask, render_template, request, redirect, url_for
from database import engine
from sqlalchemy import text

app = Flask(__name__)


def load_tur():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM Tur"))
        result_all = []
        rows = result.fetchall()
        for row in rows:
            result_all.append(row)
        return result_all


def load_ghid():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM Ghid"))
        result_all = []
        rows = result.fetchall()
        for row in rows:
            result_all.append(row)
        return result_all


def load_destinatie():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM Destinatie"))
        result_all = []
        rows = result.fetchall()
        for row in rows:
            result_all.append(row)
        return result_all


def load_plate():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM Plate"))
        result_all = []
        rows = result.fetchall()
        for row in rows:
            result_all.append(row)
        return result_all


def load_rezervare():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM Rezervare"))
        result_all = []
        rows = result.fetchall()
        for row in rows:
            result_all.append(row)
        return result_all


def load_plecare():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM Plecare"))
        result_all = []
        rows = result.fetchall()
        for row in rows:
            result_all.append(row)
        return result_all


# Funcții pentru încărcare date
def load_turisti():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM Turisti"))
        result_all = []
        rows = result.fetchall()
        for row in rows:
            result_all.append(row)
        return result_all


@app.route('/turisti')
def turisti():
    turisti = load_turisti()
    return render_template('turisti.html', turisti=turisti)


# Funcție pentru adăugare turist
@app.route('/turisti/add', methods=['POST'])
def add_turist():
    nume = request.form['nume']
    prenume = request.form['prenume']
    email = request.form['email']
    sex = request.form['sex']
    telefon = request.form['telefon']
    cnp = request.form['cnp']

    with engine.connect() as conn:
        conn.execute(
            text(
                """INSERT INTO Turisti (nume, prenume, email,sex, telefon,cnp) VALUES (:nume, :prenume, :email,:sex, :telefon,:cnp)"""
            ), {
                "nume": nume,
                "prenume": prenume,
                "email": email,
                "sex": sex,
                "telefon": telefon,
                "cnp": cnp
            })
        conn.commit()
    return redirect(url_for('turisti'))


# Funcție pentru ștergere turist
@app.route('/turisti/delete/<int:id_turist>', methods=['POST'])
def delete_turist(id_turist):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM Turisti WHERE id_turist = :id_turist"),
                     {"id_turist": id_turist})
        conn.commit()
    return redirect(url_for('turisti'))


@app.route('/turisti/update/<int:id_turist>', methods=['POST'])
def update_turist(id_turist):
    # Preluăm datele din formular
    nume = request.form['nume']
    prenume = request.form['prenume']
    email = request.form['email']
    telefon = request.form['telefon']
    sex = request.form['sex']
    cnp = request.form['cnp']

    # Actualizăm în baza de date
    with engine.connect() as conn:
        conn.execute(
            text("""
            UPDATE Turisti
            SET nume = :nume, prenume = :prenume, email = :email, telefon = :telefon,
                sex = :sex, cnp = :cnp
            WHERE id_turist = :id_turist
        """), {
                "nume": nume,
                "prenume": prenume,
                "email": email,
                "telefon": telefon,
                "sex": sex,
                "cnp": cnp,
                "id_turist": id_turist
            })
        conn.commit()
    return redirect(url_for('turisti'))


# Rute existente
@app.route('/')
def login():
    return render_template('login.html')


@app.route('/query/tours-with-guides')
def query_tours_with_guides():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
            SELECT Tr.nume_tur AS "Tour Name", G.nume_ghid AS "Guide Name", G.prenume_ghid AS "Guide Surname"
            FROM Tur Tr
            JOIN Ghid G ON Tr.id_ghid = G.id_ghid
        """))
        rows = result.fetchall()
    return render_template(
        'query_result.html',
        title='Tours with Guides',
        rows=rows,
        headers=['Tour Name', 'Guide Name', 'Guide Surname'])


@app.route('/query/payments-by-method/<payment_method>')
def payments_by_method(payment_method):
    with engine.connect() as conn:
        result = conn.execute(
            text("""SELECT DISTINCT
    t.id_tur AS id_tur, 
    t.nume_tur AS nume_tur, 
    tr.id_turist AS id_turist, 
    tr.nume AS nume_turist, 
    tr.prenume AS prenume_turist, 
    p.metoda_platii AS metoda_platii
FROM Tur t
JOIN Rezervare r ON t.id_tur = r.id_tur
JOIN Turisti tr ON r.id_turist = tr.id_turist
JOIN Plate p ON r.id_plata = p.id_plata
WHERE p.metoda_platii = :payment_method
ORDER BY t.id_tur, tr.nume, tr.prenume;
"""), {"payment_method": payment_method})
        rows = result.fetchall()
    return render_template('query_result.html', 
                         title=f"Tourists paying with {payment_method}", 
                         rows=rows,
                         headers=['id_tur','nume_tur','id_turist','nume_turist','prenume_turist','metoda_platii'])


@app.route('/query/destination-tours/<int:min_duration>')
def query_destination_tours(min_duration):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
            SELECT D.nume_destinatie AS "Destination Name", 
                   Tr.nume_tur AS "Tour Name",
                   Tr.durata AS "Duration"
            FROM Destinatie D
            JOIN Tur Tr ON D.id_destinatie = Tr.id_destinatie
            WHERE Tr.durata >= :min_duration
            ORDER BY Tr.durata
        """), {"min_duration": min_duration})
        rows = result.fetchall()
    return render_template('query_result.html',
                         title=f'Destinations and Tours (Min Duration: {min_duration} days)',
                         rows=rows,
                         headers=['Destination Name', 'Tour Name', 'Duration'])


@app.route('/query/departures-with-details')
def query_departures_with_details():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
            SELECT Tr.nume_tur AS "Tour Name", P.ora_plecare AS "Departure Time", P.loc_plecare AS "Departure Location"
            FROM Tur Tr
            JOIN Plecare P ON Tr.id_plecare = P.id_plecare
        """))
        rows = result.fetchall()
    return render_template(
        'query_result.html',
        title='Departure Schedule Details',
        rows=rows,
        headers=['Tour Name', 'Departure Time', 'Departure Location'])


@app.route('/query/payments-by-tour')
def query_payments_by_tour():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
            SELECT Tr.nume_tur AS "Tour Name", SUM(P.suma) AS "Total Payments"
            FROM Tur Tr
            JOIN Rezervare R ON Tr.id_tur = R.id_tur
            JOIN Plate P ON R.id_plata = P.id_plata
            GROUP BY Tr.nume_tur
        """))
        rows = result.fetchall()
    return render_template('query_result.html',
                           title='Payments by Tour',
                           rows=rows,
                           headers=['Tour Name', 'Total Payments'])


@app.route('/query/popular-destinations')
def popular_destinations():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
            SELECT d.nume_destinatie, COUNT(r.id_plata) AS total_rezervari
FROM Destinatie d
JOIN Tur t ON d.id_destinatie = t.id_destinatie
JOIN Rezervare r ON t.id_tur = r.id_tur
GROUP BY d.nume_destinatie
ORDER BY total_rezervari DESC;
        """))
        rows = result.fetchall()
    return render_template('query_result.html',
                           title="Popular Destinations",
                           rows=rows,
                           headers=['nume_destinatie', 'total_rezervari'])

@app.route('/query/Tururi-eficiente')
def Tururi_eficiente():
    with engine.connect() as conn:
        result = conn.execute(
            text("""SELECT 
    t.nume_tur,
    t.durata,
    COUNT(r.id_rezervare) as numar_rezervari,
    SUM(p.suma) as venit_total,
    SUM(p.suma) / t.durata as venit_per_zi,
    AVG(r.nr_locuri_rezervate) as medie_locuri_per_rezervare
FROM Tur t
JOIN Rezervare r ON t.id_tur = r.id_tur
JOIN Plate p ON r.id_plata = p.id_plata
GROUP BY t.id_tur, t.nume_tur, t.durata
HAVING (SUM(p.suma) / t.durata) > (
    SELECT AVG(venit_per_zi)
    FROM (
        SELECT SUM(p2.suma) / t2.durata as venit_per_zi
        FROM Tur t2
        JOIN Rezervare r2 ON t2.id_tur = r2.id_tur
        JOIN Plate p2 ON r2.id_plata = p2.id_plata
        GROUP BY t2.id_tur, t2.durata
    ) sub
)
ORDER BY venit_per_zi DESC;"""))
        rows = result.fetchall()
    return render_template('query_result.html', title="Tururi eficiente", rows=rows,headers=['nume_tur', 'durata', 'numar_rezervari', 'venit_total','venit_per_zi','medie_locuri_per_rezervare'])

@app.route('/query/top-guides')
def top_guides():
    with engine.connect() as conn:
        result = conn.execute(
            text("""SELECT g.nume_ghid, g.prenume_ghid, 
                   SUM(p.suma) as venit_total
            FROM Ghid g
            JOIN Tur t ON g.id_ghid = t.id_ghid
            JOIN Rezervare r ON t.id_tur = r.id_tur
            JOIN Plate p ON r.id_plata = p.id_plata
            GROUP BY g.id_ghid, g.nume_ghid, g.prenume_ghid
            HAVING SUM(p.suma) > (
                SELECT AVG(venit_per_ghid)
                FROM (
                    SELECT SUM(p2.suma) as venit_per_ghid
                    FROM Ghid g2
                    JOIN Tur t2 ON g2.id_ghid = t2.id_ghid
                    JOIN Rezervare r2 ON t2.id_tur = r2.id_tur
                    JOIN Plate p2 ON r2.id_plata = p2.id_plata
                    GROUP BY g2.id_ghid
                ) as avg_venituri
            )
            ORDER BY venit_total DESC"""))
        rows = result.fetchall()
    return render_template('query_result.html', title="Top Guides", rows=rows,headers=['nume_ghid', 'prenume_ghid', 'total_rezervari'])

@app.route('/query/top-tours')
def top_tours():
    with engine.connect() as conn:
        result = conn.execute(
            text("""SELECT t.nume_tur, SUM(p.suma) AS venit_total
FROM Tur t
JOIN Rezervare r ON t.id_tur = r.id_tur
JOIN Plate p ON r.id_plata = p.id_plata
GROUP BY t.id_tur, t.nume_tur
HAVING venit_total > (
    SELECT AVG(venit_total_tur) 
    FROM (
        SELECT SUM(p2.suma) AS venit_total_tur
        FROM Tur t2
        JOIN Rezervare r2 ON t2.id_tur = r2.id_tur
        JOIN Plate p2 ON r2.id_plata = p2.id_plata
        GROUP BY t2.id_tur
    ) AS venituri
)
ORDER BY venit_total DESC;
"""))
        rows = result.fetchall()
    return render_template('query_result.html', title="Top Tours", rows=rows,headers=['nume_tur','venit_total'])

@app.route('/query/card-payments')
def card():
    with engine.connect() as conn:
        result = conn.execute(
            text("""SELECT DISTINCT
    t.id_tur AS id_tur,
    t.nume_tur AS nume_tur,
    tr.id_turist AS id_turist,
    tr.nume AS nume_turist,
    tr.prenume AS prenume_turist,
    p.metoda_platii AS metoda_platii
FROM Tur t
JOIN (
    SELECT r.id_tur, r.id_turist, r.id_plata
    FROM Rezervare r
    WHERE r.id_plata IN (
        SELECT p.id_plata
        FROM Plate p
        WHERE p.metoda_platii = 'Card'
    )
) r_filtered ON t.id_tur = r_filtered.id_tur
JOIN Turisti tr ON r_filtered.id_turist = tr.id_turist
JOIN Plate p ON r_filtered.id_plata = p.id_plata
ORDER BY t.id_tur, tr.nume, tr.prenume;
"""))
        rows = result.fetchall()
    return render_template('query_result.html', title="Card Tourists", rows=rows,headers=['id_tur','nume_tur','id_turist','nume_turist','prenume_turist','metoda_platii'])


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/ghid')
def ghid():
    ghid = load_ghid()
    return render_template('ghid.html', ghid=ghid)


@app.route('/plate')
def plate():
    plate = load_plate()
    return render_template('plate.html', plate=plate)


@app.route('/destinatie')
def destinatie():
    destinatie = load_destinatie()
    return render_template('destinatie.html', destinatie=destinatie)


@app.route('/tur')
def tur():
    tur = load_tur()
    return render_template('tur.html', tur=tur)


@app.route('/rezervare')
def rezervare():
    rezervare = load_rezervare()
    return render_template('rezervare.html', rezervare=rezervare)


@app.route('/plecare')
def plecare():
    plecare = load_plecare()
    return render_template('plecare.html', plecare=plecare)


@app.route('/plecare/add', methods=['POST'])
def add_plecare():
    ora_plecare = request.form['ora_plecare']
    loc_plecare = request.form['loc_plecare']
    observatii_plecare = request.form['observatii_plecare']

    with engine.connect() as conn:
        conn.execute(
            text("""
            INSERT INTO Plecare (ora_plecare, loc_plecare, observatii_plecare)
            VALUES (:ora_plecare, :loc_plecare, :observatii_plecare)
            """), {
                "ora_plecare": ora_plecare,
                "loc_plecare": loc_plecare,
                "observatii_plecare": observatii_plecare
            })
        conn.commit()
    return redirect(url_for('plecare'))


@app.route('/plecare/delete/<int:id_plecare>', methods=['POST'])
def delete_plecare(id_plecare):
    with engine.connect() as conn:
        conn.execute(
            text("DELETE FROM Plecare WHERE id_plecare = :id_plecare"),
            {"id_plecare": id_plecare})
        conn.commit()
    return redirect(url_for('plecare'))


@app.route('/plecare/update/<int:id_plecare>', methods=['POST'])
def update_plecare(id_plecare):
    ora_plecare = request.form['ora_plecare']
    loc_plecare = request.form['loc_plecare']
    observatii_plecare = request.form['observatii_plecare']

    with engine.connect() as conn:
        conn.execute(
            text("""
            UPDATE Plecare
            SET ora_plecare = :ora_plecare,
                loc_plecare = :loc_plecare,
                observatii_plecare = :observatii_plecare
            WHERE id_plecare = :id_plecare
            """), {
                "ora_plecare": ora_plecare,
                "loc_plecare": loc_plecare,
                "observatii_plecare": observatii_plecare,
                "id_plecare": id_plecare
            })
        conn.commit()
    return redirect(url_for('plecare'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
