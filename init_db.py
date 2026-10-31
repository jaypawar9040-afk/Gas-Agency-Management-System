from app import db, User
from werkzeug.security import generate_password_hash

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        mobile TEXT,
        pincode TEXT,
        email TEXT UNIQUE,
        password TEXT,
        date TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        cylinder_type TEXT,
        address TEXT,
        status TEXT,
        date TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS contact_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT,
        date TEXT
    )''')

    conn.commit()
    conn.close()


def seed():
    db.create_all()
    if not User.query.filter_by(email='admin@example.com').first():
        admin = User(
            name='Admin',
            address='HQ',
            mobile='9999999999',
            pincode='000000',
            email='admin@example.com',
            password_hash=generate_password_hash('Admin@1234'), # must be 10 chars? this is 10 with mix
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created: admin@example.com / Admin@1234")

if __name__ == '__main__':
    seed()
