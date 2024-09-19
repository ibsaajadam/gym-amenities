import sqlite3
from flask import Flask, jsonify, render_template

app = Flask(__name__)

def get_gym_amenities():
    conn = sqlite3.connect('gym.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, quantity FROM amenities")
    amenities = cursor.fetchall()
    conn.close()
    return {amenity[0]: amenity[1] for amenity in amenities}

def get_court_availability():
    conn = sqlite3.connect('gym.db')
    cursor = conn.cursor()
    cursor.execute("SELECT court_name, availability FROM courts")
    courts = cursor.fetchall()
    conn.close()
    return {court[0]: court[1] for court in courts}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/amenities', methods=['GET'])
def amenities():
    amenities_data = get_gym_amenities()
    return render_template('amenities.html', amenities=amenities_data)

@app.route('/courts', methods=['GET'])
def courts():
    courts_data = get_court_availability()
    return render_template('courts.html', courts=courts_data)

if __name__ == '__main__':
    conn = sqlite3.connect('gym.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS amenities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        court_name TEXT NOT NULL,
        availability TEXT NOT NULL
    )
    ''')

    cursor.execute("SELECT COUNT(*) FROM amenities")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO amenities (name, quantity) VALUES ('Treadmills', 14)")
        cursor.execute("INSERT INTO amenities (name, quantity) VALUES ('Bench Presses', 10)")
        cursor.execute("INSERT INTO amenities (name, quantity) VALUES ('Basketball Courts', 2)")
        cursor.execute("INSERT INTO amenities (name, quantity) VALUES ('Olympic Pool', 1)")
        cursor.execute("INSERT INTO amenities (name, quantity) VALUES ('Boxing Gym', 1)")
        cursor.execute("INSERT INTO amenities (name, quantity) VALUES ('Tennis Courts', 2)")

    cursor.execute("SELECT COUNT(*) FROM courts")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO courts (court_name, availability) VALUES ('Basketball Court 1', 'available')")
        cursor.execute("INSERT INTO courts (court_name, availability) VALUES ('Basketball Court 2', 'booked')")
        cursor.execute("INSERT INTO courts (court_name, availability) VALUES ('Tennis Court 1', 'available')")
        cursor.execute("INSERT INTO courts (court_name, availability) VALUES ('Tennis Court 2', 'booked')")
        cursor.execute("INSERT INTO courts (court_name, availability) VALUES ('Handball Court', 'available')")

    conn.commit()
    conn.close()

    app.run(debug=True)
