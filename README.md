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

4. Post-Call Analysis (Added Last Midnight)

Logged each user message and bot response into a persistent format (planned CSV/JSON).

Prepared a simple /analyze endpoint to visualize or review past sessions (future enhancement).

Designed the foundation for analysis like:

Response effectiveness

FAQ coverage

Booking completion rate


This data will be used to optimize prompts, KB content, and LLM temperature settings later.



---

Deployment & UI

Hosted the project on Render.

Frontend built using basic HTML + JS with:

Chat interface for message exchange

Live display of LLM replies

Toggle to review current knowledge base chunks


here is my deployed link
https://barbeque-kb-api.onrender.com

I have also done the post call analysis using the service account and enabling the APi and tested it by entering the prompt of curl and then it uploaded in excel sheet
