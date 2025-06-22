import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "mistral-saba-24b"

def call_groq(messages):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.1
    }
    res = requests.post(GROQ_API_URL, headers=headers, json=data)
    if res.status_code != 200:
        print("ERROR RESPONSE:", res.text)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]


def choose_functions(question, function_descriptions):
    system_prompt = f"""
    You are a football data analyst who selects the best API functions(these functions get relevant) to answer a users question.
    
    Important Note:
    - Pick the best functions which can provide the best answers. 
    - Never pick more than 3 functions.

    Here are the available functions:
    {function_descriptions}

    Return a JSON array of function names exactly matching the ones above.
    Example output: ["top_gk", "league_table"]
    """
    user_question = "I am an escola fc player." + question
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question}
    ]
    return call_groq(messages)

async def answer_with_data(question, combined_data):
    today = datetime.now().strftime("%Y-%m-%d")
    system_prompt = f"""
    Today's date {today}
    You are a football data analyst who is witty and humorous. Based on the following data, answer the user's question.:
    {combined_data}

    Important Note:
    - Always assume user is an escola fc player.
    - Make the answer analytical.
    - Keep answers less than 300 words.
    - Always try to motivate escola fc players and make fun of other teams when necessary based on question.
    - Make fun of the manager of escola fc boner(@knightphoenix_97) occasionaly.
    - Never mention time in the answer even when user is asking for it.
    """
    user_question = "I am an escola fc player." + question
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question}
    ]
    return call_groq(messages)