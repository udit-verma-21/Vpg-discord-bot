import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"
# GROQ_API_URL = "https://api.together.xyz/v1/chat/completions"
# GROQ_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
# TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")


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
    - Never pick more than 6 functions.

    Escola squad information: 
    1. Flamenco - Main keeper with lots of saves. Has played for indian national team as keeper in fc 25.
    2. Cermatic_sweater - Backup keeper who is learning quick.
    3. bhoglubhai - Amazing bangladeshi fullback who can also play centre back. Runs bhoglu striker academy which is big scam. Claims that godmod is from his academy.
    4. cech_mate33 - Mumbaikar who plays centre back.
    5. Danny - Dannnny1003 - danish bhai plays Centre back. Also no one can speak in front of danish bhai.
    6. Aronno29 - also known as plastic - Very good centre back. Loves getting red cards.
    7. KaranPrakash - Another solid centre back. Also a great lawyer off the field.
    8. noolster18 - Also known as coolster for his tricks on the pitch. Plays mostly as CAM. 
    9. anrf77 - The oldest player in the squad. Plays multiple positions in midfield (CM, CDM, CAM). Always on vacation in goa.
    10. Gamerdude2418 - plays as leftback mostly or CDM.
    11. awesome- awesome player as name suggests. anrf claims that awesome is his best friend.
    12. anilca7 - Plays cdm. Always wants to rotate the ball. looks like ozil.
    12. shaggytarius - manager of escola. plays rw mostly. has played cdm and st as well. he is godmod's older brother. great 3d designer as well.
    13. godmod - plays st or winger. younger brother of shaggytarius. known for his free kicks. 
    14. knight_phoneix97- also known as boner. manager of escola. plays as st or winger. always keeps saying that press higher.

    Here are the available functions:
    {function_descriptions}

    Return a JSON array of function names exactly matching the ones above. If you dont find any relevant function, just return league table function.
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


    Escola squad information: 
    1. Flamenco - Main keeper with lots of saves. Has played for indian national team as keeper in fc 25.
    2. Cermatic_sweater - Backup keeper who is learning quick.
    3. bhoglubhai - Amazing bangladeshi fullback who can also play centre back. Runs bhoglu striker academy which is big scam. Claims that godmod is from his academy.
    4. cech_mate33 - Mumbaikar who plays centre back.
    5. Danny - Dannnny1003 - danish bhai plays Centre back. Also no one can speak in front of danish bhai.
    6. Aronno29 - also known as plastic - Very good centre back. Loves getting red cards.
    7. KaranPrakash - Another solid centre back. Also a great lawyer off the field.
    8. noolster18 - Also known as coolster for his tricks on the pitch. Plays mostly as CAM. 
    9. anrf77 - The oldest player in the squad. Plays multiple positions in midfield (CM, CDM, CAM). Always on vacation in goa.
    10. Gamerdude2418 - plays as leftback mostly or CDM.
    11. awesome- awesome player as name suggests. anrf claims that awesome is his best friend.
    12. anilca7 - Plays cdm. Always wants to rotate the ball. looks like ozil.
    12. shaggytarius - manager of escola. plays rw mostly. has played cdm and st as well. he is godmod's older brother. great 3d designer as well.
    13. godmod - plays st or winger. younger brother of shaggytarius. known for his free kicks. 
    14. knight_phoneix97- also known as boner. manager of escola. plays as st or winger. always keeps saying that press higher.

    """
    user_question = "I am an escola fc player." + question
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question}
    ]
    return call_groq(messages)

