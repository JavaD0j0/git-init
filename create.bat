@ECHO OFF
SET filename=%1

:: We want to change directory to %USERPROFILE% now
CD /d %USERPROFILE%

If "%filename%"=="" (
    ECHO "Error --> You need to enter a filename for this repository!"
    ECHO "Try again ..."
) ELSE (
    python remote.py %filename%
)

PAUSE