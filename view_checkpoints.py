import sqlite3
from langgraph_database_backend import chatbot

# Retrieve all threads and iterate through their checkpoint history
threads = [row[0] for row in sqlite3.connect("chatbot.db").execute("SELECT DISTINCT thread_id FROM checkpoints")]
for t in threads:
    print(f"\n=== THREAD ID: {t} ===")
    for s in chatbot.get_state_history(config={"configurable": {"thread_id": t}}):
        print(f"[*] Checkpoint: {s.config['configurable'].get('checkpoint_id')}")
        for m in s.values.get("messages", []):
            print(f"  - {m.type.upper()}: {m.content}")
