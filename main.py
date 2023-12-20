from login import login

def main():

        while True:
            print("Welcome to the Conference Room Booking System:")
            print("1. Login")
            print("2. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                login()
            elif choice == '2':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
