@ECHO OFF
SET filename=%1
:: SET flag=%2

REM We want to change directory to %USERPROFILE% now
CD /d %USERPROFILE%

IF %filename%=="" (
    ECHO "Error --> You need to enter a filename for this repository!"
    ECHO "Try again ..."
) ELSE (
    REM If you just want to set up a repository locally (Not sure if really needed)
    ::IF %flag%=="l" (
    ::    python local.py %filename%
    ::)

    python remote.py %filename%

    ECHO "Successfully created repository..."
)