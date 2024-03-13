import aiohttp
import asyncio
import re
import time
import logging

from tool import confirmation,  timer, terminal_divider, test

from Levenshtein import distance

STEAM_API_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v0002/"
STEAM_STORE_API_URL = "https://store.steampowered.com/api/appdetails?appids="
STEAM_REVIEW_API_URL = "https://store.steampowered.com/appreviews/{app_id}?json=1"

logging.basicConfig(level=logging.DEBUG, format='- %(levelname)s - %(message)s')

# Return a specific steam game data by appid query
async def get_app_info_by_id(app_id: int):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{STEAM_STORE_API_URL}{app_id}") as response:
                response.raise_for_status()  # Raise an error if the response status code is not in the 2xx range
                return await response.json()
    except aiohttp.ClientError as e:
        print(f"An error occurred: {e}")
        return None

# Return the whole steam game database by name query
async def get_app_list():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{STEAM_API_URL}") as response:
                response.raise_for_status()  # Raise an error if the response status code is not in the 2xx range
                return await response.json()
    except aiohttp.ClientError as e:
        print(f"An error occurred: {e}")
        return None

# Return filtered steam game data by appid query
async def search_by_appid(app_id: int):
    app_info = await get_app_info_by_id(app_id)
    if app_info and app_info.get(str(app_id), {}).get("success"):
        app_data = app_info[str(app_id)].get("data")

        return {
            'appid': app_data["steam_appid"], 
            'name': app_data["name"], 
            'type': app_data["type"]
        }
    
    else: return None
    
# Remove special characters, whitespace
def normalizing(input_string: str):
    return re.sub(r'[^a-zA-Z0-9]', '', input_string.lower())

# Return sorted game list by ascending Levenshtein distance
def match_sort(search_query: str, matching_apps:dict):

    # Calculate Levenshtein distance between user input and each result
    distances = [(name, distance(search_query, normalizing(name))) for name in matching_apps.values()]

    # Sort results by ascending Levenshtein distance
    closest_matches = sorted(distances, key=lambda x: x[1])
    
    # Extract up to 10 names of closest matches
    closest_matches = [match[0] for match in closest_matches[:10]]

    matches = {}
    for match in closest_matches:
        for appid, name in matching_apps.items():
            if normalizing(match) == normalizing(name):
                matches[appid] = name
    return matches

# Return games list that match string search query 
async def search_by_game_name(search_query: str):
    app_list = await get_app_list()
    search_query = normalizing(search_query)

    matching_apps = {}
    for app in app_list["applist"]["apps"]:
        app_name_normalized = normalizing(app["name"])
        
        if search_query in app_name_normalized: ####Control Ultimate Edition cant be found if query is only "control"
            matching_apps[app["appid"]] = app["name"]

    if not matching_apps:
        print(f"Notice: No exact match found, will retrieve similar match instead")
        for app in app_list["applist"]["apps"]:
            matching_apps[app["appid"]] = app["name"]

    closest_matches = match_sort(search_query, matching_apps)

    return closest_matches

# Return only game with "game" type by appid query
async def game_appid(search_query: int):
    app_data = await search_by_appid(int(search_query))

    if app_data and app_data.get("type") == "game":
        print(f"\n{'AppID' : <10}{'Name' : <10}")
        print(f"{search_query : <10}{app_data['name']: <10}")
        return app_data["appid"]
    elif app_data and app_data.get("type") != "game":
        print(f"\n{'AppID' : <10}{'Name' : <10}")
        print(f"{search_query : <10}{app_data['name']: <10}")
        logging.warning(f"{app_data['name']} is not a base game")
        
        return None
    else:
        logging.warning(f"No game found with ID {search_query}.")
        
        return None

# Return only games with "game" type by name query
async def game_name(search_query: str):
        
    matching_apps = await search_by_game_name(search_query)
    
    print(f"\nMatching data for '{search_query}':")
    
    # creates a list of coroutine objects (tasks) using a list comprehension.
    tasks = [search_by_appid(app_id) for app_id in matching_apps.keys()]

    # fetch app information for multiple app IDs concurrently.
    app_datas = await asyncio.gather(*tasks)
            
    # create list only with game type
    base_game = [app_data for app_data in app_datas if app_data and app_data["type"] == "game"]
    
    if not base_game:
        logging.error(f"No base game retrieved")
        return None
    
    if base_game:
        print(f"\n{'AppID' : <10}{'Name' : <10}")
        for game in base_game:
            print(f"{game['appid'] : <10}{game['name']: <10}")
        print()
        return base_game

# Main function
@terminal_divider
def main():
    
    while True:
        search_query = input(f"Enter the app ID or name of the app: ")
        
        if not normalizing(search_query):
            logging.error(f"Only non-alphanumeric characters detected!\n")
            continue

        if search_query.isdigit():
            appid = asyncio.run(game_appid(search_query))
            if appid and confirmation("Are you sure this is the correct game? (y/n)\t"):
                return appid
            print()
        else:
            asyncio.run(game_name(search_query))

if __name__ == "__main__":
    main()
