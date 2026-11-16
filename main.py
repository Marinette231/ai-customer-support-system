
import sqlite3

# DATABASE CONNECTION
def connect_db():
    return sqlite3.connect("support_tickets.db")


def initialize_database():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            priority TEXT DEFAULT 'Normal'
        )
    """)

    connection.commit()
    connection.close()


# CUSTOMER FUNCTIONS
def create_ticket(customer_name):
    print("\n=== Create Support Ticket ===")

    title = input("Enter ticket title: ").strip()
    description = input("Describe your problem: ").strip()

    if not title or not description:
        print("Title and description cannot be empty.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tickets (customer, title, description)
        VALUES (?, ?, ?)
    """, (customer_name, title, description))

    ticket_id = cursor.lastrowid

    connection.commit()
    connection.close()

    print("\nTicket created successfully!")
    print("Your Ticket ID:", ticket_id)


def view_customer_tickets(customer_name):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM tickets WHERE customer = ?
    """, (customer_name,))

    results = cursor.fetchall()
    connection.close()

    print("\n=== My Support Tickets ===")

    if not results:
        print("No tickets found.")
        return

    for ticket in results:
        display_ticket(ticket)


# SUPPORT AGENT FUNCTIONS
def display_ticket(ticket):
    print("\n-----------------------------")
    print("Ticket ID:", ticket[0])
    print("Customer:", ticket[1])
    print("Title:", ticket[2])
    print("Description:", ticket[3])
    print("Status:", ticket[4])
    print("Priority:", ticket[5])


def view_all_tickets():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tickets")

    results = cursor.fetchall()
    connection.close()

    print("\n=== All Support Tickets ===")

    if not results:
        print("No tickets available.")
        return

    for ticket in results:
        display_ticket(ticket)


def update_ticket():
    try:
        ticket_id = int(input("\nEnter Ticket ID: "))
    except ValueError:
        print("Invalid Ticket ID.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM tickets WHERE id = ?",
        (ticket_id,)
    )

    ticket = cursor.fetchone()

    if ticket is None:
        print("Ticket not found.")
        connection.close()
        return

    print("\n1. Update Status")
    print("2. Update Priority")

    choice = input("Choose an option: ")

    if choice == "1":
        print("\n1. Open")
        print("2. In Progress")
        print("3. Resolved")

        option = input("Select status: ")

        statuses = {
            "1": "Open",
            "2": "In Progress",
            "3": "Resolved"
        }

        if option in statuses:
            cursor.execute(
                "UPDATE tickets SET status = ? WHERE id = ?",
                (statuses[option], ticket_id)
            )
            print("Status updated successfully!")

        else:
            print("Invalid status.")

    elif choice == "2":
        print("\n1. Low")
        print("2. Normal")
        print("3. High")
        print("4. Urgent")

        option = input("Select priority: ")

        priorities = {
            "1": "Low",
            "2": "Normal",
            "3": "High",
            "4": "Urgent"
        }

        if option in priorities:
            cursor.execute(
                "UPDATE tickets SET priority = ? WHERE id = ?",
                (priorities[option], ticket_id)
            )
            print("Priority updated successfully!")

        else:
            print("Invalid priority.")

    else:
        print("Invalid choice.")

    connection.commit()
    connection.close()


# CUSTOMER DASHBOARD
def customer_dashboard():
    customer_name = input("\nEnter your name: ").strip()

    if not customer_name:
        print("Name cannot be empty.")
        return

    while True:
        print("\n===== CUSTOMER DASHBOARD =====")
        print("1. Create Ticket")
        print("2. View My Tickets")
        print("3. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            create_ticket(customer_name)

        elif choice == "2":
            view_customer_tickets(customer_name)

        elif choice == "3":
            break

        else:
            print("Invalid choice.")


# SUPPORT AGENT DASHBOARD
def agent_dashboard():
    while True:
        print("\n===== SUPPORT AGENT DASHBOARD =====")
        print("1. View All Tickets")
        print("2. Update Ticket")
        print("3. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            view_all_tickets()

        elif choice == "2":
            update_ticket()

        elif choice == "3":
            break

        else:
            print("Invalid choice.")


# MAIN PROGRAM
initialize_database()

while True:
    print("\n===== CUSTOMER SUPPORT SYSTEM =====")
    print("1. Customer")
    print("2. Support Agent")
    print("3. Exit")

    role = input("Select your role: ")

    if role == "1":
        customer_dashboard()

    elif role == "2":
        agent_dashboard()

    elif role == "3":
        print("Thank you for using our system!")
        break

    else:
        print("Invalid choice.")
