@echo off
rem Kullanım: baslat.bat VIDEO_ID   (örn. baslat.bat ec69uXnbLM4)
cd /d "%~dp0"
if "%1"=="" (
  echo Kullanim: baslat.bat VIDEO_ID
  exit /b 1
)
start "" http://localhost:8765/video.html?v=%1
start "" http://localhost:8765/prompter.html?f=veri/%1/prompter.txt
python -m http.server 8765
