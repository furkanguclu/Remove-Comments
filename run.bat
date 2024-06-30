@echo off
set SYS_SCRIPT=remove_comments.py

REM python çalışmazsa pythonun kurulu path kısımı değiştirin

set PYTHON_PATH=C:\Program Files\Python312\python.exe


if not defined PYTHON_PATH (
    set PYTHON_COMMAND=python
) else (
    set PYTHON_COMMAND="%PYTHON_PATH%"
)

%PYTHON_COMMAND% %SYS_SCRIPT%

pause
