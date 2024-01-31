@echo off

::391540 - Undertale
::1290000 - Powerwash Simulator

:start
::read data from login_appid.txt file
if exist login_appid.txt (
	for /F "tokens=1,* delims==" %%A in (login_appid.txt) do (
		if %%A == appid ( call set "appid=%%B" )
		if %%A == accountName ( call set "accountName=%%B" )
		if %%A == password ( call set "PASSWORD=%%B" )
	)
)

echo AppID: %appid%
echo Account Name: %accountName%
echo Password: %PASSWORD%
echo MAKE SURE THE DETAILS ABOVE ARE CORRECT!
echo.

:appid_input
if not defined appid (
	call set /p appid="Enter the appid: "
	if not defined appid (
		echo Error: Appid is required.
		echo.
        	goto :appid_input
	)
)

:accountName_input
if not defined accountName (
	call set /p accountName="Enter Steam account name: "
	if not defined accountName (
		echo Error: Steam account name is required.
		echo.
        	goto :accountName_input
	)
)

:password_input
if not defined PASSWORD (
	call set /p PASSWORD="Enter Steam password: "
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
		call set "dll_folder=%%~fa"
		call set "dll_file=%dll%"
	)
   if exist ..\%dll64% ( 
		call set "dll_folder=%%~fa"
		call set "dll_file=%dll64%"
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
		if "%%d" == "%CD%" (
			set exclude=1
		)
   )

	setlocal enabledelayedexpansion
   if !exclude! equ 0 (
		endlocal
      if exist "%%d\%dll%" (
         call set "dll_folder=%%d"
			call set "dll_file=%dll%"
      )
      if exist "%%d\%dll64%" (
         call set "dll_folder=%%d"
			call set "dll_file=%dll64%"
      )
   )
	endlocal
)

if exist "%dll_folder%" (
	echo Opening DLL directory: %dll_folder%\%dll_file%
	start "" "%dll_folder%"
	echo.
) else (
	echo DLL directory cannot be found!
	goto :restart
)

::setup constant

set "dll_file_original=%dll_folder%\%dll_file%"
set "dll_file_goldberg=Goldberg_Lan_Steam_Emu_master--475342f0\experimental\%dll_file%"
set "dll_file_backup=%dll_folder%\backup\%appid%_%dll_file%"
set "script_file=goldberg_emulator-master-scripts\scripts\generate_emu_config.py"
set "interfaces_exe=Goldberg_Lan_Steam_Emu_master--475342f0\tools\generate_interfaces_file.exe"

::delete folders and files from any previous installation
set "prev_install=1"

if exist "%appid%_output" ( rd /s /q "%appid%_output"
) else if exist "login_temp" ( rd /s /q "login_temp" 
) else if exist "%dll_folder%\steam_settings" ( rd /s /q "%dll_folder%\steam_settings" 
) else if exist "%dll_folder%\steam_interfaces.txt" ( del "%dll_folder%\steam_interfaces.txt" 
) else if exist "steam_interfaces.txt" ( del "steam_interfaces.txt" 
) else if exist "%dll_file_backup%" ( copy "%dll_file_backup%" "%dll_file_original%" > nul 
) else (set "prev_install=0")

if %prev_install%==1 (
	echo Successfully deleted/restored folders/files from any previous installation!
	pause
)

::create emu config:
call python %script_file% %accountName% %PASSWORD% %appid% > nul
if %ERRORLEVEL% neq 0 (
	echo Unable to run generate_emu_config.py
	goto :restart
	)

::move emu config to game directory
move "%appid%_output\steam_settings" "%dll_folder%" > nul
if exist "%dll_folder%\steam_settings" ( echo Successfully created emu config in dll folder! )

::create steam_interfaces.txt
if exist "%dll_file_original%" (start "" "%interfaces_exe%" "%dll_file_original%")

:check_running
timeout /t 1 /nobreak >nul
tasklist | find /i "%interfaces_exe%" > nul
if %ERRORLEVEL% equ 0 ( goto :check_running )

::move steam_interfaces.txt to dll folder::
move "steam_interfaces.txt" "%dll_folder%" > nul
if exist "%dll_folder%\steam_interfaces.txt" (
	echo Successfully created steam_interfaces.txt in dll folder!
) else (
	echo Unable to create steam_interfaces.txt!
	goto :restart
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

echo.
echo Goldberg emu has been successfully implemented!

:restart
set /p restart="Do you want to restart the process? (y/n): "
echo.
if "%restart%" == "y" (
	goto :start
) else if "%restart%" == "n" (
	echo exiting...
	timeout /t 2 /nobreak >nul
	exit
) else (
	echo please enter only y/n
	goto :restart
)

pause