## Overview  
**Project Title**: To-Do List with Firestore and Real-Time Updates  
**Project Description**: A Python-based to-do list app that performs CRUD operations on a Firestore cloud database. It also listens for real-time updates whenever data changes in the cloud, providing instant feedback without manual refresh.  
**Project Goals**:  
- Build a cloud-connected app with Firebase Firestore  
- Implement create, read, update, delete operations  
- Add real-time update notifications using Firestore snapshot listeners  
- Learn how Python connects with Firestore  

## Instructions for Build and Use  
Steps to build and/or run the software:  
1. Clone the repo: `git clone https://github.com/your-username/your-repo.git`  
2. Navigate into the folder: `cd todo_list`  
3. Create a virtual environment: `python3 -m venv venv`  
4. Activate the environment: `source venv/bin/activate`  
5. Install dependencies: `pip install firebase-admin`  
6. Add your Firebase service account JSON file (don’t upload it to GitHub)  
7. Run the app: `python main.py`  

Instructions for using the software:  
1. `add_task("Task", "Description")` to add a task  
2. `update_task("doc_id", {"completed": True})` to update a task  
3. `delete_task("doc_id")` to delete a task  
4. `listen_to_tasks()` to start real-time update logging and automatically reflect changes  

> ℹ️ **Note:** The app includes error handling to skip malformed Firestore documents that are missing required fields such as `title` or `completed`.

## Error Handling  
- Tasks without a `title` or `completed` field will be automatically skipped and logged with a warning.  
- This ensures the program does not crash when malformed data is present in the Firestore collection.  
- A message like `⚠️ Skipping malformed task: doc_id => {...}` will appear in the console.

## Development Environment  
To recreate the development environment, you need the following software and/or libraries with the specified versions:  
* Python 3.10+  
* `firebase-admin` (install via pip)  
* Firebase Firestore (set up on [firebase.google.com](https://firebase.google.com))  

## Useful Websites to Learn More  
I found these websites useful in developing this software:  
* [Firebase Admin SDK (Python)](https://firebase.google.com/docs/admin/setup)  
* [Google Firestore Documentation](https://cloud.google.com/firestore/docs)  
* [GitHub Markdown Guide](https://www.markdownguide.org/basic-syntax/)  

## Future Work  
The following items I plan to fix, improve, and/or add to this project in the future:  
* [ ] Add a user interface (web or GUI)  
* [ ] Implement user authentication with Firebase Auth  
* [ ] Add support for multiple collections (e.g., users, tags)  
