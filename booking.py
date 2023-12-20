from datetime import datetime
from database import conn, cursor

def list_organization_bookings(org_id):
    cursor.execute("""
        SELECT B.booking_id, R.room_name, B.date, B.start_time, B.end_time
        FROM Bookings AS B
        INNER JOIN Rooms AS R ON B.room_id = R.room_id
        WHERE org_id = ? 
    """, (org_id,))
    return cursor.fetchall()


def delete_booking(org_id):
    org_bookings = list_organization_bookings(org_id)

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

    try:
        booking_choice = int(input("Select a booking to delete (enter the corresponding number): "))
        if 1 <= booking_choice <= len(org_bookings):
            booking_id = org_bookings[booking_choice - 1][0]
            start_time = org_bookings[booking_choice - 1][3]

            current_time = datetime.now()
            time_difference = start_time_timestamp - current_time

            if time_difference.total_seconds() < 900:
                print("You can't cancel this booking as it's less than 15 minutes before the start time.")
            else:
                cursor.execute("DELETE FROM Bookings WHERE booking_id = ?", (booking_id,))
                conn.commit()
                print(f"Booking {booking_id} deleted successfully.")
        else:
            print("Invalid choice. Please select a valid booking.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def is_room_available(room_id, start_time, end_time):
    cursor.execute("SELECT COUNT(*) FROM Bookings WHERE room_id = ? AND ((start_time <= ? AND end_time > ?) OR (start_time < ? AND end_time >= ?))",
                   (room_id, start_time, start_time, end_time, end_time))
    return cursor.fetchone()[0] == 0


def get_organization_monthly_booking_hours(org_id):
    cursor.execute("SELECT SUM(end_time - start_time) FROM Bookings "
                   "WHERE Users.org_id = ?", (org_id,))
    total_hours = cursor.fetchone()[0]
    return total_hours if total_hours is not None else 0


def list_available_rooms(criteria_capacity, start_time_str, end_time_str, selected_date_str):
    start_time = datetime.strptime(start_time_str, "%H:%M")
    end_time = datetime.strptime(end_time_str, "%H:%M")
    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d")

    cursor.execute("""
        SELECT R.room_id, R.floor_id, R.room_name, R.capacity
        FROM Rooms AS R
        WHERE R.capacity = ? AND
              R.room_id NOT IN (
                SELECT B.room_id
                FROM Bookings AS B
                WHERE B.date = ? AND (
                    (B.start_time <= ? AND B.end_time > ?) OR
                    (B.start_time < ? AND B.end_time >= ?)
                )
              )
    """, (criteria_capacity, selected_date, end_time, start_time, start_time, end_time))

    exact_capacity_rooms = cursor.fetchall()

    if not exact_capacity_rooms:
        cursor.execute("""
        SELECT R1.room_id, R1.floor_id, R1.room_name, R1.capacity
        FROM Rooms AS R1
        WHERE R1.capacity = (
            SELECT MIN(R2.capacity)
            FROM Rooms AS R2
            WHERE R2.capacity > ?)
        AND R1.room_id NOT IN (
            SELECT B.room_id
            FROM Bookings AS B
            WHERE B.date = ? AND (
                (B.start_time <= ? AND B.end_time > ?) OR
                (B.start_time < ? AND B.end_time >= ?)
            )
        )
    """, (criteria_capacity, selected_date, end_time, start_time, start_time, end_time))
        
        closest_capacity_rooms = cursor.fetchall()
        if closest_capacity_rooms:
            return closest_capacity_rooms
        else:
            return []

    return exact_capacity_rooms


def book_room(org_id, room_id, start_time_str, end_time_str, selected_date):
    start_time = datetime.strptime(start_time_str, "%H:%M")
    end_time = datetime.strptime(end_time_str, "%H:%M")
    cursor.execute("SELECT COUNT(*) FROM Bookings WHERE room_id = ? AND date = ? AND ((start_time <= ? AND end_time > ?) OR (start_time < ? AND end_time >= ?))",
                   (room_id, selected_date, start_time, start_time, end_time, end_time))
    
    if cursor.fetchone()[0] == 0:
        booking_duration = (end_time - start_time).total_seconds() / 3600
        
        cursor.execute("SELECT SUM(duration) FROM Bookings WHERE org_id = ? AND strftime('%Y-%m', date) = ?",
                       (org_id, selected_date.strftime('%Y-%m')))
        monthly_hours = cursor.fetchone()[0] or 0.0

        if monthly_hours + booking_duration <= 30.0:
            cursor.execute("INSERT INTO Bookings (org_id, room_id, date, start_time, end_time, duration) VALUES (?, ?, ?, ?, ?, ?)",
                           (org_id, room_id, selected_date, start_time, end_time, booking_duration))
            conn.commit()
            print("Booking successful!")
        else:
            print("Organization has exceeded the monthly limit.")
    else:
        print("The selected room is not available for the specified date and time.")


def booking_menu(org_id):
    criteria_capacity = int(input("Enter the required room capacity: "))
    start_time = input("Enter the start time (24-hour format, e.g., 13:00): ")
    end_time = input("Enter the end time (24-hour format, e.g., 14:00): ")
    selected_date_str = input("Enter the date (YYYY-MM-DD) for which you want to book: ")

    available_rooms = list_available_rooms(criteria_capacity, start_time, end_time, selected_date_str)

    if not available_rooms:
        print("No available rooms match the criteria.")
        return

    print("Available Rooms:")
    for i in range(len(available_rooms)):
        room_info = available_rooms[i]
        room_id = room_info[0]
        floor_id = room_info[1]
        room_name = room_info[2]
        print(f"{i+1}. Floor {floor_id}, Room {room_name}")

    room_choice = int(input("Select a room by entering the corresponding number: "))
    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d")
    if 1 <= room_choice <= len(available_rooms):
        room_info = available_rooms[room_choice - 1]
        room_id = room_info[0]
        floor_id = room_info[1]
        room_name = room_info[2]

        book_room(org_id, room_id, start_time, end_time, selected_date)
