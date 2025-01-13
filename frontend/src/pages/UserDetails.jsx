import React from "react";

const UserDetails = ({ user, onBack }) => {
  return (
    <div className="p-4">
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition mb-4"
        onClick={onBack}
        >
        Back to User List
      </button>
      <div className="p-4 bg-white border border-gray-200 rounded-lg">
        <p>
          <strong>ID:</strong> {user.id}
        </p>
        <p>
          <strong>Username:</strong> {user.username}
        </p>
        <p>
          <strong>Email:</strong> {user.email}
        </p>
        <p>
          <strong>Active:</strong>{" "}
          <span className={user.is_active ? "text-green-500" : "text-red-500"}>
              {user.is_active ? "Yes" : "No"}
          </span>
        </p>
        <p>
          <strong>Email Verified:</strong>{" "}
          {user.email_is_verified ? "Yes" : "No"}
        </p>
        <p>
          <strong>Created At:</strong> {new Date(user.created_at).toLocaleString()}
        </p>
      </div>
    </div>
  );
};

export default UserDetails;