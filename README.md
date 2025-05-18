Barbeque Nation Chatbot Assistant – README

This project implements an intelligent chatbot assistant for Barbeque Nation, capable of handling inbound booking inquiries and FAQs across Bengaluru and New Delhi. The solution consists of four major components: Chatbot backend, Knowledge Base, State-driven Conversation Flow, and Post-call Analysis.


---

1. Chatbot System (LLM-Driven)

Built a Flask API route /chatbot that accepts session_id and user_input, manages conversation states, and returns dynamic responses.

Integrated with OpenAI's gpt-3.5-turbo model via the official openai>=1.0.0 SDK using secure API key handling through environment variables.

Designed modular response generation using prompt templates corresponding to different conversation states.

Added fallback handling and default prompts to maintain graceful responses for undefined cases.



---

2. Knowledge Base API

Developed a /kb/all route to serve all branch-specific KB chunks (Bengaluru, Delhi).

Preprocessed data and chunked it under 800 tokens per chunk to fit LLM input limits.

Stored the KB as structured JSON and supported retrieval in the frontend for transparency.

Integrated a "Show Knowledge Base Chunks" toggle in the HTML UI to review current data used by the chatbot.

### Knowledge Base API – Barbeque Nation

*Base URL:* https://barbeque-kb-api.onrender.com

*Endpoints:*
- /kb/all – Get all knowledge chunks (GET)
- /kb/chunk/<chunk_id> – Get chunk by ID (GET)
- /kb/search – Search chunks by keyword (POST)
- /kb/query – Smart query routing (POST)
- /kb/fallback – Fallback response (POST)

*Example Query:*
```bash
curl -X POST https://barbeque-kb-api.onrender.com/kb/query \
-H "Content-Type: application/json" \
-d '{"query": "Do you serve Halal food?"}'




---

3. Conversation Flow Logic

Implemented a finite-state-driven system to handle step-by-step data collection:

collect_city

collect_contact_information

master_collect

master_inform


Used session_id-based context management via a global dictionary to track user variables and state.

Created prompt templates for each state to dynamically fill LLM inputs with user-provided data.

Logic defined in state_transition.py determines state shifts based on keyword presence and input structure.



---

4. Post-Call Analysis

   In this, I have to build a Flask-based backend with Google sheets API integration:
 - aceepts post-interaction data via API
 - Logs into goggle sheet

   Tech stack:
   Python (Flask) for API backend

Google Sheets API for logging

OAuth2 credentials for Google integration

In data format I have taken an example 
the written the python script
after that , I did google sheet setup
- Now, I setupt google sheets API by going to google cloud console, 
creating new project , enabling the Google sheets API
and now creating service account will give me the credentials.json file 
then, I gave the editor access with service account after downloading credentials file
then I integrated both 

- For testing it I run a code 
curl -X POST http://localhost:5000/log_conversation \
-H "Content-Type: application/json" \
-d '{
  "modality": "Call",
  "call_time": "2025-01-03 12:50:07",
  "phone_number": "9833620578",
  "call_outcome": "ROOM_AVAILABILITY",
  "room_name": "Executive Room",
  "booking_date": "2025-01-03",
  "booking_time": "15:30",
  "number_of_guests": "2",
  "customer_name": "Aryamann",
  "call_summary": "User called to inquire about availability and wanted a booking voucher."
}'
  after clicking enter my data was logged into the sheet

I have also attatched the screenshots of my work

here's tthe link to the excel sheet : https://docs.google.com/spreadsheets/d/16dqa3hqc-bQWYx36XElAw9REy5aEyAV9-rFGiuAfypM/edit?gid=0#gid=0




This data will be used to optimize prompts, KB content, and LLM temperature settings later.



---

Deployment & UI

Hosted the project on Render.

Frontend built using basic HTML + JS with:

Chat interface for message exchange

Live display of LLM replies

Toggle to review current knowledge base chunks


here is my deployed link of chatbot

https://barbeque-kb-api.onrender.com

