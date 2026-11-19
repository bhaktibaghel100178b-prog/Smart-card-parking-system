from collections import deque

TOTAL_SLOTS = 5
parking = [None] * TOTAL_SLOTS
vehicles = {}
waiting = deque()


# Function to register a vehicle
def register():
    card = input("Enter Card ID: ")
    name = input("Enter Owner Name: ")
    number = input("Enter Vehicle Number: ")

    if card in vehicles:
        print("Card already registered!")
        return

    vehicles[card] = [name, number]
    print("Vehicle Registered Successfully!")


# Function for vehicle entry
def entry():
    card = input("Enter Card ID: ")

    if card not in vehicles:
        print("Please Register First!")
        return

    if card in parking:
        print("Vehicle Already Parked!")
        return

    if card in waiting:
        print("Vehicle Already Waiting!")
        return

    for i in range(TOTAL_SLOTS):
        if parking[i] is None:
            parking[i] = card
            print("Vehicle Parked!")
            print("Slot Number:", i + 1)
            return

    waiting.append(card)
    print("Parking Full!")
    print("Added to Waiting Queue!")


# Function for vehicle exit
def exit_vehicle():
    card = input("Enter Card ID: ")

    for i in range(TOTAL_SLOTS):
        if parking[i] == card:
            parking[i] = None
            print("Vehicle Exited Successfully!")

            if waiting:
                next_vehicle = waiting.popleft()
                parking[i] = next_vehicle

                print("Waiting Vehicle Parked!")
                print("Slot Number:", i + 1)

            return

    print("Vehicle Not Found!")


# Function to display parking and waiting queue
def display():
    print("\n--- PARKING STATUS ---")

    for i in range(TOTAL_SLOTS):
        if parking[i] is None:
            print("Slot", i + 1, ": Available")
        else:
            print("Slot", i + 1, ": Occupied")

    print("\n--- WAITING QUEUE ---")

    if not waiting:
        print("No vehicles waiting!")
    else:
        for i, card in enumerate(waiting, start=1):
            print(i, ".", card)

    print("Total Waiting Vehicles:", len(waiting))


# Function to search a vehicle
def search():
    card = input("Enter Card ID: ")

    if card in vehicles:
        print("\n--- VEHICLE DETAILS ---")
        print("Card ID:", card)
        print("Owner:", vehicles[card][0])
        print("Vehicle:", vehicles[card][1])

        if card in parking:
            slot = parking.index(card) + 1
            print("Status: Parked")
            print("Parking Slot Number:", slot)

        elif card in waiting:
            position = list(waiting).index(card) + 1
            print("Status: Waiting")
            print("Waiting Queue Position:", position)

        else:
            print("Status: Registered")
            print("Parking Slot: Not Assigned")

    else:
        print("Vehicle Not Registered!")


# Main menu
while True:
    print("\n===== SMART PARKING SYSTEM =====")
    print("1. Register Vehicle")
    print("2. Vehicle Entry")
    print("3. Vehicle Exit")
    print("4. Display Parking")
    print("5. Search Vehicle")
    print("0. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        register()

    elif choice == "2":
        entry()

    elif choice == "3":
        exit_vehicle()

    elif choice == "4":
        display()

    elif choice == "5":
        search()

    elif choice == "0":
        print("Thank You!")
        break

    else:
        print("Invalid Choice!")