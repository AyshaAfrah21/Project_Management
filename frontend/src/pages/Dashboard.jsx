import React, { useEffect, useState } from "react";
import { fetchProjects } from "../api/api";

export default function Dashboard() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    fetchProjects().then(setProjects);
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Projects Dashboard</h1>
      {projects.length === 0 ? (
        <p>No projects found.</p>
      ) : (
        projects.map((p) => (
          <div key={p.id} style={{ border: "1px solid #ccc", margin: "10px", padding: "10px" }}>
            <h3>{p.title}</h3>
            <p>{p.description}</p>
            <p>Tasks: {p.tasks ? p.tasks.length : 0}</p>
          </div>
        ))
      )}
    </div>
  );
}
