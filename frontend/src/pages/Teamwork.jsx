import React, { useState, useEffect } from "react";
import { useGlobalContext } from "@/context/GlobalContext";
import { ScrollArea } from "@/components/ui/scroll-area";
import { toast } from "react-toastify";

const Teamwork = () => {
  const { currentUser, getCurrentUser, users, getAllUsers } = useGlobalContext();
  const [groups, setGroups] = useState([]); // Список груп
  const [newGroupName, setNewGroupName] = useState(""); // Для створення нової групи
  const [selectedGroup, setSelectedGroup] = useState(null); // Вибрана група
  const [groupMembers, setGroupMembers] = useState([]); // Учасники вибраної групи
  const [allUsers, setAllUsers] = useState([]); // Всі доступні користувачі
  const [initialized, setInitialized] = useState(false); // Флаг для контролю ініціалізації

  useEffect(() => {
    // Запити виконуються лише один раз при першому рендері компонента
    if (!initialized) {
      getCurrentUser();
      getAllUsers();
      setInitialized(true); // Встановлюємо флаг після виконання запитів
    }
  }, [initialized, getCurrentUser, getAllUsers]);

  useEffect(() => {
    // Завантажуємо доступних користувачів
    setAllUsers(users);
  }, [users]);

  const createGroup = () => {
    if (!newGroupName) {
      alert("Group name cannot be empty!");
      return;
    }

    const newGroup = {
      id: groups.length + 1,
      name: newGroupName,
      created_by: currentUser.id,
      members: [],
    };

    setGroups([...groups, newGroup]);
    setNewGroupName("");
    toast.success("Group created successfully!");
  };

  const addMember = (userId) => {
    if (!selectedGroup) return;
    const updatedGroup = {
      ...selectedGroup,
      members: [...selectedGroup.members, userId],
    };

    const updatedGroups = groups.map((group) =>
      group.id === selectedGroup.id ? updatedGroup : group
    );

    setGroups(updatedGroups);
    setSelectedGroup(updatedGroup);
  };

  const removeMember = (userId) => {
    if (!selectedGroup) return;
    const updatedGroup = {
      ...selectedGroup,
      members: selectedGroup.members.filter((id) => id !== userId),
    };

    const updatedGroups = groups.map((group) =>
      group.id === selectedGroup.id ? updatedGroup : group
    );

    setGroups(updatedGroups);
    setSelectedGroup(updatedGroup);
  };

  const isAdmin = selectedGroup && selectedGroup.created_by === currentUser.id;

  return (
    <div className="p-4 h-full w-full">

      {/* Створення групи */}
      <div className="mb-6">
        <input
          type="text"
          placeholder="Enter group name"
          value={newGroupName}
          onChange={(e) => setNewGroupName(e.target.value)}
          className="border rounded p-2 mr-2"
        />
        <button onClick={createGroup} className="bg-blue-500 text-white px-4 py-2 rounded">
          Create Group
        </button>
      </div>

      {/* Вибір групи */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">Your Groups</h2>
        <ul className="space-y-2">
          {groups.map((group) => (
            <li
              key={group.id}
              onClick={() => setSelectedGroup(group)}
              className={`cursor-pointer p-2 border rounded ${
                selectedGroup?.id === group.id ? "bg-blue-100" : ""
              }`}
            >
              {group.name}
            </li>
          ))}
        </ul>
      </div>

      {/* Інформація про групу */}
      {selectedGroup && (
        <ScrollArea className="flex-1 max-h-[calc(83vh-200px)] overflow-auto">
          <h2 className="text-xl font-semibold mb-2">Group: {selectedGroup.name}</h2>
          <p>Admin: {selectedGroup.created_by === currentUser.id ? "You" : "Other"}</p>
          <h3 className="text-lg font-medium mt-4">Members:</h3>
          <ul className="space-y-2">
            {selectedGroup.members.map((memberId) => {
              const user = allUsers.find((user) => user.id === memberId);
              return (
                <li key={memberId} className="flex justify-between items-center p-2 border rounded">
                  <span>{user?.username || "Unknown User"}</span>
                  {isAdmin && (
                    <button
                      onClick={() => removeMember(memberId)}
                      className="bg-red-500 text-white px-2 py-1 rounded"
                    >
                      Remove
                    </button>
                  )}
                </li>
              );
            })}
          </ul>

          {/* Додавання учасників */}
          {isAdmin && (
            <div className="mt-4">
              <h3 className="text-lg font-medium mb-2">Add Members:</h3>
              <ul className="space-y-2">
                {allUsers
                  .filter((user) => !selectedGroup.members.includes(user.id))
                  .map((user) => (
                    <li key={user.id} className="flex justify-between items-center p-2 border rounded">
                      <span>{user.username}</span>
                      <button
                        onClick={() => addMember(user.id)}
                        className="bg-green-500 text-white px-2 py-1 rounded"
                      >
                        Add
                      </button>
                    </li>
                  ))}
              </ul>
            </div>
          )}
        </ScrollArea>
      )}
    </div>
  );
};

export default Teamwork;
