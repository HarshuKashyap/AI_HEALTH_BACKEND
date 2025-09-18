import { useState, useRef, useEffect } from "react";

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    // User message add karo
    const userMsg = { sender: "user", text: input };
    setMessages(prev => [...prev, userMsg]);

    try {
      const res = await fetch("https://ai-health-backend-r967.onrender.com/chat/message", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message: input }),
});


      const data = await res.json();
      const aiMsg = { sender: "ai", text: data.answer || "No answer found." };
      setMessages(prev => [...prev, aiMsg]);
    } catch (err) {
      console.error(err);
      const aiMsg = { sender: "ai", text: "Backend error! Try again later." };
      setMessages(prev => [...prev, aiMsg]);
    }

    setInput("");
  };

  return (
    <div style={{
      maxWidth: 600,
      margin: "2rem auto",
      border: "1px solid #ccc",
      borderRadius: 12,
      padding: 16,
      display: "flex",
      flexDirection: "column",
      height: "70vh"
    }}>
      <div style={{
        flex: 1,
        overflowY: "auto",
        marginBottom: 10,
        paddingRight: 8
      }}>
        {messages.map((msg, i) => (
          <div key={i} style={{
            display: "flex",
            justifyContent: msg.sender === "user" ? "flex-end" : "flex-start",
            marginBottom: 8
          }}>
            <span style={{
              maxWidth: "70%",
              padding: "10px 14px",
              borderRadius: 16,
              backgroundColor: msg.sender === "user" ? "#dcf8c6" : "#f1f0f0",
              boxShadow: "0 1px 3px rgba(0,0,0,0.1)"
            }}>
              {msg.text}
            </span>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <div style={{ display: "flex", gap: 8 }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          style={{
            flex: 1,
            padding: 10,
            borderRadius: 12,
            border: "1px solid #ccc"
          }}
        />
        <button
          onClick={sendMessage}
          style={{
            padding: "10px 16px",
            borderRadius: 12,
            border: "none",
            backgroundColor: "#4caf50",
            color: "#fff",
            cursor: "pointer"
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}
