@echo off
SET path_self=%~dp0
CALL :NORMALIZEPATH  %path_self%\..\..
set path_project=%RETVAL%

cd %path_project%
rmdir /S /Q dist
pip install nuitka
python -m nuitka --follow-imports --output-dir=dist/psistats2 --verbose psistats2.py
mkdir dist\psistats2\etc
copy etc\psistats2.conf dist\psistats2\etc

:: ========== FUNCTIONS ==========
EXIT /B

:NORMALIZEPATH
  SET RETVAL=%~dpfn1
  EXIT /B