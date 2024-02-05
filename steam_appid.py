import aiohttp
import asyncio
import re
import time

from Levenshtein import distance

STEAM_API_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v0002/"
STEAM_STORE_API_URL = "https://store.steampowered.com/api/appdetails?appids="

# Return a specific steam game data by appid query
async def get_app_info_by_id(app_id):
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
async def search_by_appid(app_id):
    app_info = await get_app_info_by_id(app_id)
    if app_info and app_info.get(str(app_id), {}).get("success"):
        app_data = app_info[str(app_id)].get("data")

        return {'appid': app_data["steam_appid"], 'name': app_data["name"], 'type': app_data["type"]}
    
    else: return None
    
# Remove special characters, whitespace
def normalizing(input_string):
    return re.sub(r'[^a-zA-Z0-9]', '', input_string.lower())

# Return sorted game list by ascending Levenshtein distance
def match_sort(search_query, matching_apps):

    # Calculate Levenshtein distance between user input and each result
    distances = [(name, distance(search_query, normalizing(name))) for name in matching_apps.values()]

    # Sort results by ascending Levenshtein distance
    closest_matches = sorted(distances, key=lambda x: x[1])
    
    # Extract up to 10 closest matches
    closest_matches = [match[0] for match in closest_matches[:10]]

    matches = {}
    for match in closest_matches:
        for appid, name in matching_apps.items():
            if normalizing(match) == normalizing(name):
                matches[appid] = name
    return matches

# Return games list that match string search query 
async def search_by_game_name(search_query):
    app_list = await get_app_list()
    search_query = normalizing(search_query)

    matching_apps = {}
    for app in app_list["applist"]["apps"]:
        app_name_normalized = normalizing(app["name"])
        
        if search_query in app_name_normalized:
            matching_apps[app["appid"]] = app["name"]

    # for app in app_list["applist"]["apps"]:
    #     matching_apps[app["appid"]] = app["name"]

    closest_matches = match_sort(search_query, matching_apps)

    return closest_matches 

# Return only game with "game" type by appid query
async def game_appid(search_query):
    app_data = await search_by_appid(int(search_query))

    if app_data and app_data.get("type") == "game":
        print(f'AppID: {search_query} | Name: {app_data["name"]}')
        return {"appid": app_data["appid"], "name": app_data["name"]}
    elif app_data and app_data.get("type") != "game":
        print(f'AppID: {search_query} | Name: {app_data["name"]}')
        print(f'Notice: This is not a game')
    else:
        print(f"Notice: No game found with ID {search_query}.")

# Return only games with "game" type by name query
async def game_name(search_query):
        
    matching_apps = await search_by_game_name(search_query)

    if matching_apps:

        print(f"\nMatching data for '{search_query}':")

        # creates a list of coroutine objects (tasks) using a list comprehension.
        tasks = [search_by_appid(app_id) for app_id in matching_apps.keys()]

        # fetch app information for multiple app IDs concurrently.
        app_datas = await asyncio.gather(*tasks) 
        
        base_game = False
        for app_id, app_name in matching_apps.items(): #iterates over each key-value pair in the matching_apps dictionary
            app_data = app_datas.pop(0) #removes and returns the first element from app_datas

            if app_data and app_data["type"] == "game":
                print(f"AppID: {app_id} | Name: {app_name}")
                base_game = True
            elif app_data and not base_game:
                base_game = False

        if base_game == False:
            print(f"Error: No base game retrieved")
    else:
        print(f"Error: No game found with a name containing '{search_query}'.")

# Main function
async def main():
    search_query = input(f"\nEnter the app ID or name of the app: ")
    start_time = time.time()

    if search_query.isdigit():  # Check if input is only a number
        return await game_appid(search_query)
    else:
        await game_name(search_query)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTime taken: {'{:.4f}'.format(elapsed_time)} seconds")

if __name__ == "__main__":
    # Loop main function if no return
    while True:
        result = asyncio.run(main())
        if result:
            print (f"\nExiting...")
            break
