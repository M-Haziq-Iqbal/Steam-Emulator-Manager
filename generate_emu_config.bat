@echo off

::391540 - Undertale
::1290000 - Powerwash Simulator

::read data from login_appid.txt file
if exist login_appid.txt (
	for /F "tokens=1,* delims==" %%A in (login_appid.txt) do (
		if %%A == appid ( set "appid=%%B" )
		if %%A == accountName ( set "accountName=%%B" )
		if %%A == password ( set "PASSWORD=%%B" )
	)
)

setlocal enabledelayedexpansion
endlocal & set "appid=%appid%" & set "accountName=%accountName%" & set "PASSWORD=%PASSWORD%"

echo AppID: %appid%
echo Account Name: %accountName%
echo Password: %PASSWORD%
echo.

:appid_input
if not defined appid (
	set /p appid="Enter the appid: "
	if not defined appid (
		echo Error: Appid is required.
		echo.
        	goto :appid_input
	)
)

:accountName_input
if not defined accountName (
	set /p accountName="Enter Steam account name: "
	if not defined accountName (
		echo Error: Steam account name is required.
		echo.
        	goto :accountName_input
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

set "dll=steam_api.dll"
set "dll64=steam_api64.dll"

::find dll folder
for %%a in ("%CD%\..") do (
   if exist ..\%dll% ( 
		set "dll_folder=%%~fa"
		set "dll_file=%dll%"
	)
   if exist ..\%dll64% ( 
		set "dll_folder=%%~fa"
		set "dll_file=%dll64%"
	)
)

:: loop through all folders and subfolders
for /f "delims=" %%d in ('dir /ad /b /s ..') do (
   set exclude=0

   :: Loop through working directory to be excluded
   for /f "delims=" %%e in ('dir /ad /b /s') do (
      if "%%d" == "%%e" (
         set exclude=1
      )
   )

   if !exclude! equ 0 (
      if exist "%%d\%dll%" (
         set "dll_folder=%%d"
			set "dll_file=%dll%"
      )
      if exist "%%d\%dll64%" (
         set "dll_folder=%%d"
			set "dll_file=%dll64%"
      )
   )
)

echo DLL folder: %dll_folder%
echo.

setlocal enabledelayedexpansion
endlocal & set "dll_folder=%dll_folder%" & set "dll_file=%dll_file%"

::setup constant

set "dll_file_original=%dll_folder%\%dll_file%"
set "dll_file_goldberg=Goldberg_Lan_Steam_Emu_master--475342f0\experimental\%dll_file%"
set "dll_file_backup=%dll_folder%\backup\%appid%_%dll_file%"
set "script_file=goldberg_emulator-master-scripts\scripts\generate_emu_config.py"
set "interfaces_exe=Goldberg_Lan_Steam_Emu_master--475342f0\tools\generate_interfaces_file.exe"

::delete folders and files from any previous installation
if exist "%appid%_output" ( rd /s /q "%appid%_output" )
if exist "login_temp" ( rd /s /q "login_temp" )
if exist "%dll_folder%\steam_settings" ( rd /s /q "%dll_folder%\steam_settings" )
if exist "%dll_folder%\steam_interfaces.txt" ( del "%dll_folder%\steam_interfaces.txt" )
if exist "%dll_file_backup%" ( copy "%dll_file_backup%" "%dll_file_original%" > nul )
echo Successfully deleted folders and files from any previous installation!

pause
echo.

::create emu config:
call python %script_file% %accountName% %PASSWORD% %appid% > nul

::move emu config to game directory
move "%appid%_output\steam_settings" "%dll_folder%" > nul
if exist "%dll_folder%\steam_settings" ( echo Successfully created emu config in dll folder! )

::create steam_interfaces.txt
start "" "%interfaces_exe%" "%dll_file_original%"

:check_running
timeout /t 1 /nobreak >nul
tasklist | find /i "%interfaces_exe%" >nul
if %ERRORLEVEL% equ 0 ( goto :check_running )

::move steam_interfaces.txt to dll folder::
move "steam_interfaces.txt" "%dll_folder%" > nul
if exist "%dll_folder%\steam_interfaces.txt" (
	echo Successfully created steam_interfaces.txt in dll folder!
)

::backup original steam_api.dll or steam_api64.dll
if not exist "%dll_file_backup%" (
	mkdir "%dll_folder%\backup"
	move "%dll_file_original%" "%dll_file_backup%" > nul
	if exist "%dll_file_backup%" (
		echo Successfully backed up original %appid% %dll_file% to backup folder!
	)
)

::copy steam_api.dll or steam_api64.dll to dll folder
copy "%dll_file_goldberg%" "%dll_folder%" > nul
if exist "%dll_file_original%" (
	echo Successfully copied Goldberg %dll_file% to dll folder!
)

::delete_leftover_folders
if exist "%appid%_output" ( rd /s /q "%appid%_output" )
if exist "login_temp" ( rd /s /q "login_temp" )
if exist "backup" ( rd /s /q "backup" )

pause