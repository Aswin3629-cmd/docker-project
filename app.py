from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

tasks = []

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager</title>
</head>
<body>
    <h2>🔥 Aswin's DevOps Task Manager</h2>

    <input id="taskInput" placeholder="Enter task">
    <button onclick="addTask()">Add</button>

    <ul id="taskList"></ul>

    <script>
        async function fetchTasks() {
            let res = await fetch('/tasks');
            let data = await res.json();
            let list = document.getElementById("taskList");
            list.innerHTML = "";
            data.forEach((task, index) => {
                list.innerHTML += `<li>${task} <button onclick="deleteTask(${index})">❌</button></li>`;
            });
        }

        async function addTask() {
            let input = document.getElementById("taskInput").value;
            await fetch('/tasks', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(input)
            });
            fetchTasks();
        }

        async function deleteTask(index) {
            await fetch(`/tasks/${index}`, { method: 'DELETE' });
            fetchTasks();
        }

        fetchTasks();
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    tasks.append(data)
    return {"message": "Task added"}, 201

@app.route("/tasks/<int:index>", methods=["DELETE"])
def delete_task(index):
    if index < len(tasks):
        tasks.pop(index)
        return {"message": "Deleted"}
    return {"error": "Not found"}, 404

app.run(host="0.0.0.0", port=5000)
