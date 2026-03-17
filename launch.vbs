Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd.exe /k cd /d ""%~dp0"" && if exist ""venv\Scripts\python.exe"" (venv\Scripts\python app.py) else (python app.py)", 1
Set WshShell = Nothing
