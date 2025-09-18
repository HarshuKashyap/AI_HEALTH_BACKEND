import { useState } from "react";

export default function FeedbackForm({ onSubmit }) {
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSubmit) onSubmit(rating);
    setComment("");
    alert("Feedback submitted!");
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
      <h3>Feedback</h3>
      <label>
        Rating:
        <select value={rating} onChange={(e) => setRating(Number(e.target.value))}>
          {[1,2,3,4,5].map((n) => <option key={n} value={n}>{n}</option>)}
        </select>
      </label>
      <br />
      <label>
        Comment:
        <input value={comment} onChange={(e) => setComment(e.target.value)} style={{ width: "100%" }} />
      </label>
      <br />
      <button type="submit" style={{ marginTop: "5px" }}>Submit</button>
    </form>
  );
}
