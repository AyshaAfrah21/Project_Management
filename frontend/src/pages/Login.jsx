import React, { useState } from "react";
import { login, setAuthToken } from "../api/api";
import { useNavigate } from "react-router-dom";
import "./Login.css"; // ✅ Import CSS

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const data = await login(email, password);
      console.log("Login success:", data);

      if (data && data.access_token) {
        localStorage.setItem("pm_token", data.access_token);
        setAuthToken(data.access_token);
        navigate("/dashboard");
      } else {
        alert("Unexpected response from server");
      }
    } catch (err) {
      console.error("Login error:", err);
      alert("Invalid credentials");
    }
  }

  return (
    <div className="login-container">
      <form className="login-card" onSubmit={handleSubmit}>
        <h2>Welcome Back</h2>
        <p className="login-subtitle">Login to your account</p>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">Login</button>
      </form>
    </div>
  );
}
