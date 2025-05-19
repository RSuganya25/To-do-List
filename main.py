import firebase_admin
from firebase_admin import credentials, firestore
import time

# Initialize Firebase
cred = credentials.Certificate("to-do-list-db1b7-firebase-adminsdk-fbsvc-530b3a6ef4.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
tasks_ref = db.collection('tasks')

def add_task(title, description):
    print("Set task priority (High, Medium, Low):")
    priority = input().strip().capitalize()
    if priority not in ['High', 'Medium', 'Low']:
        print("Invalid priority, defaulting to Medium.")
        priority = 'Medium'
    tasks_ref.add({
        'title': title,
        'description': description,
        'completed': False,
        'priority': priority
    })
    print("✅ Task added with priority:", priority)

def get_tasks_with_menu():
    tasks = list(tasks_ref.stream())
    id_map = {}
    priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
    task_list = []
    for task in tasks:
        task_data = task.to_dict()
        priority = task_data.get('priority', 'Medium')
        task_list.append((priority_order.get(priority, 2), task_data, task.id))
    task_list.sort(key=lambda x: x[0])
    print("\n--- To-Do Tasks (Sorted by Priority) ---")
    for i, (prio_num, task_data, task_id) in enumerate(task_list, 1):
        if 'title' not in task_data or 'completed' not in task_data:
            print(f"⚠️ Skipping malformed task: {task_id} => {task_data}")
            continue
        print(f"{i}. {task_data['title']} - Priority: {task_data.get('priority', 'Medium')} - {'✅' if task_data['completed'] else '❌'}")
        id_map[i] = task_id
    return id_map

def update_task_by_number(task_num, id_map):
    if task_num in id_map:
        task_id = id_map[task_num]
        task_ref = tasks_ref.document(task_id)
        task_ref.update({"completed": True})
        print("✅ Task marked as completed!")
    else:
        print("❌ Invalid task number!")

def delete_task_by_number(task_num, id_map):
    if task_num in id_map:
        task_id = id_map[task_num]
        tasks_ref.document(task_id).delete()
        print("🗑️ Task deleted!")
    else:
        print("❌ Invalid task number!")

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

def main():
    listen_to_tasks()
    while True:
        print("\n--- MENU ---")
        print("1. View tasks")
        print("2. Add task")
        print("3. Mark task as complete")
        print("4. Delete task")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            id_map = get_tasks_with_menu()

        elif choice == "2":
            title = input("Title: ").strip()
            description = input("Description: ").strip()
            add_task(title, description)

        elif choice == "3":
            id_map = get_tasks_with_menu()
            task_input = input("Enter task number to complete: ").strip()
            if not task_input.isdigit():
                print("❌ Invalid input. Please enter a valid task number.")
                continue
            update_task_by_number(int(task_input), id_map)

        elif choice == "4":
            id_map = get_tasks_with_menu()
            task_input = input("Enter task number to delete: ").strip()
            if not task_input.isdigit():
                print("❌ Invalid input. Please enter a valid task number.")
                continue
            delete_task_by_number(int(task_input), id_map)

        elif choice == "5":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid choice")

        time.sleep(1)

if __name__ == "__main__":
    main()
