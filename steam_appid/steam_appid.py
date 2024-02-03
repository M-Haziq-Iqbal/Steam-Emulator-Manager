import aiohttp
import asyncio
import re

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

async def search_by_appid(app_id): #"https://store.steampowered.com/api/appdetails?appids={app_id}"
    app_info = await get_app_info_by_id(app_id)
    if app_info and app_info.get(str(app_id), {}).get("success"):
        app_data = app_info[str(app_id)].get("data")
        return {'appid': app_data["steam_appid"], 'name': app_data["name"], 'type': app_data["type"]}
    else: return None

async def search_by_game_name(game_name): #"https://api.steampowered.com/ISteamApps/GetAppList/v0002/"
    app_list = await get_app_list()
    name_normalized = re.sub(r'[^a-zA-Z0-9]', '', game_name.lower())
    matching_apps = {}
    for app in app_list["applist"]["apps"]:
        app_name_normalized = re.sub(r'[^a-zA-Z0-9]', '', app["name"].lower())
        if name_normalized in app_name_normalized:
            matching_apps[app["appid"]] = app["name"]
    return matching_apps

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

    if matching_apps and len(matching_apps) > 10:
        print(f"Matching data for '{search_query}' exceeds 10 games. Please enter more specific keywords. ")
    elif matching_apps:
        print(f"Matching data for '{search_query}':")
        tasks = [search_by_appid(app_id) for app_id in matching_apps.keys()] # creates a list of coroutine objects (tasks) using a list comprehension.
        app_datas = await asyncio.gather(*tasks) # fetch app information for multiple app IDs concurrently.
        
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
