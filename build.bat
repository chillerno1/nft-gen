@echo off

set name=nftgen

REM Path to the project root directory
set root=%cd%

set mainPath=%root%\src\%name%\main.py

set outputPath=%root%\build
set workPath=%root%\tmp
set specPath=%root%\tmp
set paths=%root%\venv\Lib\site-packages

set data=data
set iconImage=%root%\%data%\icon.ico


@RD /S /Q "%outputPath%"

pyinstaller ^
--distpath %outputPath% ^
--workpath %workPath% ^
--specpath %specPath% ^
--name %name% ^
--icon %iconImage% ^
--onefile ^
--noconfirm ^
%mainPath%


set configPath=%root%\config.yaml
set attributesPath=%root%\attributes.yaml

xcopy %configPath% %outputPath%
xcopy %attributesPath% %outputPath%

@RD /S /Q "%workPath%"
