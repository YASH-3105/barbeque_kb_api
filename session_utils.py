# session_utils.py

# Simple in-memory store for session states
session_store = {}

def get_current_state(session_id):
    return session_store.get(session_id, "collect_city")

def update_session(session_id, next_state):
    session_store[session_id] = next_state