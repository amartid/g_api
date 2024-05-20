@echo off
setlocal

REM Set current directory as the target directory
set "target_directory=%~dp0"

REM Set output file path
set "output_file=%target_directory%output.txt"

REM Clear output file if it exists
if exist "%output_file%" (
    del /q "%output_file%"
)

REM Function to process each .py file
:process_file
for %%I in ("%target_directory%\*.py") do (
    echo %%~fI >> "%output_file%"
    type "%%~fI" >> "%output_file%"
    echo. >> "%output_file%"
)

REM Recursive call to process subdirectories
for /r "%target_directory%" %%D in (*) do (
    if /i "%%~xD"==".py" (
        echo %%~fD >> "%output_file%"
        type "%%~fD" >> "%output_file%"
        echo. >> "%output_file%"
    )
)

echo Task completed. Output saved in %output_file%
exit /b 0
