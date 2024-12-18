// import React, { useEffect, useState } from "react";
// import { getAllUsers } from "@/services/userService";

// function UserList() {
//   const [users, setUsers] = useState([]);

//   useEffect(() => {
//     async function fetchUsers() {
//       const data = await getAllUsers();
//       setUsers(data);
//     }
//     fetchUsers();
//   }, []);

//   return (
//     <div>
//       <h2>All Users</h2>
//       <ul>
//         {users.map((user) => (
//           <li key={user.id}>
//             {user.username} ({user.email}) - {user.is_active ? "Active" : "Inactive"}
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// }

// export default UserList;
