from booking import  booking_menu, delete_booking, list_organization_bookings, book_room, list_available_rooms
from database import conn, cursor
from collections import Counter
from datetime import datetime, timedelta
import heapq


def org_admin_actions(user):
    while True:
        print("\nOrganization Administrator Menu:")
        print("1. Create Booking")
        print("2. Delete Booking")
        print("3. List Bookings")
        print("4. Suggest Booking")
        print("5. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_booking_as_org_admin(user)  
        elif choice == '2':
            cancel_booking_as_org_admin(user)  
        elif choice == '3':
            list_bookings_as_org_admin(user)
        elif choice == '4':
            get_top_3_preferred_booking_params(user)
            pass
        elif choice == '5':
            break


def create_booking_as_org_admin(user):
    org_id = user[1]
    booking_menu(org_id)


def cancel_booking_as_org_admin(user):
    org_id = user[1]
    delete_booking(org_id)


def list_bookings_as_org_admin(user):
    org_id = user[1]
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


def get_top_3_preferred_booking_params(user):
    org_id = user[1]
    cursor.execute("""
        SELECT B.date, B.start_time, B.end_time, R.capacity
        FROM Bookings AS B
        INNER JOIN Rooms AS R ON B.room_id = R.room_id
        WHERE B.org_id = ?
    """, (org_id,))

    bookings = []
    for row in cursor.fetchall():
        booking = {
            "date": row[0],
            "start_time": row[1],
            "end_time": row[2],
            "capacity": row[3]
        }
        bookings.append(booking)
    combined_params = Counter()
    max_heap = []

    for booking in bookings:
        params = (booking["date"], booking["start_time"], booking["end_time"], booking["capacity"])
        combined_params[params] += 1

    for params, count in combined_params.items():
        if len(max_heap) < 3:
            heapq.heappush(max_heap, (count, params))
        else:
            if count > max_heap[0][0]:
                heapq.heappop(max_heap)
                heapq.heappush(max_heap, (count, params))

    top_3_params = [params for count, params in max_heap]
    print("Top 3 Preferred Booking Options:")
    for i in range(len(top_3_params)):
        date = params[0]
        start_time = params[1]
        end_time = params[2]
        capacity = params[3]

        start_time_timestamp = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        formatted_start_time = start_time_timestamp.strftime("%H:%M")

        end_time_timestamp = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        formatted_end_time = end_time_timestamp.strftime("%H:%M")
        date_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

        original_date = date_time.date()
        corrected_date = original_date + timedelta(days=7)
        
        corrected_date_str = corrected_date.strftime("%Y-%m-%d")

        print(f"Option {i+1}: Date: {corrected_date_str}, Start Time: {formatted_start_time}, End Time: {formatted_end_time}, Capacity: {capacity} people")

    selected_option = input("Select preferred booking: ")

    while not selected_option.isdigit() or int(selected_option) not in range(1, len(top_3_params) + 1):
        print("Invalid choice. Please select again")
        selected_option = input("Select preferred booking: ")

    selected_option = int(selected_option)
    selected_params = top_3_params[selected_option - 1]

    date_time_str, start_time, end_time, capacity = selected_params

    start_time_timestamp = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    formatted_start_time = start_time_timestamp.strftime("%H:%M")

    end_time_timestamp = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    formatted_end_time = end_time_timestamp.strftime("%H:%M")

    date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

    original_date = date_time.date()
    corrected_date = original_date + timedelta(days=7)
    
    corrected_date_str = corrected_date.strftime("%Y-%m-%d")

    available_rooms = list_available_rooms(capacity, formatted_start_time, formatted_end_time, corrected_date_str)
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
    if 1 <= room_choice <= len(available_rooms):
        room_info = available_rooms[room_choice - 1]
        room_id = room_info[0]
        floor_id = room_info[1]
        room_name = room_info[2]

        book_room(org_id, room_id, formatted_start_time, formatted_end_time, corrected_date)





