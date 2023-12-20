import sqlite3


conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

def create_organizations_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Organizations (
            org_id INTEGER PRIMARY KEY,
            org_name TEXT,
            org_email TEXT
        )
    ''')


def create_users_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY,
            org_id INTEGER,
            name TEXT,
            email TEXT,
            password TEXT,
            role TEXT,
            permissions TEXT,
            FOREIGN KEY (org_id) REFERENCES Organizations(org_id)
        )
    ''')


def create_floors_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Floors (
            floor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            floor_number INTEGER
        )
    ''')


def create_rooms_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Rooms (
            room_id INTEGER PRIMARY KEY,
            floor_id INTEGER,
            room_name TEXT,
            capacity INTEGER,
            FOREIGN KEY (floor_id) REFERENCES Floors(floor_id)
        )
    ''')


def create_bookings_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bookings (
            booking_id INTEGER PRIMARY KEY,
            org_id INTEGER,
            room_id INTEGER,
            start_time DATETIME,
            end_time DATETIME,
            date Date,
            duration DECIMAL(5, 2),
            FOREIGN KEY (org_id) REFERENCES Organizations(org_id),
            FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
        )
    ''')


def insert_floors_and_rooms():
    cursor.executemany('INSERT INTO Floors (floor_number) VALUES (?)', [(0,), (1,)])
    cursor.executemany('''
        INSERT INTO Rooms (floor_id, room_name, capacity) VALUES (?, ?, ?)
    ''', [
        (1, 'Room A', 10),
        (1, 'Room B', 10),
        (1, 'Room C', 5),
        (1, 'Room D', 4),
        (1, 'Room E', 2),
        (2, 'Room F', 10),
        (2, 'Room G', 10),
        (2, 'Room H', 5),
        (2, 'Room I', 4),
        (2, 'Room J', 2),
    ])


def insert_main_user():
    cursor.executemany('INSERT INTO Users (org_id, name, email, password, role) VALUES (?, ?, ?, ?, ?)', 
        [(0,"Admin","admin@gmail.com", "65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5", "Administrator")])



create_organizations_table()
create_users_table()
create_floors_table()
create_rooms_table()
create_bookings_table()
insert_floors_and_rooms()
insert_main_user()
conn.commit()
