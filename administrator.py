from database import conn, cursor
import hashlib
from booking import booking_menu, delete_booking, list_organization_bookings
from datetime import datetime
import re

def administrator_actions():
    while True:
        print("Options for Administrator:")
        print("1. Add Floor and Room Details")
        print("2. Register New Organization")
        print("3. Register New User")
        print("4. List Conference Rooms")
        print("5. Book Room")
        print("6. Cancel Booking")
        print("7. List User/Organization Bookings")
        print("8. Logout")

        option = input("Enter your choice: ")

        if option == '1':
            add_floor_or_rooms()
        elif option == '2':
            register_new_organization()
        elif option == '3':
            register_new_user()
        elif option == '4':
            list_conference_rooms()
        elif option == '5':
            book_room_as_admin()
        elif option == '6':
            cancel_booking_as_admin()
        elif option == '7':
            list_booking_for_admin()
        elif option == '8':
            print("Logging out...")
            break;
        else:
            print("Invalid option.")


def add_floor_or_rooms():
    while True:
        print("Options for adding floors and rooms:")
        print("1. Add a new floor")
        print("2. Add rooms to an existing floor")
        print("3. Back to main menu")

        option = input("Enter your choice: ")

        if option == '1':
            cursor.execute("INSERT INTO Floors DEFAULT VALUES")
            conn.commit()

            cursor.execute("SELECT last_insert_rowid()")
            floor_id = cursor.fetchone()[0]

            print(f"New floor '{floor_id}' added successfully!")

            add_rooms_to_floor(floor_id)
        elif option == '2':
            print("Available Floors:")
            cursor.execute("SELECT floor_id FROM Floors")
            available_floors = cursor.fetchall()
            for floor_id in available_floors:
                print(f"{floor_id}")

            floor_id = input("Select a floor by entering the floor number: ")

            if (int(floor_id),) in available_floors:
                add_rooms_to_floor(floor_id)
            else:
                print("Invalid floor number. Please select an existing floor.")
        elif option == '3':
            print("Returning to the main menu...")
            break
        else:
            print("Invalid option.")


def add_rooms_to_floor(floor_id):
    num_rooms = int(input("Enter the number of rooms to add: "))

    for _ in range(num_rooms):
        room_name = input("Enter the room name: ")
        capacity = int(input("Enter the room capacity: "))

        cursor.execute("INSERT INTO Rooms (floor_id, room_name, capacity) VALUES (?, ?, ?)",
                       (floor_id, room_name, capacity))
        conn.commit()

        print(f"New room '{room_name}' added to floor {floor_id} successfully!")


def register_new_organization():
    org_name = input("Enter the organization name: ")

    while True:
        org_email = input("Enter the org email: ")
        if is_valid_email(org_email):
            break
        else:
            print("Invalid email format. Please enter a valid email address.")

    cursor.execute("INSERT INTO Organizations (org_name, org_email) VALUES (?, ?)",
                   (org_name, org_email))
    conn.commit()

    print(f"New organization '{org_name}' registered successfully!")


def is_valid_email(email):
    # Define a regular expression pattern for a basic email validation
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_pattern, email) is not None


def register_new_user():
    orgs = list_all_organizaztions()

    if not orgs:
        print("No organizations found. Please register an organization first.")
        return

    print("List of Organizations:")
    for org_id, org_name in orgs:
        print(f"{org_id}. {org_name}")

    while True:
        org_id = input("Select an organization by entering its ID: ")

        if org_id.isdigit():
            org_id = int(org_id)
            if any(org_id == org[0] for org in orgs):
                break

        print("Invalid organization ID. Please enter a valid ID from the list.")

    user_name = input("Enter the user name: ")

    while True:
        user_email = input("Enter the user email: ")
        if is_valid_email(user_email):
            break
        else:
            print("Invalid email format. Please enter a valid email address.")

    password = input("Enter the user password: ")
    confirm_password = input("Confirm the user password: ")

    if password != confirm_password:
        print("Passwords do not match. User not registered.")
        return

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute("INSERT INTO Users (org_id, name, email, password, 'role') VALUES (?, ?, ?, ?, ?)",
                   (org_id, user_name, user_email, hashed_password, 'org_admin'))
    conn.commit()

    print(f"New org_admin user '{user_name}' registered successfully!")


def list_conference_rooms():
    print("List Conference Rooms:")
    print("1. Show all rooms with capacity")
    print("2. Show rooms by date")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        cursor.execute("SELECT R.floor_id, R.room_name, R.capacity "
                       "FROM Rooms AS R")
        rooms = cursor.fetchall()

        print("Floor Name  Room Name  Capacity")
        for room in rooms:
            floor_id, room_name, capacity = room
            print(f"Floor {floor_id}  {room_name}  {capacity}")

    elif choice == '2':
        selected_date_str = input("Enter the date (YYYY-MM-DD): ")
        cursor.execute("SELECT R.floor_id, R.room_name, R.capacity, "
                       "CASE WHEN B.room_id IS NULL THEN 'Not Booked' ELSE 'Booked' END AS status "
                       "FROM Rooms AS R "
                       "LEFT JOIN Bookings AS B ON R.room_id = B.room_id "
                       "AND B.date = ?",
                       (selected_date_str,))
        rooms = cursor.fetchall()

        print("Floor Name  Room Name  Capacity  Status")
        for room in rooms:
            floor_id, room_name, capacity, status = room
            print(f"Floor {floor_id}  {room_name}  {capacity}  {status}")
    else:
        print("Invalid choice.")


def book_room_as_admin():
    orgs = list_all_organizaztions()
    
    if not orgs:
        print("No organizations found. Please create organizations first.")
        return

    print("Available Organizations:")
    for org_id, org_name in orgs:
        print(f"{org_id}. {org_name}")

    while True:
        try:
            selected_org_id = int(input("Enter the ID of the organization you want to book for: "))
            if selected_org_id in [org[0] for org in orgs]:
                booking_menu(selected_org_id)
                return
            else:
                print("Invalid organization ID. Please enter a valid ID.")
        except ValueError:
            print("Invalid input. Please enter a valid organization ID.")


def list_all_organizaztions():
    cursor.execute("SELECT org_id, org_name FROM Organizations")
    orgs = cursor.fetchall()
    return orgs


def cancel_booking_as_admin():
    orgs = list_all_organizaztions()
    
    if not orgs:
        print("No organizations found. Please create organizations first.")
        return

    print("Available Organizations:")
    for org_id, org_name in orgs:
        print(f"{org_id}. {org_name}")
    selected_org_id = input("Enter the ID of the organization you want to book for: ")
    delete_booking(selected_org_id)


def list_booking_for_admin():
    orgs = list_all_organizaztions()
    
    if not orgs:
        print("No organizations found. Please create organizations first.")
        return

    print("Available Organizations:")
    for org_id, org_name in orgs:
        print(f"{org_id}. {org_name}")
    selected_org_id = input("Enter the ID of the organization you want to book for: ")
    org_bookings = list_organization_bookings(selected_org_id)
    if not org_bookings:
        print("No bookings found for your organization.")
        return

    print("Bookings for Your Organization:")
    for i in range(len(org_bookings)):
        booking_info = org_bookings[i]
        booking_id = booking_info[0]
        room_name = booking_info[1]
        date = booking_info[2]
        start_time = booking_info[3]
        end_time = booking_info[4]

        start_time_timestamp = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        formatted_start_time = start_time_timestamp.strftime("%H:%M")

        end_time_timestamp = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        formatted_end_time = end_time_timestamp.strftime("%H:%M")
        
        print(f"{i + 1}. Booking ID: {booking_id}, Room: {room_name}, Date: {date}, Time: {formatted_start_time} - {formatted_end_time}")
