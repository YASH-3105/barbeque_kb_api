from flask import Flask, request, jsonify
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

if __name__ == "__main__":
    print(">>> Flask App is launching")
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))