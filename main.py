from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
HF_API_KEY = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mixtral-8x7b-instruct-v0.1"  # Free model
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

class Query(BaseModel):
    text: str

def get_obd_data(code):
    conn = sqlite3.connect("obd_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM obd_codes WHERE code = ?", (code,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "Code not found"

def log_query(query, response):
    conn = sqlite3.connect("obd_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO query_history (user_query, response) VALUES (?, ?)", (query, response))
    conn.commit()
    conn.close()

@app.post("/diagnose")
async def diagnose(query: Query):
    # Extract OBD code (e.g., "P0420") from query
    words = query.text.split()
    obd_code = next((word for word in words if word.startswith("P") and len(word) == 5), None)
    if obd_code:
        obd_info = get_obd_data(obd_code)
        prompt = f"Act as a vehicle support assistant. Given OBD code {obd_code}: {obd_info}, explain the issue in simple terms."
    else:
        prompt = f"Act as a vehicle support assistant. Explain: {query.text}"

    # Call Hugging Face API
    payload = {"inputs": prompt, "parameters": {"max_length": 200}}
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()[0]["generated_text"] if response.ok else "Error querying LLM"

    # Log query and response
    log_query(query.text, result)
    return {"diagnosis": result}