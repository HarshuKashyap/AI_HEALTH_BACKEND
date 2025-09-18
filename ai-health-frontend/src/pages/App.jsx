import ChatBox from "./components/ChatBox";
import FeedbackForm from "./components/FeedbackForm";
import StatsDashboard from "./components/StatsDashboard";

export default function App() {
  return (
    <div>
      <h1>AI Health Assistant</h1>
      <ChatBox />
      <FeedbackForm />
      <StatsDashboard />
    </div>
  );
}
