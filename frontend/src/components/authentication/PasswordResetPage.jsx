import React, { useState } from "react";
import { toast } from "react-toastify";
import axios from "axios";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "../ui/card";
import AuthenticationPage from "./AuthenticationPage";

function PasswordResetPage() {
  const [showLogin, setShowLogin] = useState(false); // Додаємо стан для перемикання на логін

  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    setEmail(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email) {
      toast.error("Please enter your email address.");
      return;
    }

    setIsLoading(true);
    try {
      // Надсилаємо запит на бекенд
      await axios.post("/change/request-password-reset", { email });

      toast.success("Password reset link sent to your email.");
    } catch (error) {
      console.error(error);
      if (error.response?.status === 422) {
        toast.error("Invalid email address.");
      } else {
        toast.error("Something went wrong. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Якщо `showLogin` активний, показуємо компонент Login
  if (showLogin) {
    return <AuthenticationPage />;
  }

  return (
    <div className="flex justify-center items-center">
      <Card className="w-[400px] rounded-xl shadow-lg">
        <CardHeader>
          <CardTitle>Reset Your Password</CardTitle>
          <CardDescription>Enter your email to receive a reset link.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="grid gap-4">
              <Input
                type="email"
                placeholder="Your email address"
                value={email}
                onChange={handleInputChange}
                required
                className="focus:border-blue-400"
              />
              <Button
                type="submit"
                disabled={isLoading}
                className="w-full shadow-md bg-blue-500 hover:bg-blue-600 text-white rounded-lg"
              >
                {isLoading ? "Sending..." : "Send Reset Link"}
              </Button>
            </div>
          </form>
        </CardContent>
        <CardFooter>
          <p className="text-sm text-gray-600 text-center">
            Remembered your password?{" "}
            <span
              onClick={() => setShowLogin(true)} // Активуємо стан для показу Login
              className="text-blue-500 hover:underline cursor-pointer"
            >
              Log in
            </span>
          </p>
        </CardFooter>
      </Card>
    </div>
  );
}

export default PasswordResetPage;
