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


pip install %root%\


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
set assetsFolder=Assets

xcopy %configPath% %outputPath%
xcopy %attributesPath% %outputPath%

mkdir %outputPath%\%assetsFolder%

@RD /S /Q "%workPath%"
