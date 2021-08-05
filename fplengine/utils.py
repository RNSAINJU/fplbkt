from fplengine.models import Gameweek
import aiohttp
import asyncio
from fpl import FPL


# client = aiohttp.ClientSession

async def get_all_fixtures():
    results = []
    async with aiohttp.ClientSession() as session:
        
        fpl = FPL(session)
        fixtures_data = await fpl.get_fixtures(return_json=True)
        for data in fixtures_data:
            home_team = await fpl.get_team(data.get('team_h'),return_json=True)
            away_team = await fpl.get_team(data.get('team_a'),return_json=True)
            fixtures ={
                "code":data.get('code'),
                "home_team":home_team["name"],
                "home_team_score":data.get('team_h_score'),
                "away_team":away_team["name"],
                "away_team_score":data.get('team_a_score'),
                "event":data.get("event"),
            }
            # print(fixtures)
            results.append(fixtures)
            # print(results)
            
        
        return list(results)


def get_latest_gameweek():
    latest_gameweek = Gameweek.objects.all().order_by('-no').first()
    return latest_gameweek.no

