@ECHO OFF
SET filename=%1

:: This command will expand to the drive letter and path in which the batch file
:: is located (which cannot change) 
:: CD /d %USERPROFILE%\GitInit
CD /d %~dp0
ECHO "Current dir is %~dp0"

If "%filename%"=="" (
    ECHO "Error --> You need to enter a filename for this repository!"
    ECHO "Try again ..."
) ELSE (
    python remote.py %filename%
)

PAUSE