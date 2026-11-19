import streamlit as st
from collections import deque

# -----------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="Smart Card Parking System",
    page_icon="🚗",
    layout="wide"
)

TOTAL_SLOTS = 5

# -----------------------------------
# 2. INITIALIZE SESSION STATE
# -----------------------------------

if "parking" not in st.session_state:
    st.session_state.parking = [None] * TOTAL_SLOTS

if "vehicles" not in st.session_state:
    st.session_state.vehicles = {}

if "waiting" not in st.session_state:
    st.session_state.waiting = deque()


# -----------------------------------
# 3. MAIN HEADING
# -----------------------------------

st.title("🚗 Smart Card Parking System")


st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Select an Option",
    [
        "Dashboard",
        "Register Vehicle",
        "Vehicle Entry",
        "Vehicle Exit",
        "Waiting Queue",
        "Search Vehicle"
    ]
)


# -----------------------------------
# 4. VEHICLE REGISTRATION
# -----------------------------------

if menu == "Register Vehicle":

    st.header("📝 Register New Vehicle")

    with st.form("registration_form"):

        card = st.text_input("Enter Smart Card ID")
        name = st.text_input("Enter Owner Name")
        number = st.text_input("Enter Vehicle Number")

        submit = st.form_submit_button("Register Vehicle")

        if submit:

            card = card.strip().upper()
            name = name.strip()
            number = number.strip().upper()

            if not card or not name or not number:
                st.error("Please fill all the fields!")

            elif card in st.session_state.vehicles:
                st.warning("Card ID already registered!")

            else:
                st.session_state.vehicles[card] = [
                    name,
                    number
                ]

                st.success("Vehicle Registered Successfully!")


# -----------------------------------
# 5. VEHICLE ENTRY
# -----------------------------------

elif menu == "Vehicle Entry":

    st.header("🚘 Vehicle Entry")

    with st.form("entry_form"):

        card = st.text_input("Enter Smart Card ID")

        submit = st.form_submit_button("Allow Entry")

        if submit:

            card = card.strip().upper()

            if card not in st.session_state.vehicles:
                st.error("Please Register First!")

            elif card in st.session_state.parking:
                st.warning("Vehicle Already Parked!")

            elif card in st.session_state.waiting:
                st.warning("Vehicle Already Waiting!")

            else:

                slot_found = False

                for i in range(TOTAL_SLOTS):

                    if st.session_state.parking[i] is None:

                        st.session_state.parking[i] = card

                        st.success("Vehicle Parked Successfully!")

                        st.info(f"Assigned Slot Number: {i + 1}")

                        slot_found = True
                        break

                if not slot_found:

                    st.session_state.waiting.append(card)

                    st.warning("Parking Full!")

                    st.success("Vehicle Added to Waiting Queue!")


# -----------------------------------
# 6. VEHICLE EXIT
# -----------------------------------

elif menu == "Vehicle Exit":

    st.header("🚙 Vehicle Exit")

    with st.form("exit_form"):

        card = st.text_input("Enter Smart Card ID")

        submit = st.form_submit_button("Exit Vehicle")

        if submit:

            card = card.strip().upper()

            found = False

            for i in range(TOTAL_SLOTS):

                if st.session_state.parking[i] == card:

                    st.session_state.parking[i] = None

                    st.success("Vehicle Exited Successfully!")

                    found = True

                    if st.session_state.waiting:

                        next_vehicle = (
                            st.session_state.waiting.popleft()
                        )

                        st.session_state.parking[i] = next_vehicle

                        st.success(
                            f"Waiting Vehicle {next_vehicle} "
                            f"automatically assigned Slot {i + 1}!"
                        )

                    break

            if not found:

                st.error("Vehicle Not Found in Parking!")


# -----------------------------------
# 7. WAITING QUEUE
# -----------------------------------

elif menu == "Waiting Queue":

    st.header("⏳ Vehicle Waiting Queue")

    waiting = st.session_state.waiting

    st.metric("Total Waiting Vehicles", len(waiting))

    if waiting:

        st.write("Vehicles are arranged according to FIFO.")

        for position, card in enumerate(waiting, start=1):

            name = st.session_state.vehicles[card][0]
            number = st.session_state.vehicles[card][1]

            st.info(
                f"Position {position} | Card ID: {card} | "
                f"Owner: {name} | Vehicle: {number}"
            )

    else:

        st.success("No Vehicles are Waiting!")


# -----------------------------------
# 8. SEARCH VEHICLE (UPDATED)
# -----------------------------------

elif menu == "Search Vehicle":

    st.header("🔍 Search Vehicle")

    with st.form("search_form"):

        card = st.text_input("Enter Smart Card ID")

        submit = st.form_submit_button("Search")

        if submit:

            card = card.strip().upper()

            if card in st.session_state.vehicles:

                name, number = st.session_state.vehicles[card]

                st.success("Vehicle Found!")

                st.write("### Vehicle Details")

                st.write("**Card ID:**", card)
                st.write("**Owner Name:**", name)
                st.write("**Vehicle Number:**", number)

                if card in st.session_state.parking:

                    slot = (
                        st.session_state.parking.index(card) + 1
                    )

                    st.success("Status: Parked")

                    st.info(f"🅿️ Assigned Parking Slot: {slot}")

                elif card in st.session_state.waiting:

                    position = (
                        list(st.session_state.waiting).index(card) + 1
                    )

                    st.warning("Status: Waiting")

                    st.info(f"Waiting Queue Position: {position}")

                else:

                    st.info("Status: Registered, Not Parked")
                    st.write("Parking Slot: Not Assigned")

            else:

                st.error("Vehicle Not Registered!")


# -----------------------------------
# 9. DASHBOARD
# -----------------------------------

st.divider()

st.header("📊 Parking Dashboard")

occupied = sum(
    1 for slot in st.session_state.parking
    if slot is not None
)

available = TOTAL_SLOTS - occupied

waiting_count = len(st.session_state.waiting)

registered = len(st.session_state.vehicles)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Slots", TOTAL_SLOTS)

col2.metric("Occupied Slots", occupied)

col3.metric("Available Slots", available)

col4.metric("Waiting Vehicles", waiting_count)

st.write("### 🅿️ Parking Slot Status")

slot_columns = st.columns(TOTAL_SLOTS)

for i in range(TOTAL_SLOTS):

    with slot_columns[i]:

        if st.session_state.parking[i] is None:

            st.success(f"Slot {i + 1}\n\nAvailable")

        else:

            card = st.session_state.parking[i]

            st.error(f"Slot {i + 1}\n\nOccupied\n\n{card}")


# -----------------------------------
# 10. REGISTERED VEHICLES
# -----------------------------------

st.write("### 📋 Registered Vehicles")

if st.session_state.vehicles:

    for card, details in st.session_state.vehicles.items():

        st.write(
            f"**{card}** | Owner: {details[0]} | "
            f"Vehicle: {details[1]}"
        )

else:

    st.info("No vehicles registered yet.")


# -----------------------------------
# 11. WAITING QUEUE PREVIEW
# -----------------------------------

st.write("### ⏳ Current Waiting Queue")

if st.session_state.waiting:

    for position, card in enumerate(
        st.session_state.waiting,
        start=1
    ):

        st.write(f"{position}. {card}")

else:

    st.write("No vehicles waiting.")

st.divider()

st.caption("Smart Card Parking System")