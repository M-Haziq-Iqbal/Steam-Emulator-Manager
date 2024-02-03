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
        return {'name': app_data["name"], 'type': app_data["type"]}
    else: return None

async def search_by_game_name(name): #"https://api.steampowered.com/ISteamApps/GetAppList/v0002/"
    app_list = await get_app_list()
    name_normalized = re.sub(r'[^a-zA-Z0-9]', '', name.lower())
    matching_apps = {}
    for app in app_list["applist"]["apps"]:
        app_name_normalized = re.sub(r'[^a-zA-Z0-9]', '', app["name"].lower())
        if name_normalized in app_name_normalized:
            matching_apps[app["appid"]] = app["name"]
            # matching_apps["appid"] = app["appid"]
    return matching_apps


async def main():
    steam_game = {}
    while True:
        search_query = input("Enter the app ID or name of the app: ")
        if search_query.isdigit():  # Check if input is only a number
            app_info = await search_by_appid(int(search_query))
            if app_info and app_info.get("type") == "game":
                steam_game = {"appid": search_query, "name": app_info["name"]}
                print(f'Game Name: {app_info["name"]}')
            elif app_info and app_info.get("type") != "game":
                print(f'Notice: {app_info["name"]} is not the base game')
            else:
                print(f"Notice: No game found with ID {search_query}.")
        else:
            matching_apps = await search_by_game_name(search_query)

            if matching_apps and len(matching_apps) > 10:
                print(f"\nMatching data for '{search_query}' exceeds 10 games. Please enter more specific keywords: ")
            
            elif matching_apps:
                print(f"\nMatching data for '{search_query}':")
                tasks = [search_by_appid(app_id) for app_id in matching_apps.keys()] # creates a list of coroutine objects (tasks) using a list comprehension.
                app_infos = await asyncio.gather(*tasks) # fetch app information for multiple app IDs concurrently.
                
                for app_id, app_name in matching_apps.items():
                    app_info = app_infos.pop(0)
                    if app_info and app_info["type"] == "game":
                        print(f"AppID: {app_id}, Name: {app_name}")
                
                # search again game data through appid
                search_query = input("Enter the app ID of the app: ")
                
                if search_query.isdigit():  # Check if input is only a number
                    app_info = await search_by_appid(int(search_query))
                    if app_info and app_info.get("type") == "game":
                        steam_game = {"appid": search_query, "name": app_info["name"]}
                        print(f'Game Name: {app_info["name"]}')
                    elif app_info and app_info.get("type") != "game":
                        print(f'Notice: {app_info["name"]} is not the base game')
                    else:
                        print(f"Notice: No game found with ID {search_query}.")
                else: print(f"{search_query} is not a valid AppID")

            else:
                print(f"Notice: No apps found with a name containing '{search_query}'.")
        
        if steam_game:
            break # Exit the loop
        else: 
            print("Restarting the script...")
            continue # Restart the loop

    

if __name__ == "__main__":
    asyncio.run(main())
