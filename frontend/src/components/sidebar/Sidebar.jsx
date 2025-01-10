import React from "react";
import { useSelector } from "react-redux"; // Для отримання ролі з Redux
import { Link } from "react-router-dom";
import { Button } from "../ui/button";

function Sidebar() {
  const user = useSelector((state) => state.auth.user);

  const isSuperUser = user?.role === "admin";

  return (
    <aside className="w-64 shadow-sm flex flex-col">
      <div className="px-6 pt-10 font-bold text-xl text-[#3B82F6]">Sosal</div>
      <nav className="flex-1 mt-4 pt-10">
      <ul className="space-y-2">
        <li>
          <Link to="/" className="px-6 py-3 shadow bg-[#5216dd] text-[#ffffff] font-medium rounded-xl">
          Home
          </Link>
        </li>

        {isSuperUser ? (
          <>
            <li>
              <Link to="/set-tasks" className="px-6 py-3 shadow bg-[#5216dd] text-[#ffffff] font-medium rounded-xl">
                Встановлення завдань
              </Link>
            </li>
            <li>
              <Link to="/user-list" className="px-6 py-3 shadow bg-[#5216dd] text-[#ffffff] font-medium rounded-xl">
                Список користувачів
              </Link>
            </li>
          </>
        ) : (
          <>
            <li>
              <Link to="/settasks" className="text-gray-300 hover:text-white">
                Tasks
              </Link>
            </li>
            <li>
              <Link to="/work-hours" className="text-gray-300 hover:text-white">
                Hours
              </Link>
            </li>
          </>
        )}
      </ul>
      </nav>
      <Button
        variant="ghost"
        className="w-full px-6 py-3 text-left text-gray-500 hover:text-red-500"
      >
        Log Out
      </Button>
    </aside>
  );
}

export default Sidebar;

