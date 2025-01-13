import React, { useState, useEffect } from "react";
import { useLocation, Link } from "react-router-dom";
import { useDispatch } from "react-redux";
import { Button } from "../ui/button";
import { RxDashboard } from "react-icons/rx";
import { CiLogout } from "react-icons/ci";
import { logout } from "@/context/auth/AuthSlice";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { PiInfoLight } from "react-icons/pi";
import { AiOutlineTeam } from "react-icons/ai";



const menuItems = [
  {
    id: 1,
    icon: <RxDashboard style={{ width: "24px", height: "24px" }} />,
    title: "Dashboard",
    link: "/dashboard",
  },
  {
    id: 2,
    icon: <PiInfoLight style={{ width: "24px", height: "24px" }} />,
    title: "UserInfo",
    link: "/users",
  },
  {
    id: 3,
    icon: <AiOutlineTeam style={{ width: "24px", height: "24px" }} />,
    title: "Teamwork",
    link: "/teamwork",
  }
];

function Sidebar({ active, setActive }) {
  const location = useLocation();
  const navigate = useNavigate();
  const dispatch = useDispatch();

  useEffect(() => {
    const path = location.pathname;
    const activeItem = menuItems.find((item) => item.link === path);
    if (activeItem) {
      setActive(activeItem.id);
    }
  }, [location.pathname, setActive]);

  const handleLogout = async () => {
    try {
      await dispatch(logout());
      navigate("/authentication");
      toast.success("Logged out!");
    } catch (error) {
      console.error("Error during logout:", error);
    }
  };

  return (
    <aside className="h-full w-full flex flex-col justify-between ">
      <div className="px-6 py-16">
        <h1 className="font-semibold text-black text-2xl">work-time-tracker</h1>
      </div>
      <nav className="flex-1 pt-10">
        <ul className="space-y-4 px-6"> {/* змінив padding на 6 */}
          {menuItems.map((item) => (
            <li
              key={item.id}
              onClick={() => setActive(item.id)}
              className={`flex items-center space-x-4 pl-4 p-3 rounded-2xl ${
                active === item.id
                  ? "bg-blue-500 text-white"
                  : "hover:bg-blue-200 text-gray-600"
              } cursor-pointer transition-colors duration-300 `}
            >
              <span className="pl-3">{item.icon}</span>
              <span className="font-medium">{item.title}</span>
            </li>
          ))}
        </ul>
      </nav>
      <div className="p-6">
        <Button
          variant="ghost"
          onClick={handleLogout}
          className="w-full flex items-center justify-start space-x-3 pb-10 text-gray-600 hover:text-red-600"
        >
          <CiLogout size={24} />
          <span className="font-medium">LogOut</span>
        </Button>
      </div>
    </aside>
  );
}

export default Sidebar;