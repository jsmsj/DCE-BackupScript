@echo off

@REM MAKE SURE THAT THE MAIN_PATH ENDS WITH A `\` (BACKSLASH)
set "MAIN_PATH=C:\Users\USERNAME\Desktop\Python stuff\Github Public\DCE-BackupScript\"

pushd "%MAIN_PATH%"
set "PYTHON_PATH=python"
set "FILE_1=%MAIN_PATH%bash_script_gen.py"
set "FILE_2=%MAIN_PATH%DCE_CLI\my_cmd.bat"
set "FILE_3=stitch_json.py"

echo Generating the batch script for exporting: "%FILE_1%"
%PYTHON_PATH% "%FILE_1%"
if errorlevel 1 goto ERROR

pushd "DCE_CLI\"

echo Running the batch script: "%FILE_2%"
"%FILE_2%"
if errorlevel 1 goto ERROR

REM echo Stitching the json files: "%FILE_3%"
REM %PYTHON_PATH% "%FILE_3%"
REM if errorlevel 1 goto ERROR

popd
popd

echo All files generated.
pause > nul
exit /b 0

:ERROR
echo An error occurred while running one of the files.
pause > nul
exit /b 1
