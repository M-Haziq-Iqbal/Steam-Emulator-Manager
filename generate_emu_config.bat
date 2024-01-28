@echo off

::setup variables::
set "appid=1290000"
set "USERNAME=KurashiAOI"
set "PASSWORD=rnRv8Gu#QB3NJbF!ety$"

::-----------------------------------------------------------------------------------------------::

:appid_input
if not defined appid (
	set /p appid="Enter the appid: "
	if not defined appid (
		echo Error: Appid is required.
		echo.
        	goto :appid_input
	)
)

:username_input
if not defined USERNAME (
	set /p USERNAME="Enter Steam username: "
	if not defined USERNAME (
		echo Error: Steam username is required.
		echo.
        	goto :username_input
	)
)

:password_input
if not defined PASSWORD (
	set /p PASSWORD="Enter Steam password: "
	if not defined PASSWORD (
		echo Error: Steam password is required.
		echo.
        	goto :password_input
	)
)

::setup constant
set "dll_file_goldberg=Goldberg_Lan_Steam_Emu_master--475342f0\experimental\steam_api.dll"
set "dll64_file_goldberg=Goldberg_Lan_Steam_Emu_master--475342f0\experimental\steam_api64.dll"
set "dll_file_backup=..\backup\steam_api(%appid%).dll"
set "dll64_file_backup=..\backup\steam_api64(%appid%).dll"
set "script_file=goldberg_emulator-master-scripts\scripts\generate_emu_config.py"
set "interfaces_exe=Goldberg_Lan_Steam_Emu_master--475342f0\tools\generate_interfaces_file.exe"

::delete folders and files from any previous installation
if exist "%appid%_output" ( rd /s /q "%appid%_output" )
if exist "login_temp" ( rd /s /q "login_temp" )
if exist "..\steam_settings" ( rd /s /q "..\steam_settings" )
if exist "steam_interfaces.txt" ( del "steam_interfaces.txt" )
if exist "..\steam_interfaces.txt" ( del "..\steam_interfaces.txt" )
if exist "%dll_file_backup%" ( copy "%dll_file_backup%" "..\steam_api.dll" > nul )
if exist "%dll64_file_backup%" ( copy "%dll64_file_backup%" "..\steam_api64.dll" > nul )
echo Successfully deleted folders and files from any previous installation!

pause

if exist "..\steam_api.dll" (
	set "dll_file_original=..\steam_api.dll"
) else if exist "..\steam_api64.dll" (
	set "dll_file_original=..\steam_api64.dll"
)

::backup original steam_api.dll or steam_api64.dll
if not exist "%dll_file_backup%" (
	mkdir "..\backup"
	move "%dll_file_original%" "%dll_file_backup%" > nul
	if exist "%dll_file_backup%" (
		echo Successfully backed up original %appid% steam_api.dll!
	)
)

::copy steam_api.dll or steam_api64.dll to dll folder
copy "%dll_file_goldberg%" .. > nul
if exist "%dll_file_original%" (
	echo Successfully copied Goldberg steam_api.dll to dll folder!
)

::create emu config::
call python %script_file% %USERNAME% %PASSWORD% %appid%
echo Successfully created emu config!

::move emu config to game directory::
move "%appid%_output\steam_settings" .. > nul
echo Successfully moved emu config to game directory!

:delete_leftover_folders
if exist "%appid%_output" ( rd /s /q "%appid%_output" )
if exist "login_temp" ( rd /s /q "login_temp" )

pause