import aiohttp
import asyncio
import re
from Levenshtein import distance

async def get_app_info_by_id(app_id):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://store.steampowered.com/api/appdetails?appids={app_id}") as response:
                response.raise_for_status()  # Raise an error if the response status code is not in the 2xx range
                return await response.json()
    except aiohttp.ClientError as e:
        print(f"An error occurred: {e}")
        return None

async def get_app_list():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.steampowered.com/ISteamApps/GetAppList/v0002/") as response:
                response.raise_for_status()  # Raise an error if the response status code is not in the 2xx range
                return await response.json()
    except aiohttp.ClientError as e:
        print(f"An error occurred: {e}")
        return None

# return {appid:appid, name:name, type:type}
async def search_by_appid(app_id):
    #"https://store.steampowered.com/api/appdetails?appids={app_id}"
    app_info = await get_app_info_by_id(app_id)
    if app_info and app_info.get(str(app_id), {}).get("success"):
        app_data = app_info[str(app_id)].get("data")
        return {'appid': app_data["steam_appid"], 'name': app_data["name"], 'type': app_data["type"]}
    else: return None

def normalizing(input_string):
    return re.sub(r'[^a-zA-Z0-9]', '', input_string.lower())

# Sort dictionaries of game names by ascending Levenshtein distance
def match_sort(search_query, matching_apps):

    # Calculate Levenshtein distance between user input and each result
    distances = [(apps["name"], distance(normalizing(search_query), normalizing(apps["name"]))) for apps in matching_apps]

    # Sort results by ascending Levenshtein distance
    closest_matches = sorted(distances, key=lambda x: x[1])
    
    # Extract up to 10 closest matches
    closest_matches = [match[0] for match in closest_matches[:10]]

    return closest_matches

# Return {appid:appid, name:name}
async def search_by_game_name(search_query): #"https://api.steampowered.com/ISteamApps/GetAppList/v0002/"
    app_list = await get_app_list()
    query_normalized = normalizing(search_query)

    matching_apps = []
    # matching_apps = {}
    for app in app_list["applist"]["apps"]:
        app_name_normalized = normalizing(app["name"])
        
        if query_normalized in app_name_normalized:
            matching_apps.append({"appid": app["appid"], "name": app["name"]})
            # matching_apps[app["appid"]] = app["name"]

    closest_matches = match_sort(search_query, matching_apps)

    matches = {}

    for name in closest_matches:
        for apps in matching_apps:
            if normalizing(name) == normalizing(apps["name"]):
                matches[apps["appid"]] = apps["name"]

    return matches

async def compare_appid(search_query):
    app_data = await search_by_appid(int(search_query))

    if app_data and app_data.get("type") == "game":
        print(f'AppID: {search_query} | Name: {app_data["name"]}')
        return {"appid": app_data["appid"], "name": app_data["name"], "type": app_data["type"]}
    elif app_data and app_data.get("type") != "game":
        print(f'AppID: {search_query} | Name: {app_data["name"]}')
        print(f'Notice: This is not a game')
    else:
        print(f"Notice: No game found with ID {search_query}.")

async def compare_game_name(search_query):
        
    matching_apps = await search_by_game_name(search_query)

    if matching_apps:

        print(f"Matching data for '{search_query}':")

        # creates a list of coroutine objects (tasks) using a list comprehension.
        # tasks = [search_by_appid(apps["appid"]) for apps in matching_apps]
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

async def main():
    search_query = input(f"\nEnter the app ID or name of the app: ")

    if search_query.isdigit():  # Check if input is only a number
        await compare_appid(search_query)
    else:
        await compare_game_name(search_query)

if __name__ == "__main__":
    while True:
        result = asyncio.run(main())
        if result:
            print (f"Exiting...")
            break
