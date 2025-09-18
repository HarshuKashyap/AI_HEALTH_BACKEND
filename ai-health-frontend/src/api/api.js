import axios from "axios";

// Base URL (deployment friendly)
const BASE_URL = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";

// Secure headers
const headers = {
  "X-API-Key": "supersecret123",
  "Content-Type": "application/json",
};

// Axios instance (reusable)
const api = axios.create({
  baseURL: BASE_URL,
  headers,
  timeout: 10000, // 10 sec timeout
});

// ------------------ APIs ------------------ //

// Chat query -> /predict
export async function sendQuery(message) {
  const response = await fetch("http://127.0.0.1:8000/chat/message", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message })
  });

  if (!response.ok) throw new Error("Network response was not ok");
  return response.json();
}


// Feedback -> /feedback
export const sendFeedback = async (feedback) => {
  try {
    const res = await api.post("/feedback", feedback);
    return res.data || { message: "Feedback not saved" };
  } catch (err) {
    console.error("Error in sendFeedback:", err.response?.data || err.message);
    return { message: "Backend error! Could not send feedback." };
  }
};

// Stats -> /stats
export const getStats = async () => {
  try {
    const res = await api.get("/stats");
    return res.data || { total_queries: 0, avg_rating: 0, top_queries: [] };
  } catch (err) {
    console.error("Error in getStats:", err.response?.data || err.message);
    return { total_queries: 0, avg_rating: 0, top_queries: [] };
  }
};

// Health check -> /health
export const checkHealth = async () => {
  try {
    const res = await api.get("/health");
    return res.data || { status: "unknown" };
  } catch (err) {
    console.error("Error in checkHealth:", err.response?.data || err.message);
    return { status: "down" };
  }
};
