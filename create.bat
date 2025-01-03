@ECHO OFF
SET filename=%1
SET local=%2

:: This command refers to the full path to the batch file directory
:: (which cannot change) 
CD /d %~dp0
@REM ECHO "Batch file directory is %~dp0"

IF "%filename%"=="" (
    ECHO "Error --> You need to enter a filename for this repository!"
    ECHO "Try again ..."
) ELSE (
    IF "%local%"=="-l" (
        ECHO "Creating project locally..."
        python remote.py %filename% %local%
    ) ELSE (
        python remote.py %filename%
    )

    :: Redirect user straight to newly creatred project folder
    CD %PROJECT_DIR%\%filename%
)

PAUSE