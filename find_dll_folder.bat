@echo off
setlocal enabledelayedexpansion

set "dll_file=steam_api.dll"
set "dll64_file=steam_api64.dll"

::find dll folder
for %%a in ("%CD%\..") do (
   if exist ..\%dll_file% ( set "dll_folder=%%~fa" )
   if exist ..\%dll64_file% ( set "dll_folder=%%~fa" )
)

:: Loop through all folders and subfolders
for /f "delims=" %%d in ('dir /ad /b /s ..') do (
   set exclude=0

   :: Loop through working directory to be excluded
   for /f "delims=" %%e in ('dir /ad /b /s') do (
      if "%%d" == "%%e" (
         set exclude=1
      )
   )

   if !exclude! equ 0 (
      if exist "%%d\%dll_file%" (
         set "dll_folder=%%d"
      )
      if exist "%%d\%dll64_file%" (
         set "dll_folder=%%d"
      )
   )
)

echo DLL folder: %dll_folder%

endlocal
pause