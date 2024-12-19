import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { toast } from "react-toastify";
import { Link, useNavigate } from "react-router-dom";
import { register, reset } from "@/context/auth/AuthSlice";
import { Button } from "../ui/button";
import { Input } from "../ui/input";

function Register() {
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password: "",
    });

    const { username, email, password } = formData;
    const { user, isLoading, isError, isSuccess, message } = useSelector(
        (state) => state.auth
    );
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        dispatch(register(formData));
    };

    useEffect(() => {
        if (isError) toast.error(message);
        if (isSuccess || user) {
            navigate("/home");
            toast.success("Registration successful!");
        }
        dispatch(reset());
    }, [isError, isSuccess, user, navigate, dispatch]);

    return (
        <div className="flex flex-col gap-4">
            <Input
                id="username"
                type="text"
                placeholder="Username"
                name="username"
                value={username}
                onChange={handleChange}
                className="focus:border-blue-400"
                required
            />
            <Input
                id="email"
                type="email"
                placeholder="Email Address"
                name="email"
                value={email}
                onChange={handleChange}
                className="focus:border-blue-400"
                required
            />
            <Input
                id="password"
                type="password"
                placeholder="Password"
                name="password"
                value={password}
                onChange={handleChange}
                className="focus:border-blue-400"
                required
            />
            <Button
                className="bg-blue-500 hover:bg-blue-600 text-white w-full rounded-lg py-2"
                onClick={handleSubmit}
                disabled={isLoading}
            >
                {isLoading ? "Signing up..." : "Sign up"}
            </Button>
        </div>
    );
}

export default Register;
