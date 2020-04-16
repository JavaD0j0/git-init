@ECHO OFF
SET filename=%1
SET currDir=%cd%

:: This command refers to the full path to the batch file directory
:: (which cannot change) 
CD /d %~dp0
ECHO "Batch file directory is %~dp0"

If "%filename%"=="" (
    ECHO "Error --> You need to enter a filename for this repository!"
    ECHO "Try again ..."
) ELSE (
    python remote.py %filename%
)

CD %currDir%
PAUSE