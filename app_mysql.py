import mysql.connector

#  MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shail@bt17",    # if your MySQL has password then write it here
    database="user_management"
)

cursor = db.cursor()

def create_user():
    name = input("Enter name: ")
    email = input("Enter email: ")
    age = int(input("Enter age: "))

    query = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
    values = (name, email, age)

    cursor.execute(query, values)
    db.commit()   # changes save karna jaruri hai
    print("User created successfully!\n")


def view_users():
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()

    if not result:
        print("No users found\n")
    else:
        print("---- All Users ----")
        for row in result:
            print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]} | Age: {row[3]}")
        print()


def update_user():
    user_id = input("Enter user ID to update: ")

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if user is None:
        print("User not found!\n")
        return

    print("\nPress ENTER if you don't want to update a field.\n")

    name = input(f"Enter new name ({user[1]}): ")  # user[1] = existing name
    email = input(f"Enter new email ({user[2]}): ")  # user[2] = existing email
    age = input(f"Enter new age ({user[3]}): ")  # user[3] = existing age

    # keep old values if input blank
    if name == "":
        name = user[1]
    if email == "":
        email = user[2]
    if age == "":
        age = user[3]

    query = "UPDATE users SET name=%s, email=%s, age=%s WHERE id=%s"
    values = (name, email, age, user_id)

    cursor.execute(query, values)
    db.commit()
    print("User updated successfully!\n")


def delete_user():
    user_id = int(input("Enter User ID to delete: "))

    query = "DELETE FROM users WHERE id=%s"
    cursor.execute(query, (user_id,))
    db.commit()

    if cursor.rowcount == 0:
        print("User not found!\n")
    else:
        print("User deleted successfully!\n")


# 🔁 Menu loop
while True:
    print("1. Create User")
    print("2. View Users")
    print("3. Update User")
    print("4. Delete User")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        create_user()
    elif choice == "2":
        view_users()
    elif choice == "3":
        update_user()
    elif choice == "4":
        delete_user()
    elif choice == "5":
        print("Program ended")
        break
    else:
        print("Invalid choice\n")
