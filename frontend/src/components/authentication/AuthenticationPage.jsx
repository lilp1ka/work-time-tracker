import React, { useState } from "react";
import Register from "./Register";
import Login from "./Login";
import PasswordResetPage from "./PasswordResetPage";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "../ui/tabs";

function AuthenticationPage() {
  const [activeTab, setActiveTab] = useState("login"); // Стан для активної вкладки

  const handleTabChange = (tab) => {
    setActiveTab(tab); // Змінюємо стан вкладки
  };

  return (
    <div className="h-screen flex justify-center items-center bg-gray-100">
      {activeTab === "resetPassword" ? (
        // Якщо активна вкладка "resetPassword", показуємо тільки компонент для скидання пароля
        <div className="flex justify-center items-center w-full h-full">
          <PasswordResetPage />
        </div>
      ) : (
        // В іншому випадку показуємо стандартну сторінку
        <div className="flex bg-white shadow-lg rounded-lg w-[900px] overflow-hidden">
          {/* Ліва частина з ілюстрацією */}
          <div className="hidden md:flex flex-1 justify-center items-center bg-blue-50">
            <img
              src="photo_2024-12-05_01-22-01.jpg"
              alt="Illustration"
              className="max-w-[80%], max-h-[100%]"
            />
          </div>
          {/* Права частина з формами */}
          <div className="flex flex-col flex-1 justify-center items-center p-8">
            <h2 className="text-2xl font-bold mb-6">Welcome!</h2>
            <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full max-w-[350px]">
              {/* Вкладки */}
              <TabsList className="grid w-full grid-cols-2 mb-4 bg-indigo-100">
                <TabsTrigger
                  value="login"
                  className={`py-2 text-lg font-medium text-center ${
                    activeTab === "login" ? "border-b-2 border-blue-500" : "border-transparent"
                  }`}
                >
                  Login
                </TabsTrigger>
                <TabsTrigger
                  value="register"
                  className={`py-2 text-lg font-medium text-center ${
                    activeTab === "register" ? "border-b-2 border-blue-500" : "border-transparent"
                  }`}
                >
                  Register
                </TabsTrigger>
              </TabsList>
              {/* Вміст вкладок */}
              <TabsContent value="login">
                <Login />
                <div className="mt-2 text-sm text-center text-gray-600">
                  <button
                    className="text-blue-500 hover:underline"
                    onClick={() => handleTabChange("resetPassword")}
                  >
                    Forgot Password?
                  </button>
                </div>
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

export default AuthenticationPage;
