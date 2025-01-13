import React, { useEffect, useState } from "react";
import { useGlobalContext } from "@/context/GlobalContext";
import UserDetails from "./UserDetails";
import { ScrollArea } from "@/components/ui/scroll-area";

const UserList = ({ searchTerm }) => {
  const { users, getAllUsers, getAllActiveUsers, loading, error } = useGlobalContext();
  const [selectedUser, setSelectedUser] = useState(null);
  const [showActiveOnly, setShowActiveOnly] = useState(false);
  
  const filteredUsers = users.filter((user) =>
    user.username.toLowerCase().includes(searchTerm.toLowerCase())
  );

  useEffect(() => {
    if (showActiveOnly) {
      getAllActiveUsers();
    } else {
      getAllUsers();
    }
  }, [showActiveOnly, getAllUsers, getAllActiveUsers]);

  if (selectedUser) {
    return (
      <UserDetails
        user={selectedUser}
        onBack={() => setSelectedUser(null)}
      />
    );
  }

  return (
    <div className="p-4 h-full w-full">
      <div className="mb-4 flex justify-end items-center">
        <button
          className={`px-4 py-2 rounded-lg ${
            showActiveOnly ? "bg-green-500 text-white" : "bg-gray-300 text-black"
          }`}
          onClick={() => setShowActiveOnly(!showActiveOnly)}
        >
          {showActiveOnly ? "Show All Users" : "Show Active Users"}
        </button>
      </div>

      {filteredUsers.length === 0 ? (
        <p className="text-red-500">No active users found.</p>
      ) : (
        <ScrollArea className="flex-1 max-h-[calc(95vh-200px)] overflow-auto">
          <ul className="space-y-4">
            {filteredUsers.map((user) => (
              <li
                key={user.id}
                className="p-4 border bg-white border-gray-200 rounded-lg flex justify-between items-center"
              >
                <div>
                  <p className="font-medium">{user.username}</p>
                  <p className="text-gray-500 text-sm">{user.email}</p>
                </div>
                <button
                  className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition"
                  onClick={() => setSelectedUser(user)}
                >
                  View Details
                </button>
              </li>
            ))}
          </ul>
        </ScrollArea>
      )}
    </div>
  );
};

export default UserList;
