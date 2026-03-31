from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
tasks = []

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Task Manager</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@600;700;800&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #0f0f13;
      --surface: #17171f;
      --border: #2a2a38;
      --accent: #7c6aff;
      --accent-dim: #3d3470;
      --text: #e8e8f0;
      --muted: #6b6b80;
      --danger: #ff5f6d;
      --success: #42e6a4;
      --mono: 'DM Mono', monospace;
      --display: 'Syne', sans-serif;
    }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--mono);
      min-height: 100vh;
      display: flex;
      align-items: flex-start;
      justify-content: center;
      padding: 48px 20px;
      background-image:
        radial-gradient(ellipse 60% 40% at 70% 10%, #2a1f6622 0%, transparent 60%),
        radial-gradient(ellipse 40% 30% at 20% 80%, #1a3a4422 0%, transparent 60%);
    }

    .container {
      width: 100%;
      max-width: 540px;
      animation: fadeUp 0.5s ease both;
    }

    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(20px); }
      to   { opacity: 1; transform: translateY(0); }
    }

    .header { margin-bottom: 36px; }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--accent-dim);
      color: var(--accent);
      font-size: 11px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: 4px;
      margin-bottom: 14px;
      font-family: var(--mono);
    }

    .badge::before {
      content: '';
      width: 6px; height: 6px;
      background: var(--accent);
      border-radius: 50%;
      animation: pulse 2s ease infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.7); }
    }

    h1 {
      font-family: var(--display);
      font-size: 28px;
      font-weight: 800;
      letter-spacing: -0.02em;
      line-height: 1.1;
      color: var(--text);
    }

    h1 span { color: var(--accent); }

    .subtitle {
      margin-top: 8px;
      font-size: 12px;
      color: var(--muted);
      letter-spacing: 0.04em;
    }

    .input-row {
      display: flex;
      gap: 10px;
      margin-bottom: 28px;
    }

    input[type="text"] {
      flex: 1;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      font-family: var(--mono);
      font-size: 13px;
      padding: 12px 16px;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }

    input[type="text"]::placeholder { color: var(--muted); }

    input[type="text"]:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px #7c6aff1a;
    }

    .btn-add {
      background: var(--accent);
      color: #fff;
      border: none;
      border-radius: 8px;
      padding: 12px 20px;
      font-family: var(--display);
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: background 0.2s, transform 0.1s;
      white-space: nowrap;
    }

    .btn-add:hover { background: #9585ff; }
    .btn-add:active { transform: scale(0.97); }

    .stats {
      display: flex;
      gap: 16px;
      margin-bottom: 20px;
    }

    .stat {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 16px;
      font-size: 11px;
      color: var(--muted);
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }

    .stat strong {
      display: block;
      font-size: 20px;
      color: var(--text);
      font-family: var(--display);
      font-weight: 700;
      letter-spacing: -0.02em;
      line-height: 1.2;
    }

    .section-label {
      font-size: 10px;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 10px;
    }

    #taskList {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    #taskList li {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 13px 16px;
      font-size: 13px;
      animation: slideIn 0.25s ease both;
      transition: border-color 0.2s;
    }

    #taskList li:hover { border-color: #3a3a50; }

    @keyframes slideIn {
      from { opacity: 0; transform: translateX(-10px); }
      to   { opacity: 1; transform: translateX(0); }
    }

    .task-index {
      color: var(--accent);
      font-size: 10px;
      margin-right: 12px;
      min-width: 20px;
      opacity: 0.7;
    }

    .task-text { flex: 1; color: var(--text); }

    .btn-delete {
      background: transparent;
      border: 1px solid transparent;
      border-radius: 6px;
      color: var(--muted);
      font-size: 11px;
      font-family: var(--mono);
      padding: 4px 8px;
      cursor: pointer;
      transition: all 0.2s;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }

    .btn-delete:hover {
      border-color: var(--danger);
      color: var(--danger);
      background: #ff5f6d12;
    }

    .empty {
      text-align: center;
      padding: 40px 20px;
      color: var(--muted);
      font-size: 12px;
      border: 1px dashed var(--border);
      border-radius: 8px;
      letter-spacing: 0.04em;
    }

    .empty-icon {
      font-size: 28px;
      margin-bottom: 10px;
      opacity: 0.4;
    }

    .footer {
      margin-top: 36px;
      font-size: 11px;
      color: var(--muted);
      letter-spacing: 0.06em;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .footer::before {
      content: '';
      flex: 1;
      height: 1px;
      background: var(--border);
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="badge">DevOps Project</div>
      <h1>Task <span>Manager</span></h1>
      <p class="subtitle">Containerized with Docker · Deployed on Render · CI/CD via GitHub Actions</p>
    </div>

    <div class="input-row">
      <input type="text" id="taskInput" placeholder="Add a new task..." />
      <button class="btn-add" onclick="addTask()">+ Add</button>
    </div>

    <div class="stats">
      <div class="stat"><strong id="totalCount">0</strong>Total</div>
      <div class="stat"><strong id="pendingCount">0</strong>Pending</div>
    </div>

    <p class="section-label">Task Queue</p>
    <ul id="taskList"></ul>
  </div>

  <script>
    async function fetchTasks() {
      const res = await fetch('/tasks');
      const data = await res.json();
      const list = document.getElementById("taskList");
      const total = document.getElementById("totalCount");
      const pending = document.getElementById("pendingCount");

      total.textContent = data.length;
      pending.textContent = data.length;

      if (data.length === 0) {
        list.innerHTML = `
          <div class="empty">
            <div class="empty-icon">📋</div>
            No tasks yet — add one above
          </div>`;
        return;
      }

      list.innerHTML = "";
      data.forEach((task, index) => {
        const li = document.createElement("li");
        li.innerHTML = `
          <span class="task-index">#${String(index + 1).padStart(2, '0')}</span>
          <span class="task-text">${task}</span>
          <button class="btn-delete" onclick="deleteTask(${index})">remove</button>
        `;
        list.appendChild(li);
      });
    }

    async function addTask() {
      const input = document.getElementById("taskInput");
      const val = input.value.trim();
      if (!val) return;
      await fetch('/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(val)
      });
      input.value = "";
      fetchTasks();
    }

    document.getElementById("taskInput").addEventListener("keydown", e => {
      if (e.key === "Enter") addTask();
    });

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
