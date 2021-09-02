@echo off

set name=nft-gen

REM Path to the project root directory
set root=%cd%

set mainPath=%root%\src\nftgen\main.py

set outputPath=%root%\build
set workPath=%root%\tmp
set specPath=%root%\tmp
set paths=%root%\venv\Lib\site-packages

set iconImage=%root%\data\icon.ico

set config=config.yaml
set attributes=attributes.yaml
set resources=resources


pip install %root%\


@RD /S /Q "%outputPath%"

pyinstaller ^
--distpath %outputPath% ^
--workpath %workPath% ^
--specpath %specPath% ^
--name %name% ^
--icon %iconImage% ^
--add-data %root%\%config%;%resources% ^
--add-data %root%\%attributes%;%resources% ^
--onefile ^
--noconfirm ^
%mainPath%

@RD /S /Q "%workPath%"
