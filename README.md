# Steam Emulator Manager

Welcome to Steam Emulator Manager, a Python terminal application that allows you to detect folders containing original `steam_api.dll` and `steam_api64.dll` files, select which folder to use, create backups of those files, replace them with modified equivalents, login into a Steam account, find games based on name or SteamID, and generate a `steam_settings` folder for each chosen folder.

This program utilizes Goldberg Emulator. You can check it out [here](https://gitlab.com/Mr_Goldberg/goldberg_emulator).

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [GUI Development](#gui-development)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone or download this repository to your local machine.
2. Make sure you have Python installed (version 3.11 or higher).
3. Navigate to the project directory in your terminal.
4. Install the required dependencies by running:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Place the directory folder of the program in any parent folder that may contain the `steam_api.dll` and `steam_api64.dll` files in any of the subfolders.
2. Run the `main.py` file:
    ```
    python main.py
    ```
3. Follow the on-screen instructions to:
   - Detect folders containing the original `steam_api.dll` and `steam_api64.dll` files.
   - Select which folder to use.
   - Create backups of the original files.
   - Replace the original files with modified equivalents.
   - Login into a Steam account.
   - Find games based on name or SteamID.
   - Generate `steam_settings` folders for each chosen folder.

## Features

- Detect folders containing original `steam_api.dll` and `steam_api64.dll` files.
- Select which folder to use.
- Create backups of original files.
- Replace original files with modified equivalents.
- Login into a Steam account.
- Find games based on name or SteamID.
- Generate `steam_settings` folders for each chosen folder.

## GUI Development

Please note that a GUI for this application is still in ongoing development. Stay tuned for updates!

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
