# Helpify AI

A simple web app where you type multiple questions at once and get AI-generated answers back — powered by Google Gemini, built with Flask, and backed by MongoDB.

---

## How It Works

1. You open the app in your browser and type your questions (one per line).
2. Flask picks them up, grabs a prompt template from MongoDB, and sends each question to Gemini AI in parallel.
3. The answers come back, get saved to the database, and show up on your screen.

---

## Tech Stack

| Technology | Why it's used |
|---|---|
| **Python** | The main language — clean syntax, great async support, huge ecosystem |
| **Flask** | Lightweight web framework, easy to set up, supports async routes out of the box |
| **Google Gemini (google-genai)** | The AI model that generates answers — fast, accurate, and has a generous free tier |
| **MongoDB Atlas** | Cloud-hosted NoSQL database — stores prompt templates and question-answer history |
| **Motor** | Async MongoDB driver for Python — lets the app talk to the database without blocking |
| **python-dotenv** | Loads secrets from the `.env` file so credentials stay out of the code |
| **TailwindCSS (CDN)** | Utility-first CSS framework used in the frontend for quick, clean styling |
| **asyncio** | Python's built-in async library — runs multiple Gemini calls in parallel instead of one by one |
---
## Project Structure

```
Api_proj/
├── app.py           — Flask server, routes, AI logic
├── init_db.py       — Seeds the database with the prompt template (run once)
├── templates/
│   └── index.html   — Frontend UI (TailwindCSS)
├── .env             — Secret keys (not committed)
├── .gitignore
└── README.md
```

---

## Setup and Run Locally

### What you'll need

- Python 3.10 or higher
- A MongoDB Atlas account (free tier is fine)
- A Google Gemini API key

### Steps

**1. Clone the repo**

```bash
git clone https://github.com/Sailee30/Intuccate_proj.git
cd Intuccate_proj
```
**2. Create a virtual environment**

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
```
**3. Install dependencies**

```bash
pip install flask motor google-genai python-dotenv
```
**4. Add your credentials**

Create a `.env` file in the project root:
```env
MONGO_URI=your_mongodb_connection_string
GEMINI_API_KEY=your_gemini_api_key
```
**5. Start the server**

```bash
python app.py
```
**6. Open** [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## API

### POST /ask-bulk

Send questions, get answers.

```json
// Request
{ "userInput": ["What is Python?", "Explain recursion"] }

// Response
{ "responses": ["Python is a ...", "Recursion is ..."] }
```

---

## Troubleshooting

| Issue | Fix |
|---|---|
| `ModuleNotFoundError` | Activate your venv and re-run `pip install` |
| MongoDB connection errors | Check your `MONGO_URI` in `.env` |
| Gemini errors | Make sure your API key is valid |
| Port 5000 in use | Kill the other process or change the port in `app.py` |

---
*Built with Flask, Google Gemini, and MongoDB Atlas.*
