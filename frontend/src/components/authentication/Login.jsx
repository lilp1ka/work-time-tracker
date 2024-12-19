import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { login, reset } from "@/context/auth/AuthSlice";
import { Button } from "../ui/button";
import { Input } from "postcss";

function Login() {
    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const { email, password } = formData;
    const { user, isLoading, isError, isSuccess, message } = useSelector(
        (state) => state.auth
    );
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = () => {
        dispatch(login({ email, password }));
    };

    useEffect(() => {
        if (isError) toast.error(message);
        if (isSuccess || user) {
            navigate("/home");
            toast.success("Welcome to your account!");
        }
        dispatch(reset());
    }, [isError, isSuccess, user, navigate, dispatch, message]);

    return (
        <div className="flex flex-col gap-4">
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
                {isLoading ? "Logging in..." : "Sign in"}
            </Button>
        </div>
    );
}

export default Login;
