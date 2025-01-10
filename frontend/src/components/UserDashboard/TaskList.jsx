// import React, { useEffect, useState } from "react";
// import { getCurrentUser } from "@/services/userService";

// function TaskList() {
//   const [tasks, setTasks] = useState([]);

//   useEffect(() => {
//     async function fetchTasks() {
//       const user = await getCurrentUser();
//       setTasks(user.tasks || []);
//     }
//     fetchTasks();
//   }, []);

//   return (
//     <div>
//       <h2>Tasks</h2>
//       <ul>
//         {tasks.map((task, index) => (
//           <li key={index} className="flex items-center justify-between">
//             <span>{task.name}</span>
//             <input type="checkbox" defaultChecked={task.completed} />
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// }

// export default TaskList;
