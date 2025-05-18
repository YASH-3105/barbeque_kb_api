# barbecue_kb_api/state_transition.py

def determine_next_state(current_state, user_input):
    user_input = user_input.lower()

    if current_state == "collect_city":
        if "bangalore" in user_input or "bengaluru" in user_input or "delhi" in user_input:
            return "collect_contact_information"
        else:
            return "collect_city"  # repeat or re-ask if invalid

    elif current_state == "collect_contact_information":
        if "my name is" in user_input or any(char.isdigit() for char in user_input):
            return "end"  # or next step, e.g., booking creation
        else:
            return "collect_contact_information"  # stay until name & phone valid

    # Add more rules as needed
    return current_state

# Session tracking (simple in-memory dictionary)
session_states = {}

def get_current_state(session_id):
    return session_states.get(session_id, "collect_city")  # default state

def set_current_state(session_id, state):
    session_states[session_id] = state