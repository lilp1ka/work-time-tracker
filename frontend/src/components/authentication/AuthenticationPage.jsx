import React, { useState } from "react";
import Register from "./Register";
import Login from "./Login";
import PasswordResetPage from "./PasswordResetPage";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "../ui/tabs";

function AuthenticationPage() {
  const [activeTab, setActiveTab] = useState("login");

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  return (
    <div className="h-screen flex justify-center items-center bg-gray-100">
      {activeTab === "resetPassword" ? (
        <div className="flex justify-center items-center w-full h-full">
          <PasswordResetPage />
        </div>
      ) : (
        <div className="flex flex-row bg-white shadow-lg rounded-lg w-[900px] overflow-hidden">
          {/* Ліва частина з ілюстрацією */}
          <div className="hidden md:flex flex-1 justify-center items-center bg-blue-50">
            <img
              src="photo_2024-12-05_01-22-01.jpg"
              alt="Illustration"
              className="max-w-full max-h-full object-contain"
            />
          </div>
          {/* Права частина з формами */}
          <div className="flex flex-col flex-1 justify-center items-center p-8">
            <h2 className="text-2xl font-bold mb-6 text-center">Welcome!</h2>
            <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full max-w-[350px]">
              {/* Вкладки */}
              <TabsList className="grid w-full grid-cols-2 mb-6 bg-indigo-100 rounded-lg">
                <TabsTrigger
                  value="login"
                  className={`py-2 text-lg font-medium text-center ${
                    activeTab === "login" ? "text-blue-500" : "text-gray-600"
                  }`}
                >
                  Login
                </TabsTrigger>
                <TabsTrigger
                  value="register"
                  className={`py-2 text-lg font-medium text-center ${
                    activeTab === "register" ? "text-blue-500" : "text-gray-600"
                  }`}
                >
                  Register
                </TabsTrigger>
              </TabsList>
              {/* Вміст вкладок */}
              <TabsContent value="login">
                <Login handleTabChange={handleTabChange} />
              </TabsContent>
              <TabsContent value="register">
                <Register />
              </TabsContent>
            </Tabs>
          </div>
        </div>
      )}
    </div>
  );
}

export default AuthenticationPage