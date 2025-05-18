from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

app = Flask(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open your Google Sheet by name
sheet = client.open("PostCallLogs").sheet1  # Change if your sheet name is different

@app.route("/log_conversation", methods=["POST"])
def log_conversation():
    try:
        data = request.get_json()

        row = [
            data.get("modality", "NA"),
            data.get("call_time", str(datetime.datetime.now())),
            data.get("phone_number", "NA"),
            data.get("call_outcome", "NA"),
            data.get("room_name", "NA"),
            data.get("booking_date", "NA"),
            data.get("booking_time", "NA"),
            data.get("number_of_guests", "NA"),
            data.get("customer_name", "NA"),
            data.get("call_summary", "NA")
        ]

        sheet.append_row(row)
        return jsonify({"status": "success", "message": "Data logged"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    print("Server is running at http:localhost:5000")
    app.run(debug=True, port=5000)