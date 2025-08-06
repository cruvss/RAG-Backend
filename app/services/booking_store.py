import sqlite3
from app.config import DB_PATH
from app.models.schemas import BookingRequest

def save_booking(booking: BookingRequest):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                date TEXT,
                time TEXT
            )
        ''')
        cursor.execute('''
            INSERT INTO bookings (name, email, date, time)
            VALUES (?, ?, ?, ?)
        ''', (booking.name, booking.email, booking.date, booking.time))
        conn.commit()
