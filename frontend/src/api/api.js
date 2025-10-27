import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:5000/api",
});

export function setAuthToken(token) {
  if (token) API.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  else delete API.defaults.headers.common["Authorization"];
}

export async function login(email, password) {
  try {
    const resp = await API.post("/auth/login", { email, password });
    return resp.data; // backend returns { access_token, user }
  } catch (err) {
    console.error("Login API Error:", err);
    throw err; // propagate error so frontend can handle
  }
}


export async function fetchProjects() {
  const res = await API.get("/projects/");
  return res.data;
}

export async function fetchTasksByProject(projectId) {
  const res = await API.get(`/tasks/project/${projectId}`);
  return res.data;
}
