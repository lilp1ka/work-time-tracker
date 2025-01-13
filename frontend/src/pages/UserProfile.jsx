import React from "react";
import { useGlobalContext } from "@/context/GlobalContext";

const UserProfile = () => {
  const { currentUser, loading, error } = useGlobalContext();

  if (!currentUser) {
    return <div>No user logged in</div>;
  }

  return (
    <div className="h-full w-full flex items-center gap-2 pt-4 pr-20">
      <div className="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center text-xl font-bold text-white">
        {currentUser.username[0].toUpperCase()}
      </div>
      <div className="text-sm font-medium">{currentUser.username}</div>
    </div>
  );
};

export default UserProfile;