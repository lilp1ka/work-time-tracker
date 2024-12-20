// import React, { useEffect, useState } from "react";
// import { Bar } from "react-chartjs-2";
// import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend } from "chart.js";
// import { getCurrentUser } from "@/services/userService";

// // Реєстрація компонентів для Chart.js
// ChartJS.register(BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

// function WorkHoursChart() {
//   const [workHours, setWorkHours] = useState([]);

//   useEffect(() => {
//     async function fetchWorkHours() {
//       const user = await getCurrentUser();
//       setWorkHours(user.work_hours || []);
//     }
//     fetchWorkHours();
//   }, []);

//   const data = {
//     labels: workHours.map((item) => item.date),
//     datasets: [
//       {
//         label: "Work Hours",
//         data: workHours.map((item) => item.hours),
//         backgroundColor: "rgba(59, 130, 246, 0.6)",
//       },
//     ],
//   };

//   const options = {
//     responsive: true,
//     plugins: {
//       legend: { display: true },
//       title: { display: true, text: "User Work Hours" },
//     },
//   };

//   return (
//     <div className="p-4 bg-white shadow rounded-xl">
//       <h2 className="text-xl font-semibold mb-4">Work Hours</h2>
//       <Bar data={data} options={options} />
//     </div>
//   );
// }

// export default WorkHoursChart;
