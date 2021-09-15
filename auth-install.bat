@echo off

chcp 65001 > NUL

echo **************************************************************
echo *  歡迎使用 auth-Hello                                       *
echo *  安裝後，可以自動登入                                      *
echo *                                                by George   *
echo **************************************************************
echo.

set /p UN=Enter Username: 
set /p PSWD=Enter password: 


echo %UN% > %userprofile%\.helloauthcred
echo %PSWD% >> %userprofile%\.helloauthcred
echo.
echo 初始化設定中...

taskkill /f /im auth-Hello.exe /fi "username eq %USERNAME%" > NUL
xcopy /y auth-Hello.exe %APPDATA%"\Microsoft\Windows\Start Menu\Programs\Startup" >NUL
start %APPDATA%"\Microsoft\Windows\Start Menu\Programs\Startup"\auth-Hello.exe

echo.
echo 恭喜您，完成設定囉 ^^.^<
echo.

pause
