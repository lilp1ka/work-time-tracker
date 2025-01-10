import React, { useState } from "react";
import { setUserTasks } from "@/services/adminService";

function SetTasks() {
  const [userId, setUserId] = useState("");
  const [tasks, setTasks] = useState("");

  const handleSubmit = async () => {
    const taskList = tasks.split(",").map((task) => task.trim());
    await setUserTasks(userId, taskList);
    alert("Tasks assigned!");
  };

  return (
    <div>
      <h2>Set Tasks</h2>
      <input
        type="text"
        placeholder="User ID"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
      />
      <input
        type="text"
        placeholder="Tasks (comma-separated)"
        value={tasks}
        onChange={(e) => setTasks(e.target.value)}
      />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}

export default SetTasks;
