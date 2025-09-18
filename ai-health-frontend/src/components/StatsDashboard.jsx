export default function StatsDashboard({ totalQueries, ratings, topQueries }) {
  const avgRating = ratings.length ? (ratings.reduce((a,b)=>a+b,0)/ratings.length).toFixed(1) : 0;

  return (
    <div style={{ border: "1px solid #ccc", padding: "10px", borderRadius: "8px" }}>
      <h3>📊 App Stats</h3>
      <p><b>Total Queries:</b> {totalQueries}</p>
      <p><b>Average Rating:</b> {avgRating}</p>
      <p><b>🔥 Top Queries:</b></p>
      <ul>
        {topQueries.length ? topQueries.map((q,i) => <li key={i}>{q}</li>) : <li>No queries yet</li>}
      </ul>
    </div>
  );
}
