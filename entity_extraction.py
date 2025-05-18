import re

def extract_entities(user_input, state):
    entities = {}
    if state == "collect_contact_information":
        phone_match = re.search(r"\b\d{10}\b", user_input)
        if phone_match:
            entities["phone"] = phone_match.group()
        name_match = re.search(r"my name is (\w+)", user_input, re.IGNORECASE)
        if name_match:
            entities["name"] = name_match.group(1)
    elif state == "collect_city":
        if "bangalore" in user_input.lower():
            entities["city"] = "Bangalore"
        elif "delhi" in user_input.lower():
            entities["city"] = "Delhi"
    return entities