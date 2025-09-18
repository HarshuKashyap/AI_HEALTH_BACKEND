// testBackend.js
async function testBackend() {
  try {
    const res = await fetch("https://ai-health-backend-r967.onrender.com/chat/message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: "Hello, how are you?" }),
    });

    const data = await res.json();
    console.log("Backend response:", data);
  } catch (err) {
    console.error("Error:", err);
  }
}

testBackend();
