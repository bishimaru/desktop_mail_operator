@echo off
:loop
python check_mail.py
echo スクリプトが終了しました。再起動します...
timeout /t 5 >nul
goto loop
