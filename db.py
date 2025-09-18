import sqlite3
import json

DB_NAME = "health_assistant.db"

# DB connection
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            ai_response TEXT,
            feedback TEXT,
            rating INTEGER,
            prediction_id INTEGER,
            correct_disease TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Save query
def save_query(user_input, ai_response):
    conn = get_db_connection()
    cursor = conn.cursor()
    if isinstance(ai_response, dict):
        ai_response = json.dumps(ai_response)
    cursor.execute(
        "INSERT INTO queries (user_input, ai_response) VALUES (?, ?)",
        (user_input, ai_response)
    )
    conn.commit()
    conn.close()

# Save feedback + optional fields safely
def save_feedback(query_id, feedback, rating=None, prediction_id=None, correct_disease=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "UPDATE queries SET feedback=?"
    params = [feedback]

    if rating is not None:
        query += ", rating=?"
        params.append(rating)
    if prediction_id is not None:
        query += ", prediction_id=?"
        params.append(prediction_id)
    if correct_disease is not None:
        query += ", correct_disease=?"
        params.append(correct_disease)

    query += " WHERE id=?"
    params.append(query_id)

    try:
        cursor.execute(query, params)
        if cursor.rowcount == 0:
            raise Exception(f"Query ID {query_id} not found in DB")
        conn.commit()
    finally:
        conn.close()

# Get recent queries
def get_history(limit=20):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM queries ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Get stats for analytics
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Total queries
    cursor.execute("SELECT COUNT(*) as total_queries FROM queries")
    total_queries = cursor.fetchone()["total_queries"]

    # Top symptoms
    cursor.execute("""
        SELECT user_input, COUNT(*) as count
        FROM queries
        GROUP BY user_input
        ORDER BY count DESC
        LIMIT 5
    """)
    top_symptoms = [{"symptoms": row["user_input"], "count": row["count"]} for row in cursor.fetchall()]

    # Top AI responses
    cursor.execute("""
        SELECT ai_response, COUNT(*) as count
        FROM queries
        GROUP BY ai_response
        ORDER BY count DESC
        LIMIT 5
    """)
    top_responses = []
    for row in cursor.fetchall():
        try:
            resp = json.loads(row["ai_response"])
        except:
            resp = row["ai_response"]
        top_responses.append({"ai_response": resp, "count": row["count"]})

    conn.close()

    return {
        "total_queries": total_queries,
        "top_symptoms": top_symptoms,
        "top_responses": top_responses
    }

# Auto init
if __name__ == "__main__":
    init_db()
    print("Database initialized 🚀")
