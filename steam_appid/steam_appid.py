import aiohttp
import asyncio
import re

async def get_app_info_by_id(app_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://store.steampowered.com/api/appdetails?appids={app_id}") as response:
            return await response.json()

async def get_app_list():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.steampowered.com/ISteamApps/GetAppList/v0002/") as response:
            return await response.json()

async def search_by_appid(app_id): #"https://store.steampowered.com/api/appdetails?appids={app_id}"
    app_info = await get_app_info_by_id(app_id)
    if app_info.get(str(app_id), {}).get("success"):
        app_data = app_info[str(app_id)]["data"]
        return {'name': app_data["name"], 'type': app_data["type"]}
    else:
        return None

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
    search_query = input("Enter the app ID or name of the app: ")
    if search_query.isdigit():  # Check if input is only a number
        app_info = await search_by_appid(int(search_query))
        if app_info and app_info["type"] == "game":
            print(f'Game Name: {app_info["name"]}')
        elif app_info and app_info.get("type") != "game":
            print(f'Notice: {app_info["name"]} is not the base game')
        else:
            print(f"Notice: No game found with ID {search_query}.")
    else:
        matching_apps = await search_by_game_name(search_query)
        if matching_apps:
            print(f"Matching App IDs for '{search_query}': ")
            tasks = [search_by_appid(app_id) for app_id in matching_apps.keys()] # creates a list of coroutine objects (tasks) using a list comprehension.
            app_infos = await asyncio.gather(*tasks) # fetch app information for multiple app IDs concurrently.
            for app_id, app_name in matching_apps.items():
                app_info = app_infos.pop(0)
                if app_info and app_info["type"] == "game":
                    print(f"{app_id}: {app_name}")
        else:
            print(f"Notice: No apps found with a name containing '{search_query}'.")

if __name__ == "__main__":
    asyncio.run(main())
