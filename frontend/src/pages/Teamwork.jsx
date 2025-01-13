import React, { useState, useEffect } from "react";
import { useGlobalContext } from "@/context/GlobalContext";
import { ScrollArea } from "@/components/ui/scroll-area";
import { toast } from "react-toastify";

const Teamwork = () => {
  const {
    currentUser,
    getCurrentUser,
    getMyTeams,
    inviteUserToTeam,
    createTeam,
    getTeamUsers,
    removeUserFromTeam,
    users,
    getAllUsers,
  } = useGlobalContext();

  const [groups, setGroups] = useState([]); // Список груп із сервера
  const [newGroupName, setNewGroupName] = useState(""); // Назва для створення нової групи
  const [selectedGroup, setSelectedGroup] = useState(null); // Вибрана група
  const [groupMembers, setGroupMembers] = useState([]); // Учасники вибраної групи
  const [allUsers, setAllUsers] = useState([]); // Усі доступні користувачі
  const [loadingGroups, setLoadingGroups] = useState(false); // Стан завантаження груп

  useEffect(() => {
    // Ініціалізація даних виконується лише один раз
    const initialize = async () => {
      try {
        await getCurrentUser();
        await getAllUsers();
        const teams = await getMyTeams();
        setGroups(teams);
      } catch (err) {
        console.error("Error initializing Teamwork component:", err);
        toast.error("Failed to load data. Please try again.");
      }
    };

    initialize();
    // Порожній масив залежностей, щоб цей `useEffect` виконувався лише один раз
  }, []);

  useEffect(() => {
    // Оновлення списку користувачів
    setAllUsers(users);
  }, [users]);

  const handleSelectGroup = async (group) => {
    if (selectedGroup?.id === group.id) return; // Якщо група вже обрана, пропускаємо
    setSelectedGroup(group);
    try {
      const members = await getTeamUsers(group.id);
      setGroupMembers(members);
    } catch (err) {
      console.error("Failed to load group members:", err);
      toast.error("Failed to load group members.");
    }
  };

  const handleCreateGroup = async () => {
    if (!newGroupName) {
      toast.error("Group name cannot be empty!");
      return;
    }

    try {
      const newGroup = await createTeam(newGroupName);
      setGroups([...groups, newGroup]);
      setNewGroupName("");
      toast.success("Group created successfully!");
    } catch (err) {
      console.error("Failed to create group:", err);
      toast.error("Failed to create group.");
    }
  };

  const handleRemoveMember = async (userId) => {
    if (!selectedGroup) return;

    try {
      await removeUserFromTeam(selectedGroup.id, userId);
      const updatedMembers = groupMembers.filter((member) => member.id !== userId);
      setGroupMembers(updatedMembers);
      toast.success("User removed from the group!");
    } catch (err) {
      console.error("Failed to remove member:", err);
      toast.error("Failed to remove member.");
    }
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
        <button onClick={handleCreateGroup} className="bg-blue-500 text-white px-4 py-2 rounded">
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
              onClick={() => handleSelectGroup(group)}
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
            {groupMembers.map((member) => (
              <li key={member.id} className="flex justify-between items-center p-2 border rounded">
                <span>{member.username || "Unknown User"}</span>
                {isAdmin && (
                  <button
                    onClick={() => handleRemoveMember(member.id)}
                    className="bg-red-500 text-white px-2 py-1 rounded"
                  >
                    Remove
                  </button>
                )}
              </li>
            ))}
          </ul>

          {/* Додавання учасників */}
          {isAdmin && (
            <div className="mt-4">
              <h3 className="text-lg font-medium mb-2">Add Members:</h3>
              <ul className="space-y-2">
                {allUsers
                  .filter((user) => !groupMembers.find((member) => member.id === user.id))
                  .map((user) => (
                    <li
                      key={user.id}
                      className="flex justify-between items-center p-2 border rounded"
                    >
                      <span>{user.username}</span>
                      <button
                        onClick={() => inviteUserToTeam(selectedGroup.id, user.email)}
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
