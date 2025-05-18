from flask import Flask, request, jsonify, render_template
from prompt_templates import prompt_templates
from state_transition import get_current_state, get_next_state
from entity_extraction import extract_entities
from openai_utils import get_openai_response
import json
import os
import re
import pprint



print(">>>App starting.....")

def log_failed_query(query_text):
    with open("logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"[FAILED QUERY]{query_text}\n")

kb_chunks = []
try:
    with open("kb_data.json", "r", encoding="utf-8") as f:
        kb_chunks = json.load(f)
    print(f">>> Loaded {len(kb_chunks)} KB chunks.")
except Exception as e:
    print(f">>> ERROR LOADING kb_data.json: {e}")



app = Flask(__name__)

@app.route("/get_prompt", methods=["POST"])
def get_prompt():
    data = request.json
    session_id = data.get("session_id")
    user_input = data.get("user_input")

    current_state = get_current_state(session_id)
    template = prompt_templates.get(current_state)

    if not template:
        return jsonify({"error": "Invalid conversation state"}), 400

    # Extract entities
    extracted_entities = extract_entities(user_input, current_state)

    # Prepare variables for prompt
    formatted_prompt = ""
    if current_state == "collect_contact_information":
        formatted_prompt = template["steps"][0]
    elif current_state == "master_collect":
        formatted_prompt = template["prompt"].format(**extracted_entities)
    elif current_state == "master_inform":
        formatted_prompt = template["template"].format(**extracted_entities)
    elif current_state == "collect_city":
        formatted_prompt = template["instructions"]
    else:
        formatted_prompt = "Unknown state logic"

    # Get OpenAI response
    bot_response = get_openai_response(formatted_prompt)

    # Determine next state
    next_state = get_next_state(session_id, current_state, extracted_entities)

    return jsonify({
        "bot_response": bot_response,
        "next_state": next_state
    })

@app.route("/")
def home():
    print(">>> Serving index.htm")
    return render_template("index.html")

# Load knowledge base
with open("kb_data.json", "r", encoding="utf-8") as f:
    kb_chunks = json.load(f)


# Utility: Token count (approximate using word count)
def token_count(text):
    return len(text.split())


# Route: Get all chunks (optional, for admin/debugging)
@app.route("/kb/all", methods=["GET"])
def get_all_chunks():
    city = request.args.get("city")
    chunk_type = request.args.get("type")

    chunks = kb_chunks
    if city:
        chunks = [chunk for chunk in chunks if chunk["city"].lower() == city.lower()]
    if chunk_type:
        chunks = [chunk for chunk in chunks if chunk["type"] == chunk_type]
        
    return jsonify(chunks), 200


# Route: Get chunk by ID
@app.route("/kb/chunk/<chunk_id>", methods=["GET"])
def get_chunk_by_id(chunk_id):
    chunk = next((c for c in kb_chunks if c["id"] == chunk_id), None)
    if chunk:
        return jsonify(chunk), 200
    return jsonify({"message": "Chunk not found"}), 404


# Route: Basic keyword search
@app.route("/kb/search", methods=["POST"])
def search_chunks():
    data = request.get_json()
    query = data.get("query", "").lower()

    if not query:
        return jsonify({"message": "Query is required"}), 400

    results = [chunk for chunk in kb_chunks if query in chunk["content"].lower()]
    if not results:
        return jsonify({"message": "No relevant information found."}), 404

    # Return top 1 or 2 chunks within 800 tokens
    total_tokens = 0
    filtered = []
    for chunk in results:
        count = token_count(chunk["content"])
        if total_tokens + count <= 800:
            filtered.append(chunk)
            total_tokens += count
        else:
            break

    return jsonify(filtered), 200


# Route: Route user query (basic matching)
@app.route("/kb/query", methods=["POST"])
def classify_and_route():
    data = request.get_json()
    query = data.get("query", "").lower()

    if not query:
        return jsonify({"message": "Query text required"}), 400

    # Simple keyword routing (extend as needed)
    if "menu" in query or "jain" in query or "halal" in query:
        intent_type = "faq"
        category = "menu_drinks"
    elif "offer" in query or "discount" in query:
        intent_type = "offers"
        category = None
    elif "time" in query or "hours" in query:
        intent_type = "timings"
        category = None
    elif "book" in query or "reservation" in query:
        intent_type = "booking_policy"
        category = None
    elif "address" in query or "location" in query:
        intent_type = "branch_info"
        category = None
    else:
        log_failed_query(query)
        return jsonify({"message": "Sorry, I couldn't find relevant information for your query."}), 404

    results = [chunk for chunk in kb_chunks if chunk["type"] == intent_type]
    if category:
        results = [chunk for chunk in results if chunk.get("category") == category]

    if not results:
        log_failed_query(query)
        return jsonify({"message": "Information not found in the knowledge base."}), 404

    # Token limit cap
    total_tokens = 0
    filtered = []
    for chunk in results:
        count = token_count(chunk["content"])
        if total_tokens + count <= 800:
            filtered.append(chunk)
            total_tokens += count
        else:
            break

    pprint.pprint(filtered)
    return jsonify(filtered), 200
     
@app.route("/kb/fallback", methods=["POST"])
def fallback_response():
    return jsonify({
        "message": "This query appears to be outside my knowledge base. Please contact customer support or try a different question."
    }), 200



print(app.url_map)

@app.route("/chat", methods=["POST"])
def chat_handler():
    data = request.get_json()
    user_input = data.get("query", "")
    current_state = data.get("state", "")
    collected_variables = data.get("variables", {})

    if not current_state:
        return jsonify({"error": "Current state is required"}), 400

    # Step 1: Extract new entities from user input
    new_entities = extract_entities(user_input, current_state)
    collected_variables.update(new_entities)

    # Step 2: Decide the next state based on current state and extracted entities
    next_state = get_next_state(current_state, user_input, collected_variables)

    # Step 3: Fetch prompt template and fill in variables
    if next_state not in prompt_templates:
        return jsonify({"error": f"Unknown next state: {next_state}"}), 500

    prompt_data = prompt_templates[next_state]
    if next_state == "master_collect":
        filled_prompt = prompt_data["prompt"].format(**collected_variables)
    elif next_state == "master_inform":
        filled_prompt = prompt_data["template"].format(**collected_variables)
    else:
        # For simple prompt types (like single instruction)
        filled_prompt = prompt_data.get("instructions") or prompt_data.get("steps", [""])[0]

    # Step 4: Optionally generate LLM response
    llm_response = generate_response(filled_prompt)

    return jsonify({
        "next_state": next_state,
        "variables": collected_variables,
        "prompt": filled_prompt,
        "response": llm_response
    }), 200



if __name__ == "__main__":
    print(">>> Flask App is launching")
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))