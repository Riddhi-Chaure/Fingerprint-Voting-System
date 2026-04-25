import firebase_admin
from firebase_admin import credentials, firestore

# Connect Firebase
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print(f"Error initializing Firebase: {e}")
    exit()

# REGISTER FUNCTION
def register_user():
    student_id = input("Enter Student ID: ")
    name = input("Enter Name: ")
    fingerprint = input("Enter Fingerprint ID: ")

    db.collection("users").document(student_id).set({
        "name": name,
        "fingerprint": fingerprint,
        "hasVoted": False
    })

    print("User Registered Successfully!")

def login_user():
    student_id = input("Enter Student ID: ")
    fingerprint = input("Enter Fingerprint ID: ")

    doc = db.collection("users").document(student_id).get()

    if doc.exists:
        data = doc.to_dict()

        if data["fingerprint"] == fingerprint:
            print("Login Successful!")
        else:
            print("Invalid Fingerprint!")
    else:
        print("User not found! Register First!")

def vote():
    student_id = input("Enter Student ID: ")

    doc = db.collection("users").document(student_id).get()

    if doc.exists:
        data = doc.to_dict()

        if data["hasVoted"]:
            print("You have already voted!")
        else:
            print("Vote for candidate:")
            print("1. Vote for candidate A")
            print("2. Vote for candidate B")

            choice = input("Enter choice: ")

            if choice == "1":
                candidate = "A"
            elif choice == "2":
                candidate = "B"
            else:
                print("Invalid choice")
                return

            # store vote
            db.collection("votes").add({
                "student_id": student_id,
                "candidate": candidate
            })

            # update user status
            db.collection("users").document(student_id).update({
                "hasVoted": True
            })

            print("Vote cast successfully!")
    else:
        print("User not found!")

def show_results():
    print("\nFetching results...")
    try:
        votes = db.collection("votes").stream()

        count_A = 0
        count_B = 0

        for vote in votes:
            data = vote.to_dict()
            if data["candidate"] == "A":
                count_A += 1
            elif data["candidate"] == "B":
                count_B += 1

        print("\n--- RESULTS ---")
        print(f"Candidate A: {count_A}")
        print(f"Candidate B: {count_B}")
        print("---------------")
    except Exception as e:
        print(f"Error fetching results: {e}")

# MAIN MENU
def main():
    while True:
        try:
            print("\n1. Register")
            print("2. Login")
            print("3. Vote")
            print("4. Show Results")
            print("5. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                register_user()
            elif choice == "2":
                login_user()
            elif choice == "3":
                vote()
            elif choice == "4":
                show_results()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice")
        except KeyboardInterrupt:
            print("\nExiting program...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()