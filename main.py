import firebase_admin
from firebase_admin import credentials, firestore

# Use your actual service account file name
cred = credentials.Certificate("to-do-list-db1b7-firebase-adminsdk-fbsvc-530b3a6ef4.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Create a reference to the 'tasks' collection
tasks_ref = db.collection('tasks')

# ---------- Add a new task ----------
def add_task(title, description):
    tasks_ref.add({
        'title': title,
        'description': description,
        'completed': False
    })
    print("Task added!")

# ---------- Get all tasks ----------
def get_tasks():
    tasks = tasks_ref.stream()
    for task in tasks:
        print(f"{task.id} => {task.to_dict()}")

# ---------- Update a task ----------
def update_task(task_id, updates):
    task = tasks_ref.document(task_id)
    task.update(updates)
    print("Task updated!")

# ---------- Delete a task ----------
def delete_task(task_id):
    task = tasks_ref.document(task_id)
    task.delete()
    print("Task deleted!")

# ---------- Listen to real-time updates ----------
def on_snapshot(col_snapshot, changes, read_time):
    print("\n--- Real-time update ---")
    for change in changes:
        if change.type.name == 'ADDED':
            print(f"New task: {change.document.id} => {change.document.to_dict()}")
        elif change.type.name == 'MODIFIED':
            print(f"Modified task: {change.document.id} => {change.document.to_dict()}")
        elif change.type.name == 'REMOVED':
            print(f"Removed task: {change.document.id}")

# Start listening to the collection
def listen_to_tasks():
    print("Listening for real-time changes in 'tasks' collection...")
    tasks_ref.on_snapshot(on_snapshot)


# Sample usage
# add_task("Finish Firestore project", "Complete all CRUD functions")
get_tasks()
update_task("Vc3NoJL1W8gQLq7X6TnH", {"completed": True})
delete_task("08XhAG1iZGLQhNUnkmL2")

get_tasks()
listen_to_tasks()

# Keep the script running
import time
while True:
    time.sleep(1)

