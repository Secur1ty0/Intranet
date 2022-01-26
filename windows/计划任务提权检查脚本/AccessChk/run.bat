@echo off
for /f %%i in (only_task_path.txt) do echo %%i && accesschk.exe  /accepteula -uwqv %%i
pause