call venv\Scripts\activate
echo Y | del dist
pyinstaller --noconsole --noconfirm --onefile .\src\convert_philter.py
echo Y | xcopy dist\convert_philter.exe installer\convert_philter.exe /E