import React, { useState } from "react";
import { ContextProvider } from "@/context/GlobalContext.jsx";
import HomePage from "./HomePage.jsx";
import Sidebar from "@/components/sidebar/Sidebar";
import UserList from "./UserList.jsx";
import UserProfile from "./UserProfile.jsx";
import Search from "./Search.jsx";
import Teamwork from "./TeamWork.jsx";

export default function DashboardPage() {
  const [active, setActive] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");

  const displayData = () => {
    switch (active) {
      case 1:
        return <HomePage />;
      case 2:
        return <UserList searchTerm={searchTerm} />;
      case 3:
        return <Teamwork />;
      default:
        return <HomePage />;
    }
  };

  return (
    <ContextProvider>
      <div className="h-screen w-screen grid grid-cols-12 gap-4 p-6 bg-gray-100">
        {/* Бокове меню (блок 1) */}
        <aside className="col-span-2">
          <Sidebar active={active} setActive={setActive} />
        </aside>

        <div className="col-span-10 flex flex-col gap-4">
          {/* Верхній бар (блок 2) */}
          <div className="flex items-center h-[10%]">
            <div className="flex justify-between w-full items-end">
              {/* Пошук */}
              <div className="flex-1">
                <Search
                  placeholder="Search..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
              {/* Профіль користувача */}
              <div>
                <UserProfile />
              </div>
            </div>
          </div>

          {/* Основний контент (блок 3) */}
          <div className="flex-grow overflow-hidden">
            <main className="h-full w-full">{displayData()}</main>
          </div>
        </div>
      </div>
    </ContextProvider>
  );
}