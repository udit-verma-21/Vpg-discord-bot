import discord
import os
import asyncio
import json
from dotenv import load_dotenv
from groq_llm import choose_functions, answer_with_data
import httpx
import re
from flask import Flask
import threading
import logging

logging.basicConfig(
    level=logging.DEBUG,  # You can change to INFO to reduce noise
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is alive!", 200

def run_flask():
    app.run(host="0.0.0.0", port=10000, use_reloader = False)


load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


async def fetch_json(http_client, url):
    resp = await http_client.get(url)
    resp.raise_for_status()
    return resp.json()

processed_messages = set()
currently_processing = set()

async def leaderboard_top_gk():
    urls = [
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_gk&weekly=false&season=1&limit=30&offset=0",
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_gk&weekly=false&season=1&limit=30&offset=30"
    ]
    async with httpx.AsyncClient() as client:
        resp1 = await fetch_json(client, urls[0])
        resp2 = await fetch_json(client, urls[1])
    
    combined = resp1.get("data", []) + resp2.get("data", [])
    
    # Extract only needed fields
    filtered = []
    for player in combined:
        filtered.append({
            "username": player.get("username"),
            "user_nationality": player.get("user_nationality"),
            "team_name": player.get("team_name"),
            "points": player.get("points"),
            "saves": player.get("saves"),
            "clean_sheet": player.get("clean_sheet"),
            "save_success": player.get("save_success"),
            "matches_played": player.get("matches_played"),
        })
    
    return {"data": filtered}

async def leaderboard_top_cb():
    urls = [
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_cb&weekly=false&season=1&limit=30&offset=0",
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_cb&weekly=false&season=1&limit=30&offset=30"
    ]
    async with httpx.AsyncClient() as client:
        resp1 = await fetch_json(client, urls[0])
        resp2 = await fetch_json(client, urls[1])
    
    combined = resp1.get("data", []) + resp2.get("data", [])
    
    filtered = []
    for player in combined:
        filtered.append({
            "username": player.get("username"),
            "user_nationality": player.get("user_nationality"),
            "team_name": player.get("team_name"),
            "points": player.get("points"),
            "goals": player.get("goals"),
            "assists": player.get("assists"),
            "interceptions": player.get("interceptions"),
            "standing_tackles": player.get("standing_tackles"),
            "sliding_tackles": player.get("sliding_tackles"),
            "clean_sheet": player.get("clean_sheet"),
            "matches_played": player.get("matches_played"),
        })
    
    return {"data": filtered}

async def leaderboard_top_fb():
    urls = [
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_fb&weekly=false&season=1&limit=30&offset=0",
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_fb&weekly=false&season=1&limit=30&offset=30"
    ]
    async with httpx.AsyncClient() as client:
        resp1 = await fetch_json(client, urls[0])
        resp2 = await fetch_json(client, urls[1])

    combined = resp1.get("data", []) + resp2.get("data", [])

    filtered = []
    for player in combined:
        filtered.append({
            "username": player.get("username"),
            "user_nationality": player.get("user_nationality"),
            "team_name": player.get("team_name"),
            "points": player.get("points"),
            "goals": player.get("goals"),
            "assists": player.get("assists"),
            "interceptions": player.get("interceptions"),
            "standing_tackles": player.get("standing_tackles"),
            "sliding_tackles": player.get("sliding_tackles"),
            "clean_sheet": player.get("clean_sheet"),
            "matches_played": player.get("matches_played"),
        })

    return {"data": filtered}

async def leaderboard_top_cdm():
    urls = [
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_cdm&weekly=false&season=1&limit=30&offset=0",
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_cdm&weekly=false&season=1&limit=30&offset=30"
    ]
    async with httpx.AsyncClient() as client:
        resp1 = await fetch_json(client, urls[0])
        resp2 = await fetch_json(client, urls[1])

    combined = resp1.get("data", []) + resp2.get("data", [])

    filtered = []
    for player in combined:
        filtered.append({
            "username": player.get("username"),
            "user_nationality": player.get("user_nationality"),
            "team_name": player.get("team_name"),
            "points": player.get("points"),
            "goals": player.get("goals"),
            "assists": player.get("assists"),
            "interceptions": player.get("interceptions"),
            "standing_tackles": player.get("standing_tackles"),
            "sliding_tackles": player.get("sliding_tackles"),
            "clean_sheet": player.get("clean_sheet"),
            "matches_played": player.get("matches_played"),
        })

    return {"data": filtered}

async def leaderboard_top_cam():
    urls = [
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_cam&weekly=false&season=1&limit=30&offset=0",
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_cam&weekly=false&season=1&limit=30&offset=30"
    ]
    async with httpx.AsyncClient() as client:
        resp1 = await fetch_json(client, urls[0])
        resp2 = await fetch_json(client, urls[1])

    combined = resp1.get("data", []) + resp2.get("data", [])

    filtered = []
    for player in combined:
        filtered.append({
            "username": player.get("username"),
            "user_nationality": player.get("user_nationality"),
            "team_name": player.get("team_name"),
            "points": player.get("points"),
            "goals": player.get("goals"),
            "assists": player.get("assists"),
            "pass_accuracy": player.get("pass_accuracy"),
            "possession_won": player.get("possession_won"),
            "matches_played": player.get("matches_played"),
        })

    return {"data": filtered}

async def leaderboard_top_wingers():
    urls = [
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_wingers&weekly=false&season=1&limit=30&offset=0",
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_wingers&weekly=false&season=1&limit=30&offset=30"
    ]
    async with httpx.AsyncClient() as client:
        resp1 = await fetch_json(client, urls[0])
        resp2 = await fetch_json(client, urls[1])

    combined = resp1.get("data", []) + resp2.get("data", [])

    filtered = []
    for player in combined:
        filtered.append({
            "username": player.get("username"),
            "user_nationality": player.get("user_nationality"),
            "team_name": player.get("team_name"),
            "points": player.get("points"),
            "goals": player.get("goals"),
            "assists": player.get("assists"),
            "pass_accuracy": player.get("pass_accuracy"),
            "possession_won": player.get("possession_won"),
            "dribble_success": player.get("dribble_success"),
            "matches_played": player.get("matches_played"),
        })

    return {"data": filtered}

async def leaderboard_top_strikers():
    urls = [
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_strikers&weekly=false&season=1&limit=30&offset=0",
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_strikers&weekly=false&season=1&limit=30&offset=30"
    ]
    async with httpx.AsyncClient() as client:
        resp1 = await fetch_json(client, urls[0])
        resp2 = await fetch_json(client, urls[1])

    combined = resp1.get("data", []) + resp2.get("data", [])

    filtered = []
    for player in combined:
        filtered.append({
            "username": player.get("username"),
            "team_name": player.get("team_name"),
            "user_nationality": player.get("user_nationality"),
            "points": player.get("points"),
            "goals": player.get("goals"),
            "assists": player.get("assists"),
            "matches_played": player.get("matches_played"),
        })

    return {"data": filtered}

async def leaderboard_top_scorer():
    urls = [
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_scorer&weekly=false&season=1&limit=30&offset=0",
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_scorer&weekly=false&season=1&limit=30&offset=30"
    ]
    async with httpx.AsyncClient() as client:
        resp1 = await fetch_json(client, urls[0])
        resp2 = await fetch_json(client, urls[1])

    combined = resp1.get("data", []) + resp2.get("data", [])

    filtered = []
    for player in combined:
        filtered.append({
            "username": player.get("username"),
            "user_nationality": player.get("user_nationality"),
            "team_name": player.get("team_name"),
            "points": player.get("points"),
            "goals": player.get("goals"),
            "matches_played": player.get("matches_played"),
        })

    return {"data": filtered}

async def leaderboard_top_assist():
    urls = [
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_assist&weekly=false&season=1&limit=30&offset=0",
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=top_assist&weekly=false&season=1&limit=30&offset=30"
    ]
    async with httpx.AsyncClient() as client:
        resp1 = await fetch_json(client, urls[0])
        resp2 = await fetch_json(client, urls[1])

    combined = resp1.get("data", []) + resp2.get("data", [])

    filtered = []
    for player in combined:
        filtered.append({
            "username": player.get("username"),
            "user_nationality": player.get("user_nationality"),
            "team_name": player.get("team_name"),
            "points": player.get("points"),
            "assists": player.get("assists"),
            "matches_played": player.get("matches_played"),
        })

    return {"data": filtered}

async def leaderboard_highest_rated():
    urls = [
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=highest_rated&weekly=false&season=1&limit=30&offset=0",
        "https://api.virtualprogaming.com/public/leagues/sal/leaderboard/?leaderboard=highest_rated&weekly=false&season=1&limit=30&offset=30"
    ]
    async with httpx.AsyncClient() as client:
        resp1 = await fetch_json(client, urls[0])
        resp2 = await fetch_json(client, urls[1])

    combined = resp1.get("data", []) + resp2.get("data", [])

    filtered = []
    for player in combined:
        filtered.append({
            "username": player.get("username"),
            "user_nationality": player.get("user_nationality"),
            "team_name": player.get("team_name"),
            "points": player.get("points"),
            "matches_played": player.get("matches_played"),
        })

    return {"data": filtered}

async def league_table():
    url = "https://api.virtualprogaming.com/public/leagues/sal/table/?season=1&is_history=false"
    async with httpx.AsyncClient() as client:
        resp = await fetch_json(client, url)

    filtered = []
    for team in resp:
        filtered.append({
            "team_name": team.get("team_name"),
            "played": team.get("played"),
            "wins": team.get("wins"),
            "draws": team.get("draws"),
            "losses": team.get("losses"),
            "score_for": team.get("score_for"),
            "score_against": team.get("score_against"),
            "points": team.get("points")
        })
    return {"data": filtered}

async def get_completed_matches():
    urls = [
        "https://api.virtualprogaming.com/public/leagues/sal/matches/?status=complete&limit=30&offset=0",
        "https://api.virtualprogaming.com/public/leagues/sal/matches/?status=complete&limit=30&offset=30"
    ]
    async with httpx.AsyncClient() as client:
        resp1 = await fetch_json(client, urls[0])
        resp2 = await fetch_json(client, urls[1])

    combined = resp1.get("data", []) + resp2.get("data", [])

    filtered = []
    for match in combined:
        filtered.append({
            "datetime": match.get("datetime"),
            "home_score": match.get("home_score"),
            "away_score": match.get("away_score"),
            "home_team": match.get("home_name"),
            "away_team": match.get("away_name"),
            "match_day": match.get("match_day"),
        })

    return {"data": filtered}

async def get_scheduled_matches():
    urls = [
        "https://api.virtualprogaming.com/public/leagues/sal/matches/?status=scheduled&limit=30&offset=0",
        "https://api.virtualprogaming.com/public/leagues/sal/matches/?status=scheduled&limit=30&offset=30"
    ]
    async with httpx.AsyncClient() as client:
        resp1 = await fetch_json(client, urls[0])
        resp2 = await fetch_json(client, urls[1])

    combined = resp1.get("data", []) + resp2.get("data", [])

    filtered = []
    for match in combined:
        filtered.append({
            "datetime": match.get("datetime"),
            "home_team": match.get("home_name"),
            "away_team": match.get("away_name"),
        })

    return {"data": filtered}

async def escola_contracts():
    url = "https://api.virtualprogaming.com/public/teams/escolafc/contracts/"
    async with httpx.AsyncClient() as client:
        resp = await fetch_json(client, url)
    # return full contracts data, no filtering
    return resp

async def escola_scheduled_matches():
    url = "https://api.virtualprogaming.com/public/teams/escolafc/matches/?match_status=scheduled&limit=30&offset=0"
    async with httpx.AsyncClient() as client:
        resp = await fetch_json(client, url)

    filtered = []
    for match in resp.get("data", []):
        filtered.append({
            "datetime": match.get("datetime"),
            "home_team": match.get("home_name"),
            "away_team": match.get("away_name"),
        })
    return {"data": filtered}

async def escola_completed_matches():
    url = "https://api.virtualprogaming.com/public/teams/escolafc/matches/?match_status=complete&limit=12&offset=0"


    async with httpx.AsyncClient() as client:
        resp = await fetch_json(client, url)

    filtered = []
    for match in resp.get("data", []):
        filtered.append({
            "datetime": match.get("datetime"),
            "home_team": match.get("home_name"),
            "away_team": match.get("away_name"),
            "home_score": match.get("home_score"),
            "away_score": match.get("away_score"),
            "match_day": match.get("match_day"),
        })

    return {"data": filtered}

async def escola_highest_rated():
    url = "https://api.virtualprogaming.com/public/teams/escolafc/leaderboard/?leaderboard=highest_rated&weekly=false&season=1&limit=30&offset=0"
    async with httpx.AsyncClient() as client:
        resp = await fetch_json(client, url)
    # same fields as top scorer but without assists
    return {
        "data": [{
            "username": p.get("username"),
            "user_nationality": p.get("user_nationality"),
            "team_name": p.get("team_name"),
            "points": p.get("points"),
            "goals": p.get("goals"),
            "matches_played": p.get("matches_played"),
        } for p in resp.get("data", [])]
    }

async def escola_top_assist():
    url = "https://api.virtualprogaming.com/public/teams/escolafc/leaderboard/?leaderboard=top_assist&weekly=false&season=1&limit=30&offset=0"
    async with httpx.AsyncClient() as client:
        resp = await fetch_json(client, url)

    filtered = []
    for player in resp.get("data", []):
        filtered.append({
            "username": player.get("username"),
            "user_nationality": player.get("user_nationality"),
            "team_name": player.get("team_name"),
            "points": player.get("points"),
            "assists": player.get("assists"),
            "matches_played": player.get("matches_played"),
        })

    return {"data": filtered}

async def escola_top_scorer():
    url = "https://api.virtualprogaming.com/public/teams/escolafc/leaderboard/?leaderboard=top_scorer&weekly=false&season=1&limit=30&offset=0"
    async with httpx.AsyncClient() as client:
        resp = await fetch_json(client, url)

    filtered = []
    for player in resp.get("data", []):
        filtered.append({
            "username": player.get("username"),
            "user_nationality": player.get("user_nationality"),
            "team_name": player.get("team_name"),
            "points": player.get("points"),
            "goals": player.get("goals"),
            "matches_played": player.get("matches_played"),
        })

    return {"data": filtered}

async def escola_top_strikers():
    url = "https://api.virtualprogaming.com/public/teams/escolafc/leaderboard/?leaderboard=top_strikers&weekly=false&season=1&limit=30&offset=0"
    async with httpx.AsyncClient() as client:
        resp = await fetch_json(client, url)

    filtered = []
    for player in resp.get("data", []):
        filtered.append({
            "username": player.get("username"),
            "user_nationality": player.get("user_nationality"),
            "team_name": player.get("team_name"),
            "points": player.get("points"),
            "goals": player.get("goals"),
            "assists": player.get("assists"),
            "matches_played": player.get("matches_played"),
        })

    return {"data": filtered}

async def escola_top_wingers():
    url = "https://api.virtualprogaming.com/public/teams/escolafc/leaderboard/?leaderboard=top_wingers&weekly=false&season=1&limit=30&offset=0"
    async with httpx.AsyncClient() as client:
        resp = await fetch_json(client, url)

    filtered = []
    for player in resp.get("data", []):
        filtered.append({
            "username": player.get("username"),
            "user_nationality": player.get("user_nationality"),
            "team_name": player.get("team_name"),
            "points": player.get("points"),
            "goals": player.get("goals"),
            "assists": player.get("assists"),
            "pass_accuracy": player.get("pass_accuracy"),
            "possession_won": player.get("possession_won"),
            "dribble_success": player.get("dribble_success"),
            "matches_played": player.get("matches_played"),
        })

    return {"data": filtered}

async def escola_top_cam():
    url = "https://api.virtualprogaming.com/public/teams/escolafc/leaderboard/?leaderboard=top_cam&weekly=false&season=1&limit=30&offset=0"
    async with httpx.AsyncClient() as client:
        resp = await fetch_json(client, url)
    return {
        "data": [{
            "username": p.get("username"),
            "user_nationality": p.get("user_nationality"),
            "team_name": p.get("team_name"),
            "points": p.get("points"),
            "goals": p.get("goals"),
            "assists": p.get("assists"),
            "pass_accuracy": p.get("pass_accuracy"),
            "possession_won": p.get("possession_won"),
            "matches_played": p.get("matches_played"),
        } for p in resp.get("data", [])]
    }

async def escola_top_cdm():
    url = "https://api.virtualprogaming.com/public/teams/escolafc/leaderboard/?leaderboard=top_cdm&weekly=false&season=1&limit=30&offset=0"
    async with httpx.AsyncClient() as client:
        resp = await fetch_json(client, url)
    return {
        "data": [{
            "username": p.get("username"),
            "user_nationality": p.get("user_nationality"),
            "team_name": p.get("team_name"),
            "points": p.get("points"),
            "goals": p.get("goals"),
            "assists": p.get("assists"),
            "interceptions": p.get("interceptions"),
            "standing_tackles": p.get("standing_tackles"),
            "sliding_tackles": p.get("sliding_tackles"),
            "clean_sheet": p.get("clean_sheet"),
            "matches_played": p.get("matches_played"),
        } for p in resp.get("data", [])]
    }

async def escola_top_fb():
    url = "https://api.virtualprogaming.com/public/teams/escolafc/leaderboard/?leaderboard=top_fb&weekly=false&season=1&limit=30&offset=0"
    async with httpx.AsyncClient() as client:
        resp = await fetch_json(client, url)
    return {
        "data": [{
            "username": p.get("username"),
            "user_nationality": p.get("user_nationality"),
            "team_name": p.get("team_name"),
            "points": p.get("points"),
            "goals": p.get("goals"),
            "assists": p.get("assists"),
            "interceptions": p.get("interceptions"),
            "standing_tackles": p.get("standing_tackles"),
            "sliding_tackles": p.get("sliding_tackles"),
            "clean_sheet": p.get("clean_sheet"),
            "matches_played": p.get("matches_played"),
        } for p in resp.get("data", [])]
    }

async def escola_top_cb():
    url = "https://api.virtualprogaming.com/public/teams/escolafc/leaderboard/?leaderboard=top_cb&weekly=false&season=1&limit=30&offset=0"
    async with httpx.AsyncClient() as client:
        resp = await fetch_json(client, url)
    return {
        "data": [{
            "username": p.get("username"),
            "user_nationality": p.get("user_nationality"),
            "team_name": p.get("team_name"),
            "points": p.get("points"),
            "goals": p.get("goals"),
            "assists": p.get("assists"),
            "interceptions": p.get("interceptions"),
            "standing_tackles": p.get("standing_tackles"),
            "sliding_tackles": p.get("sliding_tackles"),
            "clean_sheet": p.get("clean_sheet"),
            "matches_played": p.get("matches_played"),
        } for p in resp.get("data", [])]
    }

async def escola_top_gk():
    url = "https://api.virtualprogaming.com/public/teams/escolafc/leaderboard/?leaderboard=top_gk&weekly=false&season=1&limit=30&offset=0"
    async with httpx.AsyncClient() as client:
        resp = await fetch_json(client, url)

    filtered = []
    for player in resp.get("data", []):
        filtered.append({
            "username": player.get("username"),
            "user_nationality": player.get("user_nationality"),
            "team_name": player.get("team_name"),
            "points": player.get("points"),
            "saves": player.get("saves"),
            "clean_sheet": player.get("clean_sheet"),
            "save_success": player.get("save_success"),
            "matches_played": player.get("matches_played"),
        })

    return {"data": filtered}




FUNCTION_DESCRIPTIONS = {
    "leaderboard_top_gk": "Get top goalkeepers leaderboard with stats: username, nationality, team name, points, saves, clean sheets, save success, matches played.",
    "leaderboard_top_cb": "Get top center backs leaderboard with stats: username, nationality, team name, points, goals, assists, interceptions, standing tackles, sliding tackles, clean sheets, matches played.",
    "leaderboard_top_fb": "Get top fullbacks leaderboard with stats: username, nationality, team name, points, goals, assists, interceptions, standing tackles, sliding tackles, clean sheets, matches played.",
    "leaderboard_top_cdm": "Get top defensive midfielders leaderboard with stats: username, nationality, team name, points, goals, assists, interceptions, standing tackles, sliding tackles, clean sheets, matches played.",
    "leaderboard_top_cam": "Get top attacking midfielders leaderboard with stats: username, nationality, team name, points, goals, assists, pass accuracy, possession won, matches played.",
    "leaderboard_top_wingers": "Get top wingers leaderboard with stats: username, nationality, team name, points, goals, assists, pass accuracy, possession won, dribble success, matches played.",
    "leaderboard_top_strikers": "Get top strikers leaderboard with stats: username, nationality, team name, points, goals, assists, matches played.",
    "leaderboard_top_scorer": "Get top scorers leaderboard with stats: username, nationality, team name, points, goals, matches played.",
    "leaderboard_top_assist": "Get top assists leaderboard with stats: username, nationality, team name, points, assists, matches played.",
    "leaderboard_highest_rated": "Get highest rated players leaderboard with stats: username, nationality, team name, points, matches played.",

    "league_table": "Get the current league table standings for the season.",

    "get_completed_matches": "Get completed matches with details: datetime, home team, away team, home score, away score, match day.",
    "get_scheduled_matches": "Get scheduled matches with details: datetime, home team, away team.",

    "escola_contracts": "Get full list of Escola FC player contracts, no filtering applied.",

    "escola_scheduled_matches": "Get Escola FC scheduled matches with datetime, home team, and away team.",
    "escola_completed_matches": "Get Escola FC completed matches with datetime, home team, away team, home score, away score, and match day.",

    "escola_highest_rated": "Get Escola FC highest rated players leaderboard with username, nationality, team name, points, goals, matches played.",

    "escola_top_assist": "Get Escola FC top assists leaderboard with username, nationality, team name, points, assists, matches played.",
    "escola_top_scorer": "Get Escola FC top scorers leaderboard with username, nationality, team name, points, goals, matches played.",
    "escola_top_strikers": "Get Escola FC top strikers leaderboard with username, nationality, team name, points, goals, assists, matches played.",
    "escola_top_wingers": "Get Escola FC top wingers leaderboard with username, nationality, team name, points, goals, assists, pass accuracy, possession won, dribble success, matches played.",
    "escola_top_cam": "Get Escola FC top attacking midfielders leaderboard with username, nationality, team name, points, goals, assists, pass accuracy, possession won, matches played.",
    "escola_top_cdm": "Get Escola FC top defensive midfielders leaderboard with username, nationality, team name, points, goals, assists, interceptions, standing tackles, sliding tackles, clean sheets, matches played.",
    "escola_top_fb": "Get Escola FC top fullbacks leaderboard with username, nationality, team name, points, goals, assists, interceptions, standing tackles, sliding tackles, clean sheets, matches played.",
    "escola_top_cb": "Get Escola FC top center backs leaderboard with username, nationality, team name, points, goals, assists, interceptions, standing tackles, sliding tackles, clean sheets, matches played.",
    "escola_top_gk": "Get Escola FC top goalkeepers leaderboard with username, nationality, team name, points, saves, clean sheets, save success, matches played.",
}
FUNCTIONS = {
    "leaderboard_top_gk": {
        "func": leaderboard_top_gk,
        "description": FUNCTION_DESCRIPTIONS["leaderboard_top_gk"],
    },
    "leaderboard_top_cb": {
        "func": leaderboard_top_cb,
        "description": FUNCTION_DESCRIPTIONS["leaderboard_top_cb"],
    },
    "leaderboard_top_fb": {
        "func": leaderboard_top_fb,
        "description": FUNCTION_DESCRIPTIONS["leaderboard_top_fb"],
    },
    "leaderboard_top_cdm": {
        "func": leaderboard_top_cdm,
        "description": FUNCTION_DESCRIPTIONS["leaderboard_top_cdm"],
    },
    "leaderboard_top_cam": {
        "func": leaderboard_top_cam,
        "description": FUNCTION_DESCRIPTIONS["leaderboard_top_cam"],
    },
    "leaderboard_top_wingers": {
        "func": leaderboard_top_wingers,
        "description": FUNCTION_DESCRIPTIONS["leaderboard_top_wingers"],
    },
    "leaderboard_top_strikers": {
        "func": leaderboard_top_strikers,
        "description": FUNCTION_DESCRIPTIONS["leaderboard_top_strikers"],
    },
    "leaderboard_top_scorer": {
        "func": leaderboard_top_scorer,
        "description": FUNCTION_DESCRIPTIONS["leaderboard_top_scorer"],
    },
    "leaderboard_top_assist": {
        "func": leaderboard_top_assist,
        "description": FUNCTION_DESCRIPTIONS["leaderboard_top_assist"],
    },
    "leaderboard_highest_rated": {
        "func": leaderboard_highest_rated,
        "description": FUNCTION_DESCRIPTIONS["leaderboard_highest_rated"],
    },
    "league_table": {
        "func": league_table,
        "description": FUNCTION_DESCRIPTIONS["league_table"],
    },
    "get_completed_matches": {
        "func": get_completed_matches,
        "description": FUNCTION_DESCRIPTIONS["get_completed_matches"],
    },
    "get_scheduled_matches": {
        "func": get_scheduled_matches,
        "description": FUNCTION_DESCRIPTIONS["get_scheduled_matches"],
    },
    "escola_contracts": {
        "func": escola_contracts,
        "description": FUNCTION_DESCRIPTIONS["escola_contracts"],
    },
    "escola_scheduled_matches": {
        "func": escola_scheduled_matches,
        "description": FUNCTION_DESCRIPTIONS["escola_scheduled_matches"],
    },
    "escola_completed_matches": {
        "func": escola_completed_matches,
        "description": FUNCTION_DESCRIPTIONS["escola_completed_matches"],
    },
    "escola_highest_rated": {
        "func": escola_highest_rated,
        "description": FUNCTION_DESCRIPTIONS["escola_highest_rated"],
    },
    "escola_top_assist": {
        "func": escola_top_assist,
        "description": FUNCTION_DESCRIPTIONS["escola_top_assist"],
    },
    "escola_top_scorer": {
        "func": escola_top_scorer,
        "description": FUNCTION_DESCRIPTIONS["escola_top_scorer"],
    },
    "escola_top_strikers": {
        "func": escola_top_strikers,
        "description": FUNCTION_DESCRIPTIONS["escola_top_strikers"],
    },
    "escola_top_wingers": {
        "func": escola_top_wingers,
        "description": FUNCTION_DESCRIPTIONS["escola_top_wingers"],
    },
    "escola_top_cam": {
        "func": escola_top_cam,
        "description": FUNCTION_DESCRIPTIONS["escola_top_cam"],
    },
    "escola_top_cdm": {
        "func": escola_top_cdm,
        "description": FUNCTION_DESCRIPTIONS["escola_top_cdm"],
    },
    "escola_top_fb": {
        "func": escola_top_fb,
        "description": FUNCTION_DESCRIPTIONS["escola_top_fb"],
    },
    "escola_top_cb": {
        "func": escola_top_cb,
        "description": FUNCTION_DESCRIPTIONS["escola_top_cb"],
    },
    "escola_top_gk": {
        "func": escola_top_gk,
        "description": FUNCTION_DESCRIPTIONS["escola_top_gk"],
    },
}
def safe_extract_functions(raw_response):
    try:
        data = json.loads(raw_response)
        if isinstance(data, list):
            return [fn for fn in data if fn in FUNCTIONS]
    except Exception:
        pass
    return [fn for fn in re.findall(r'"([a-zA-Z0-9_]+)"', raw_response) if fn in FUNCTIONS]



def build_function_descriptions():
    return "\n".join([f"{name}: {info['description']}" for name, info in FUNCTIONS.items()])

@client.event
async def on_ready():
    logger.info(f"Bot is online as {client.user}")
    processed_messages.clear()
    currently_processing.clear()
    print(f"[DEBUG] Cleared message processing caches on startup")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.id in processed_messages or message.id in currently_processing:
        logger.debug(f"Skipping message {message.id} - already processed/processing")

        return

    if not (client.user in message.mentions):
        return
    logger.info(f"Processing message {message.id}: {message.content}")

    currently_processing.add(message.id)


    try:
        user_question = message.content.replace(f'<@!{client.user.id}>', '').strip()

        function_desc = build_function_descriptions()
        try:
            funcs_text = choose_functions(user_question, function_desc)
        except Exception as e:
            await message.channel.send(f"Error selecting functions: {e}")
            return

        function_names = safe_extract_functions(funcs_text)
        if not function_names:
            await message.channel.send("Couldn't find matching data sources to answer your question.")
            return
        tasks = []
        for fn in function_names:
            func = FUNCTIONS[fn]["func"]
            tasks.append(func())
        results = await asyncio.gather(*tasks)
        # Step 3: Combine data
        combined_data = ""
        for fn, data in zip(function_names, results):
            combined_data += f"=== Data from {fn} ===\n{json.dumps(data, indent=2)}\n\n"
        combined_data=combined_data[:10000]  
        # Step 4: Ask Groq for final answer
        try:
            answer = await answer_with_data(user_question, combined_data)
        except Exception as e:
            await message.channel.send("Stop asking so many questions. Let me breathe for a moment.")
            return
        await message.channel.send(answer[:2000])
    
    except Exception as e:
        print(f"[ERROR] Unexpected error processing message {message.id}: {e}")
        await message.channel.send("Sorry, something went wrong processing your request.")
    
    finally:
        # Always move from currently_processing to processed, regardless of success/failure
        logger.debug(f"Finished processing message {message.id}")

        currently_processing.discard(message.id)
        processed_messages.add(message.id)
        
        # Clean up old message IDs (keep only last 50 to prevent memory leak)
        if len(processed_messages) > 50:
            old_messages = list(processed_messages)[:25]
            for old_id in old_messages:
                processed_messages.discard(old_id)
        
        print(f"[DEBUG] Finished processing message {message.id}")

if __name__ == "__main__":
    logger.info("Launching bot and Flask server")
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    client.run(DISCORD_BOT_TOKEN)

