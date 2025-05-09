import firebase_admin
from firebase_admin import credentials, firestore
import time

# Initialize Firebase
cred = credentials.Certificate("to-do-list-db1b7-firebase-adminsdk-fbsvc-530b3a6ef4.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
tasks_ref = db.collection('tasks')

# ---------- Add a new task ----------
def add_task(title, description):
    tasks_ref.add({
        'title': title,
        'description': description,
        'completed': False
    })
    print("✅ Task added!")

# ---------- Get and Display All Tasks with Menu Numbers ----------

def get_tasks_with_menu():
    tasks = tasks_ref.stream()
    id_map = {}
    print("\n--- To-Do Tasks ---")
    for i, task in enumerate(tasks, 1):
        task_data = task.to_dict()
        # Skip if task data is missing title or completed
        if 'title' not in task_data or 'completed' not in task_data:
            print(f"⚠️ Skipping malformed task: {task.id} => {task_data}")
            continue
        print(f"{i}. {task_data['title']} - {'✅' if task_data['completed'] else '❌'}")
        id_map[i] = task.id
    return id_map

# ---------- Update a Task by Menu Number ----------
def update_task_by_number(task_num, id_map):
    if task_num in id_map:
        task_id = id_map[task_num]
        task_ref = tasks_ref.document(task_id)
        task_ref.update({"completed": True})
        print("✅ Task marked as completed!")
    else:
        print("❌ Invalid task number!")

# ---------- Delete a Task by Menu Number ----------
def delete_task_by_number(task_num, id_map):
    if task_num in id_map:
        task_id = id_map[task_num]
        tasks_ref.document(task_id).delete()
        print("🗑️ Task deleted!")
    else:
        print("❌ Invalid task number!")

# ---------- Real-time Listener ----------
def on_snapshot(col_snapshot, changes, read_time):
    print("\n📢 Real-time update:")
    for change in changes:
        if change.type.name == 'ADDED':
            print(f"➕ New: {change.document.to_dict()}")
        elif change.type.name == 'MODIFIED':
            print(f"✏️ Modified: {change.document.to_dict()}")
        elif change.type.name == 'REMOVED':
            print(f"🗑️ Removed: {change.document.id}")

def listen_to_tasks():
    tasks_ref.on_snapshot(on_snapshot)
    print("👂 Listening for real-time changes...")

# ---------- CLI Menu ----------
def main():
    listen_to_tasks()
    while True:
        print("\n--- MENU ---")
        print("1. View tasks")
        print("2. Add task")
        print("3. Mark task as complete")
        print("4. Delete task")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            id_map = get_tasks_with_menu()
        elif choice == "2":
            title = input("Title: ")
            description = input("Description: ")
            add_task(title, description)
        elif choice == "3":
            id_map = get_tasks_with_menu()
            task_num = int(input("Enter task number to complete: "))
            update_task_by_number(task_num, id_map)
        elif choice == "4":
            id_map = get_tasks_with_menu()
            task_num = int(input("Enter task number to delete: "))
            delete_task_by_number(task_num, id_map)
        elif choice == "5":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice")

        time.sleep(1)

if __name__ == "__main__":
    main()
