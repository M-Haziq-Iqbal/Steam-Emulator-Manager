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

async def search_by_game_name(name): #"https://api.steampowered.com/ISteamApps/GetAppList/v0002/"
    app_list = await get_app_list()
    name_normalized = re.sub(r'[^a-zA-Z0-9]', '', name.lower())
    matching_apps = {}
    for app in app_list["applist"]["apps"]:
        app_name_normalized = re.sub(r'[^a-zA-Z0-9]', '', app["name"].lower())
        if name_normalized in app_name_normalized:
            matching_apps[app["appid"]] = app["name"]
    return matching_apps

async def search_by_appid(appid):
    app_info = await get_app_info_by_id(appid)
    if app_info and app_info.get(str(appid), {}).get("success"):
        app_data = app_info[str(appid)].get("data")
        # return {'name': app_data["name"], 'type': app_data["type"]}
        if app_data and app_data.get("type") == "game":
            return {"appid": app_data["steam_appid"], "name": app_data["name"], "type": app_data["type"]}
        else:
            print(f'Notice: {app_data["name"]} is not the base game')
            return None
    else:
        print(f"Notice: No game found with ID {appid}.")
        return None

async def main():
    while True:
        matching_appid = None
        matching_name = None

        search_query = input("Enter the app ID or name of the app: ")
        if search_query.isdigit():  # Check if input is only a number
            matching_appid = await search_by_appid(int(search_query)) #{"appid": appid, "name": app_data["name"]}
            if matching_appid:
                print(f'AppID: {matching_appid["appid"]}, Name: {matching_appid["name"]}')
                
        else:
            matching_name = await search_by_game_name(search_query)

            if matching_name and len(matching_name) > 10:
                print(f"\nMatching data for '{search_query}' exceeds 10 games. Please enter more specific keywords: ")
            if matching_name:
                print(f"\nMatching data for '{search_query}':")

                tasks = [search_by_appid(app_id) for app_id in matching_name.keys()] # creates a list of coroutine objects (tasks) using a list comprehension.
                await asyncio.gather(*tasks) # fetch app information for multiple app IDs concurrently.
                
                # app_infos = await asyncio.gather(*tasks)
                # for app_id, app_name in matching_name.items():
                #     app_info = app_infos.pop(0)
                #     if app_info and app_info.get("type") == "game":
                #         print(f"AppID: {app_id}, Name: {app_name} (matching name)")
                
                # search again game data through appid
                search_query = input("Enter the appID of the app: ")
                
                if search_query.isdigit():  # Check if input is only a number
                    matching_appid = await search_by_appid(int(search_query))
                else:
                    print(f"{search_query} is not a valid AppID")

            else:
                print(f"Notice: No apps found with a name containing '{search_query}'.")
        
        if matching_appid:
            break # Exit the loop
        elif matching_name and len(matching_name) > 10: 
            print(f"Restarting...\n")
            continue # Restart the loop
        else:  
            print(f"Restarting...\n")
            continue # Restart the loop

if __name__ == "__main__":
    asyncio.run(main())
