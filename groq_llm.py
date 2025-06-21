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
        "temperature": 0.4
    }
    res = requests.post(GROQ_API_URL, headers=headers, json=data)
    if res.status_code != 200:
        print("ERROR RESPONSE:", res.text)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]


def choose_functions(question, function_descriptions):
    prompt = f"""
    You are a football data analyst who selects the best API functions to answer a football-related question.
    Pick the best functions which can provide the best answers.
    You can choose minimum 3 functions which are suitable to answer a question asked by user. 
    Always assume that the user plays for escola fc.
    Example on how to choose:
    If a person is asking analysis for other teams, you need to pick functions to get there league standings, pick functions to find out there best players in various positions etc.
    If a person is asking for a comparison of escola player with other players, then for the person's position pick players from leaderboard in same position and compare him in the league.
    Here are the available functions:
    {function_descriptions}

    Given the question:
    {question}

    Return a JSON array of function names exactly matching the ones above.
    Example output: ["top_gk", "league_table"]
    """
    messages = [
        {"role": "system", "content": "You are a function selector that picks API functions."},
        {"role": "user", "content": prompt}
    ]
    return call_groq(messages)

async def answer_with_data(question, combined_data):
    today = datetime.now().strftime("%Y-%m-%d")
    prompt = f"""
    Today's date {today}
    You are a football data analyst. Based on the following data:
    {combined_data}

    Answer the user's question:
    {question}

    Important Note:
    Always assume user is an escola fc player.
    You always respond like a famous movie star of your choice both from bollywood and hollywood.
    Do not mention which star you are acting as.
    Make the answer analytical first and funny second . You can make fun wherever its okay without crossing a line. For questions you dont have answer to respond with you need to ask Boner @knightphoneix_97 for this.
    Make sure your answer doesnt exceed 1500 characters.
    Always try to motivate escola fc players and make fun of other teams.
    Make fun of the manager of escola fc boner(@knightphoenix_97) occasionaly.
    Never mention time in the answer even when user is asking for it.
    """
    messages = [
        {"role": "system", "content": "You answer questions based on provided data."},
        {"role": "user", "content": prompt}
    ]
    return call_groq(messages)